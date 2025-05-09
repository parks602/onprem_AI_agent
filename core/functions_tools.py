# -*- coding: utf-8 -*-
# This file contains lists of functions that are used in the core module.
"""
사용 가능한 함수 목록을 정의합니다.

결재
1. user_payment_history: 유저의 전체 결제 내역을 조회합니다.
2. user_payment_history_by_date: 지정된 날짜 범위 내 유저의 결제 내역을 조회합니다.
3. user_refund_history: 유저의 환불 내역을 조회합니다.

계정
1. get_account_info: 계정의 캐릭터 목록 및 최근 접속 기록을 조회합니다.
2. get_character_info: 캐릭터의 정보를 조회합니다.
3. get_character_item_usage: 지정된 캐릭터가 사용한 아이템 로그를 조회합니다.

아이템
1. get_get_item_log: 지정된 유저의 아이템 획득 로그를 조회합니다.
2. get_use_item_log: 지정된 유저의 아이템 사용 로그를 조회합니다.
3. get_user_zeny_log: 지정된 유저의 지정된 날짜 동안의 제니 사용 로그를 조회합니다.

이벤트
1. get_event_item_usage: 지정된 유저의 이벤트 아이템 사용 내역을 조회합니다.

보안
1. get_login_log: 유저의 로그인 기록을 조회합니다.
"""


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


PAYMENT_TOOLS = [
    {
        "name": "user_payment_history",
        "description": "유저의 전체 결제 내역을 조회합니다.",
        "parameters": {
            "account_id": {"type": "str", "description": "조회할 계정 ID"},
        },
    },
    {
        "name": "user_payment_history_by_date",
        "description": "지정된 날짜 범위 내 유저의 결제 내역을 조회합니다.",
        "parameters": {
            "account_id": {"type": "str", "description": "조회할 계정 ID"},
            "start_date": {"type": "str", "description": "조회 시작일 (YYYY-MM-DD)"},
            "end_date": {"type": "str", "description": "조회 종료일 (YYYY-MM-DD)"},
        },
    },
    {
        "name": "user_refund_history",
        "description": "유저의 환불 내역을 조회합니다.",
        "parameters": {
            "account_id": {"type": "str", "description": "조회할 계정 ID"},
        },
    },
]
ACCOUNT_TOOLS = [
    {
        "name": "get_account_info",
        "description": "계정의 캐릭터 목록 및 최근 접속 기록을 조회합니다.",
        "parameters": {
            "account_id": {"type": "str", "description": "조회할 계정 ID"},
        },
    },
    {
        "name": "get_character_info",
        "description": "캐릭터의 정보를 조회합니다.",
        "parameters": {
            "char_name": {"type": "str", "description": "조회할 캐릭터 이름"},
        },
    },
    {
        "name": "get_character_item_usage",
        "description": "지정된 캐릭터가 사용한 아이템 로그를 조회합니다.",
        "parameters": {
            "char_name": {"type": "str", "description": "캐릭터 이름"},
            "item_name": {"type": "str", "description": "아이템 이름"},
            "start_date": {"type": "str", "description": "조회 시작일 (YYYY-MM-DD)"},
            "end_date": {"type": "str", "description": "조회 종료일 (YYYY-MM-DD)"},
        },
    },
]
ITEM_TOOLS = [
    {
        "name": "get_user_zeny_log",
        "description": "Inquires the '제니(Zeny)' usage log for the specified date of the specified user.",
        "parameters": {
            "user_id": {"type": "str", "description": "계정 ID 또는 캐릭터 이름"},
            "start_date": {"type": "str", "description": "조회 시작일 (YYYY-MM-DD)"},
            "end_date": {"type": "str", "description": "조회 종료일 (YYYY-MM-DD)"},
        },
    },
    {
        "name": "get_get_item_log",
        "description": "지정된 유저의 아이템 획득 로그를 조회합니다.",
        "parameters": {
            "user_id": {"type": "str", "description": "계정 ID 또는 캐릭터 이름"},
            "user_type": {
                "type": "str",
                "description": "'account_id' 또는 'char_name' 중 하나",
            },
            "item_name": {"type": "str", "description": "조회할 아이템 이름"},
            "start_date": {"type": "str", "description": "조회 시작일 (YYYY-MM-DD)"},
            "end_date": {"type": "str", "description": "조회 종료일 (YYYY-MM-DD)"},
        },
    },
    {
        "name": "get_use_item_log",
        "description": "지정된 유저의 아이템 사용 로그를 조회합니다.",
        "parameters": {
            "user_id": {"type": "str", "description": "계정 ID 또는 캐릭터 이름"},
            "user_type": {
                "type": "str",
                "description": "'account_id' 또는 'char_name' 중 하나",
            },
            "item_name": {"type": "str", "description": "조회할 아이템 이름"},
            "start_date": {"type": "str", "description": "조회 시작일 (YYYY-MM-DD)"},
            "end_date": {"type": "str", "description": "조회 종료일 (YYYY-MM-DD)"},
        },
    },
]
EVENT_TOOLS = [
    {
        "name": "get_event_item_usage",
        "description": "지정된 유저의 이벤트 아이템 사용 내역을 조회합니다.",
        "parameters": {
            "user_id": {"type": "str", "description": "계정 ID 또는 캐릭터 이름"},
            "user_type": {
                "type": "str",
                "description": "'account_id' 또는 'char_name' 중 하나",
            },
            "event_name": {"type": "str", "description": "이벤트 이름"},
            "start_date": {"type": "str", "description": "조회 시작일 (YYYY-MM-DD)"},
            "end_date": {"type": "str", "description": "조회 종료일 (YYYY-MM-DD)"},
        },
    }
]
SECURITY_TOOLS = [
    {
        "name": "get_login_log",
        "description": "유저의 로그인 기록을 조회합니다.",
        "parameters": {
            "account_id": {"type": "str", "description": "조회할 계정 ID"},
            "start_date": {"type": "str", "description": "조회 시작일 (YYYY-MM-DD)"},
            "end_date": {"type": "str", "description": "조회 종료일 (YYYY-MM-DD)"},
        },
    },
]
OTHER_TOOLS = [{}]
