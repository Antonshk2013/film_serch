import logging
from orm import MySQLConnection
from typing import Callable
from functools import wraps
from logger_config import logger


logger = logging.getLogger(__name__)


def log_function_call(level=logging.INFO):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.log(level, f"Вызов {func.__name__} с args={args}, kwargs={kwargs}")
            try:
                result = func(*args, **kwargs)
                logger.log(level, f"{func.__name__} вернула {result}")
                return result
            except Exception as e:
                logger.exception(f"Ошибка в {func.__name__}: {e}")
                raise
        return wrapper
    return decorator


def serialeizer_many_to_json(columns_name, row_data):
    colums_clean_name = [name[0] for name in columns_name]
    result = [dict(zip(colums_clean_name, row)) for row in row_data]
    return result


def serialeizer_one_to_json(columns_name, row_data):
    colums_clean_name = [name[0] for name in columns_name]
    result = dict(zip(colums_clean_name, row_data[0]))
    return result


def serialeizer_many_to_choice(columns_name, row_data):
    return [(str(row[0]), str(row[1])) for row in row_data]


def serialeizer_to_list(columns_name, row_data):
    return [row[1] for row in row_data]


def prepare_like(value:str):
    return f"{value.upper()}%"

@log_function_call()
def select_from_db(q: str, serialeizer_func: Callable = None):
    with MySQLConnection() as conn:
            cursor = conn.cursor
            cursor.execute(q)
            results = serialeizer_func(cursor.description, cursor.fetchall())
    return results


def insert_to_db(q: str):
    with MySQLConnection() as conn:
            cursor = conn.cursor
            cursor.execute(q)
            conn.commit()
    return True