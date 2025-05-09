# routers/ask.py
from fastapi import APIRouter, Request
from pydantic import BaseModel

from llm.prompt_runner import (
    find_subject_generator,
    select_functions_generator,
    make_report_generator,
)
from core.tool_runner import run_tool_response
from core.query_module import ConversationState, validate_state

router = APIRouter()


class QuestionRequest(BaseModel):
    qunestion_name: str
    question: str
    account_id: str


@router.post("/ask")
async def ask(request_data: QuestionRequest, request: Request):
    model = request.app.state.model
    tokenizer = request.app.state.tokenizer

    user_question = request_data.question
    user_question_name = request_data.qunestion_name
    user_question_id = request_data.account_id

    state = ConversationState(user_question_id, user_question_name, user_question)
    # 모델에서 주제 추출 및 질문 처리

    find_subject_generator(state, model, tokenizer)
    error = validate_state(state)
    if error:
        return {"status": "error", "message": error}

    # 질문에 맞는 함수 목록 선택
    select_functions_generator(state, model, tokenizer)
    error = validate_state(state)
    if error:
        return {"status": "error", "message": error}
    # 툴 실행 및 결과 처리

    run_tool_response(state)

    final_report = make_report_generator(
        state,
        model,
        tokenizer,
    )
    return {"status": "success", "response": final_report}
