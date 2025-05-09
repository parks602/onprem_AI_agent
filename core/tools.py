function_registry = {}


def register_tool(fn):
    function_registry[fn.__name__] = fn
    return fn


# PAYMENT_TOOLS
@register_tool
def user_payment_history(account_id):
    print(f"[user_payment_history] account_id={account_id}")
    return {"status": "success", "payments": []}


@register_tool
def user_payment_history_by_date(account_id, start_date, end_date):
    print(
        f"[user_payment_history_by_date] account_id={account_id}, start={start_date}, end={end_date}"
    )
    return {"status": "success", "payments": []}


@register_tool
def user_refund_history(account_id):
    print(f"[user_refund_history] account_id={account_id}")
    return {"status": "success", "refunds": []}


# ACCOUNT_TOOLS
@register_tool
def get_account_info(account_id):
    print(f"[get_account_info] account_id={account_id}")
    return {"status": "success", "characters": [], "last_login": "2023-01-01"}


@register_tool
def get_character_info(char_name):
    print(f"[get_character_info] char_name={char_name}")
    return {"status": "success", "level": 1, "class": "warrior", "items": []}


@register_tool
def get_character_item_usage(char_name, item_name, start_date, end_date):
    print(
        f"[get_character_item_usage] char_name={char_name}, item_name={item_name}, start={start_date}, end={end_date}"
    )
    return {"status": "success", "usage_logs": []}


# ITEM_TOOLS
@register_tool
def get_get_item_log(user_id, user_type, item_name, start_date, end_date):
    print(
        f"[get_get_item_log] user_id={user_id}, user_type={user_type}, item_name={item_name}, start={start_date}, end={end_date}"
    )
    return {"status": "success", "logs": []}


@register_tool
def get_use_item_log(user_id, user_type, item_name, start_date, end_date):
    print(
        f"[get_use_item_log] user_id={user_id}, user_type={user_type}, item_name={item_name}, start={start_date}, end={end_date}"
    )
    return {"status": "success", "logs": []}


@register_tool
def get_user_zeny_log(user_id, start_date, end_date):
    query = f"select price from itemlog where srcAccountID = {user_id}, logtime"
    result = """
    srcAccountID | logtime               | price       | action
    user001      | 2025-03-15 16:15:00   | 2,500,000   |   3
    user001      | 2025-03-15 16:15:10   | 3,000,000   |   6
    """
    return result


# EVENT_TOOLS
@register_tool
def get_event_item_usage(user_id, user_type, event_name, start_date, end_date):
    print(
        f"[get_event_item_usage] user_id={user_id}, user_type={user_type}, event_name={event_name}, start={start_date}, end={end_date}"
    )
    return {"status": "success", "event_logs": []}


# SECURITY_TOOLS
@register_tool
def get_login_log(account_id, start_date, end_date):
    print(
        f"[get_login_log] account_id={account_id}, start={start_date}, end={end_date}"
    )
    return {"status": "success", "logins": []}
