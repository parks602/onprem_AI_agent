import json, re
from transformers import PreTrainedModel, PreTrainedTokenizer
from core.prompts import openning_system_prompt, function_select_prompt
from core.functions_tools import get_category_tools


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
    request,
    model: PreTrainedModel,
    tokenizer: PreTrainedTokenizer,
):
    user_question = request.question
    user_question_name = request.qunestion_name
    user_question_id = request.account_id
    response = generator(
        user_question,
        openning_system_prompt.format(
            account_id=user_question_id, question_name=user_question_name
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
            print("Parsed Tool Call:", tool_call)
            return tool_call
        except json.JSONDecodeError as e:
            print("JSON 디코딩 오류:", e)
            return None
    else:
        print("JSON 형식이 아닙니다.")
        return None


def select_functions_generator(
    request,
    subject_json: list,
    model: PreTrainedModel,
    tokenizer: PreTrainedTokenizer,
):
    user_question = request.question
    user_question_name = request.qunestion_name
    user_question_id = request.account_id

    function_name_list = []
    function_param_list = []
    for subject in subject_json:
        subject_name = subject["subject"]
        function_tool = get_category_tools(subject_name)
        if function_tool:
            response = generator(
                user_question,
                function_select_prompt.format(
                    account_id=user_question_id,
                    question_name=user_question_name,
                    subject_name=subject_name,
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
                    function_name_list.append(tool_call["name"])
                    function_param_list.append(tool_call["parameters"])
                except json.JSONDecodeError as e:
                    print("JSON 디코딩 오류:", e)
                    function_name_list.append(None)
                    function_param_list.append(None)
        else:
            function_name_list.append(None)
            function_param_list.append(None)
    return function_name_list, function_param_list


# def make_report_generator(
#     question: str,
#     system_porompt: str,
#     function_list: list,
#     return_message: str,
#     model: PreTrainedModel,
#     tokenizer: PreTrainedTokenizer,
# ):
#     response = generator(
#         question, system_porompt(function_list, return_message), [], model, tokenizer
#     )

#     return response
