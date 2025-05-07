# main.py
from fastapi import FastAPI
import asyncio

# 라우터 임포트
from routers import ask, tools, db
from llm.model_handler import load_model, test_load_model
from db.query_executor import get_db_connection

app = FastAPI()  # FastAPI 애플리케이션 인스턴스 생성


# 비동기 함수로 모델 로딩
async def async_load_model():
    loop = asyncio.get_event_loop()
    # return await loop.run_in_executor(None, test_load_model)  ## 모델 로딩 함수 호출
    return await loop.run_in_executor(None, load_model)  # 실제 모델 로딩 함수 호출


# 비동기 함수로 DB 연결
async def async_get_db_connection():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, get_db_connection)


# FastAPI의 startup 이벤트에 연결된 함수로, 앱 시작 시 모델과 DB 연결을 비동기적으로 설정
@app.on_event("startup")
async def startup_event():
    print("모델과 DB 연결 시작")
    model_tokenizer_task = asyncio.create_task(async_load_model())  # 모델 로딩 작업
    db_task = asyncio.create_task(async_get_db_connection())  # DB 연결 작업

    app.state.model, app.state.tokenizer = (
        await model_tokenizer_task
    )  # 모델과 토크나이저 로드
    app.state.onn = await db_task  # DB 연결 설정

    print("모델 & DB 연결 완료")


# 라우터 등록
app.include_router(ask.router)  # 질문 관련 API
app.include_router(tools.router)  # 툴 관련 API
app.include_router(db.router)  # DB 관련 API
