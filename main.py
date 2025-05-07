import requests

BASE_URL = "http://127.0.0.1:8000/"
PARM = "ask"  # FastAPI 서버 주소

data = {
    "qunestion_name": "제니가 사라졌어요",
    "question": "3월 15일에 접속했더니 제니가 500만 정도 사라졌습니다. 확인 부탁드립니다.",
    "account_id": "user001",
}

# POST 요청
response = requests.post(BASE_URL + PARM, json=data)

print(response)
