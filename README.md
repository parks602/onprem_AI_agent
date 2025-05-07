# 🎮 onprem_AI_agent  
onprem_AI_agent는 게임 고객 문의를 자동화하여 처리하는 온프레미스 AI 에이전트입니다. 이 프로젝트는 OpenAI의 Function Calling 기능을 활용하여, 고객의 문의를 분석하고 적절한 함수를 호출하여 자동으로 응답을 생성하는 시스템을 구축하는 것을 목표로 합니다.

⚠️ 현재 이 프로젝트는 개발 중이며, 최종 답변 생성 기능이 아직 구현되지 않았습니다. 향후 업데이트를 통해 완성될 예정입니다.

# 🧠 프로젝트 개요  
목표: 게임 고객의 다양한 문의 사항을 자동으로 분석하고, 적절한 함수를 호출하여 신속하고 정확한 응답을 제공하는 AI 에이전트를 개발합니다.

주요 기능:  
- 고객 문의 분석 및 이해  
- 적절한 함수 호출을 위한 Function Calling 구현  
- 다양한 도구(툴)들을 통한 데이터 조회 및 처리  
- 향후 최종 응답 생성 기능 추가 예정  

# 🛠️ 기능 및 구성  
🔧 Function Calling  
OpenAI의 Function Calling 기능을 활용하여, 고객의 문의에 따라 적절한 함수를 자동으로 호출합니다. 이를 통해 다양한 고객 요청을 자동으로 처리할 수 있습니다.

# 🧰 도구(툴) 구성  
프로젝트는 다양한 카테고리의 도구들을 정의하여, 고객 문의에 따라 적절한 도구를 선택하여 사용합니다.

- **결제 관련 도구 (PAYMENT_TOOLS)**:
    - user_payment_history: 유저의 전체 결제 내역 조회
    - user_payment_history_by_date: 지정된 날짜 범위 내 결제 내역 조회
    - user_refund_history: 유저의 환불 내역 조회

- **계정 관련 도구 (ACCOUNT_TOOLS)**:
    - get_account_info: 계정의 캐릭터 목록 및 최근 접속 기록 조회
    - get_character_info: 캐릭터 정보 조회
    - get_character_item_usage: 캐릭터의 아이템 사용 로그 조회

- **아이템 관련 도구 (ITEM_TOOLS)**:
    - get_get_item_log: 유저의 아이템 획득 로그 조회
    - get_use_item_log: 유저의 아이템 사용 로그 조회

- **이벤트 관련 도구 (EVENT_TOOLS)**:
    - get_event_item_usage: 유저의 이벤트 아이템 사용 내역 조회

- **보안 관련 도구 (SECURITY_TOOLS)**:
    - get_login_log: 유저의 로그인 기록 조회

# 🧩 도구 자동 등록  
get_category_tools(category) 함수를 통해 각 카테고리에 해당하는 도구들을 자동으로 불러올 수 있습니다. 이를 통해 코드의 유지보수성과 확장성을 높였습니다.

```python
def get_category_tools(category):
    tools = {
        "결제": PAYMENT_TOOLS,
        "계정": ACCOUNT_TOOLS,
        "아이템": ITEM_TOOLS,
        "이벤트": EVENT_TOOLS,
        "보안": SECURITY_TOOLS,
        "기타": OTHER_TOOLS,
    }
    return tools[category]
```
# 🚀 설치 및 실행 방법

1. **저장소 클론**
    ```bash
    git clone https://github.com/parks602/onprem_AI_agent.git
    cd onprem_AI_agent
    ```

2. **가상 환경 설정 (선택 사항)**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows의 경우: venv\Scripts\activate
    ```

3. **필요한 패키지 설치**
    ```bash
    pip install -r requirements.txt
    ```

4. **모델 다운로드 및 설정**  
    phi-4-mini 모델을 다운로드하고, 프로젝트에 맞게 설정합니다. 모델 파일의 경로를 `model_path`에 지정해야 합니다.
    ```python
    model_path = "Your Phi-4-mini location"
    ```

# 📦 **사용 예시**
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import json

# 모델 및 토크나이저 로드
model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# 메시지 구성
messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant",
        "tools": json.dumps(tools),
    },
    {
        "role": "user",
        "content": "What is the result of Arsenal vs ManCity today?"
    }
]

# 입력 생성
inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_dict=True, return_tensors="pt")
inputs = {k: v.to(model.device) for k, v in inputs.items()}

# 응답 생성
output = model.generate(**inputs, max_new_tokens=128)
response = tokenizer.decode(output[0][len(inputs["input_ids"][0]):], skip_special_tokens=True)

print(response)
```

# 📌 향후 계획

- **최종 응답 생성 기능 추가**: 현재는 함수 호출까지의 흐름만 구현되어 있으며, 향후 함수 호출 결과를 바탕으로 최종 응답을 생성하는 기능을 추가할 예정입니다.
- **에러 처리 및 로깅 강화**: 시스템의 안정성을 높이기 위해 에러 처리 및 로깅 기능을 강화할 계획입니다.
- **테스트 케이스 추가**: 다양한 시나리오에 대한 테스트 케이스를 추가하여 시스템의 신뢰성을 높일 예정입니다.
