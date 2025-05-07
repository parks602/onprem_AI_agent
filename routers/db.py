# routers/db.py
from fastapi import APIRouter
from db.query_executor import execute_query  # DB 쿼리 실행 함수

router = APIRouter()


@router.get("/db_query")
async def run_db_query(query: str):
    # DB 쿼리 실행
    result = execute_query(query)
    return {"query": query, "result": result}
