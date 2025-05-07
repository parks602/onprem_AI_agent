import pyodbc


def get_db_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=cs_test;"
        "Trusted_Connection=yes;"
    )
    return conn


def execute_query(query: str):
    # 쿼리 실행 함수
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    return cursor.fetchall()
