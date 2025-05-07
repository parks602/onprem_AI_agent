from transformers import AutoModelForCausalLM, AutoTokenizer
import sys
import os

# 현재 파일 기준으로 상위 폴더 경로 구하기
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# 상위 폴더 경로를 sys.path에 추가
sys.path.append(parent_dir)


def load_model():
    model_path = "models/Phi4"  # <- 실제 경로로 수정
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map="cuda",
        torch_dtype="auto",
        local_files_only=True,
    )
    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        trust_remote_code=True,
        local_files_only=True,
    )
    return model, tokenizer


# 임시 테스트용 모델 객체
class DummyModel:
    def predict(self, input_text):
        return "테스트 응답입니다"


# 테스트용 모델 로딩 함수
def test_load_model():
    print("모델 로딩 생략 - 더미 모델 사용")
    return DummyModel(), DummyModel()
