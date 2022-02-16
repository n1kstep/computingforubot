import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
try:
    # Подключение к существующей базе данных
    conn = psycopg2.connect(database='fn1131_2021',
                            user="student",
                            password="bmstu",
                            host="195.19.32.74",
                            port="5432")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    # Курсор для выполнения операций с базой данных
    cursor = conn.cursor()
except:
    pass


def get_cursor():
    return cursor


def insert_or_update(user_id: int, inp_query: str, suc: bool, res: str):
    from datetime import datetime, timezone

    dt = datetime.now(timezone.utc)
    statement = f"INSERT INTO tg_data.computingforu_data (user_id, query_date, input_query, success, result) " \
                f"VALUES ({user_id}, '{dt}', '{inp_query}', {suc}, '{res}')"
    cursor.execute(statement)
    cursor.connection.commit()


def get_queries(user_id: int):
    statement = f"SELECT query_date, input_query, result from tg_data.computingforu_data WHERE user_id = {user_id} " \
                f"ORDER BY query_date DESC LIMIT 5"
    cursor.execute(statement)
    result = [f"{i+1}) {t[1]} -> {t[2]} ({str(t[0])[:-10]})" for i, t in enumerate(cursor.fetchall())]
    result = '\n---\n'.join(result)
    return result


# def _init_db():
#     """Инициализирует БД"""
#     with open(".sql", "r") as f:
#         sql = f.read()
#     cursor.executescript(sql)
#     conn.commit()


# def check_db_exists():
#     """Проверяет, инициализирована ли БД, если нет — инициализирует"""
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='youtube'")
#     table_exists = cursor.fetchall()
#     if table_exists:
#         return
#     _init_db()
#
#
# check_db_exists()
