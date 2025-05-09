class ConversationState:
    def __init__(self, user_id, question_title, question_body):
        self.user_id = user_id
        self.question_title = question_title
        self.question_body = question_body
        self.subjects = []  # 복수 주제 저장

    def add_subject(self, subject_name, subject_description):
        subject = {
            "subject_name": subject_name,
            "subject_description": subject_description,
            "functions": [],  # 각 함수: 이름, 파라미터, 결과 포함
        }
        self.subjects.append(subject)

    def add_function_to_subject(self, subject_name, function_name, function_params):
        for subject in self.subjects:
            if subject["subject_name"] == subject_name:
                subject["functions"].append(
                    {
                        "function_name": function_name,
                        "function_params": function_params,
                        "function_result": None,
                    }
                )
                return
        raise ValueError(f"Subject '{subject_name}' not found.")

    def set_function_result(self, subject_name, function_name, result):
        for subject in self.subjects:
            if subject["subject_name"] == subject_name:
                for fn in subject["functions"]:
                    if fn["function_name"] == function_name:
                        fn["function_result"] = result
                        return
        raise ValueError(
            f"Function '{function_name}' in subject '{subject_name}' not found."
        )

    def to_summary_prompt(self):
        """
        모든 주제와 함수 실행 결과를 포함한 최종 요약 프롬프트 생성
        """
        prompt = f"사용자 ID: {self.user_id}\n"
        prompt += f"문의 제목: {self.question_title}\n"
        prompt += f"문의 내용: {self.question_body}\n\n"
        prompt += "분석된 문의 주제와 함수 결과:\n"

        for subject in self.subjects:
            prompt += f"\n[주제: {subject['subject_name']}]\n"
            prompt += f"{subject['subject_description']}\n"
            for fn in subject["functions"]:
                prompt += f"  - 결과: {fn['function_result']}\n"
        return prompt


def validate_state(state: ConversationState):
    if not state.subjects:
        return "주제를 찾을 수 없습니다. 질문을 다시 확인해주세요."
    if not state.user_id:
        return "사용자 정보가 누락되었습니다."
    return None
