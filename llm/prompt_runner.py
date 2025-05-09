import json, re
from transformers import PreTrainedModel, PreTrainedTokenizer
from core.prompts import openning_system_prompt, function_select_prompt, final_prompt
from core.functions_tools import get_category_tools
from core.query_module import ConversationState


def generator(
    user_question: str,
    system_prompt: str,
    tools: list,
    model: PreTrainedModel,
    tokenizer: PreTrainedTokenizer,
):
    messages = [
        {
            "role": "system",
            "content": system_prompt,
            "tools": json.dumps(tools),
        },
        {"role": "user", "content": user_question},
    ]
    print(messages)
    inputs = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, return_dict=True, return_tensors="pt"
    )
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    print("모델 입력 및 생성 시작")
    output = model.generate(**inputs, max_new_tokens=256)
    print("모델 답변 생성 완료")
    response = tokenizer.decode(
        output[0][len(inputs["input_ids"][0]) :], skip_special_tokens=True
    )
    return response


def find_subject_generator(
    state: ConversationState,
    model: PreTrainedModel,
    tokenizer: PreTrainedTokenizer,
):

    response = generator(
        state.question_body,
        openning_system_prompt.format(
            account_id=state.user_id, question_name=state.question_title
        ),
        [],
        model,
        tokenizer,
    )
    print("오프닝 모델 응답:", response)
    # JSON 파싱
    match = re.search(r"```json\s*(\[\s*{.*?}\s*\])\s*```", response, re.DOTALL)

    if match:
        json_str = match.group(1)
        try:
            tool_call = json.loads(json_str)
            for subject in tool_call:
                state.add_subject(subject["subject"], subject["parse"])

        except json.JSONDecodeError as e:
            print("JSON 디코딩 오류:", e)
            state.subjects = None
    else:
        print("JSON 형식이 아닙니다.")
        state.subjects = None


def select_functions_generator(
    state: ConversationState,
    model: PreTrainedModel,
    tokenizer: PreTrainedTokenizer,
):
    for subject in state.subjects:
        subject_name = subject["subject_name"]

        function_tool = get_category_tools(subject_name)
        if function_tool:
            response = generator(
                state.question_body,
                function_select_prompt.format(
                    account_id=state.user_id,
                    question_name=state.question_title,
                    subject_name=subject_name,
                    subject_description=subject["subject_description"],
                ),
                function_tool,
                model,
                tokenizer,
            )
            print("함수 선택 모델 응답:", response)
            if response:
                try:
                    match = re.search(r"```json\n(.*?)```", response, re.DOTALL)
                    cleaned = match.group(1)
                    tool_call = json.loads(cleaned)
                    state.add_function_to_subject(
                        subject_name,
                        tool_call["name"],
                        tool_call["parameters"],
                    )
                    print(
                        subject_name,
                        tool_call["name"],
                        tool_call["parameters"],
                    )
                except json.JSONDecodeError as e:
                    print("JSON 디코딩 오류:", e)
                    state.subjects = None
        else:
            print("해당 주제에 대한 함수가 없습니다.")
            state.subjects = None


def make_report_generator(
    state: ConversationState,
    model: PreTrainedModel,
    tokenizer: PreTrainedTokenizer,
):
    prompt_info = state.to_summary_prompt()
    print("최종 모델 입력 자료 : ", prompt_info)
    response = generator(
        state.question_body,
        final_prompt.format(info=prompt_info),
        (),
        model,
        tokenizer,
    )
    print("최종 보고서 모델 응답:", response)
    return response
