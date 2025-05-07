# routers/tools.py
from fastapi import APIRouter

# from core.tools import tools  # 툴 목록 가져오기

router = APIRouter()


@router.post("/run_tool")
async def run_tool(tool_name: str):
    # 툴 실행 로직

    return {"tool_name": tool_name, "result": "test"}
