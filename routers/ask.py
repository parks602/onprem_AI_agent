# routers/ask.py
from fastapi import APIRouter, Request
from pydantic import BaseModel

from llm.prompt_runner import find_subject_generator, select_functions_generator
from core.tool_runner import run_tool_response

router = APIRouter()


class QuestionRequest(BaseModel):
    qunestion_name: str
    question: str
    account_id: str


@router.post("/ask")
async def ask(request_data: QuestionRequest, request: Request):
    model = request.app.state.model
    tokenizer = request.app.state.tokenizer
    # 모델에서 주제 추출 및 질문 처리
    subject_json = find_subject_generator(request_data, model, tokenizer)
    # 질문에 맞는 함수 목록 선택
    if subject_json != None:
        function_name_list, function_param_list = select_functions_generator(
            request_data, subject_json, model, tokenizer
        )
        print("함수 목록:", function_name_list)
    else:
        pass
    # 툴 실행 및 결과 처리

    data = run_tool_response(function_name_list, function_param_list)
    print("툴 실행 결과:", data)

    # if state:
    #     # 성공적인 응답 처리
    #     final_report = make_report_generator(
    #         question,
    #         make_report_prompt,
    #         function_list,
    #         return_message,
    #         model,
    #         tokenizer,
    #     )
    # else:
    #     # 실패 시 처리
    #     final_report = (
    #         "AI Agent가 답변을 만들지 못했습니다. 운영 Unit의 수기 답변이 필요합니다."
    #     )

    return {"status": "success", "response": final_report}
