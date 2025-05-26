import logging
import os
import mysql.connector
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logger.info("Таблицы и колонки проинициализированны")

load_dotenv()
PER_PAGE = 10


class MySQLConnection:

    dbconfig = {
        'host': os.getenv('MYSQL_HOST'),
        'user': os.getenv('MYSQL_USER'),
        'password': os.getenv('MYSQL_PASSWORD'),  # пароль пользователя, не root
        'database': os.getenv('MYSQL_DATABASE'),
        'port': int(os.getenv('MYSQL_PORT')),
    }
    def __init__(self):
        self.config = MySQLConnection.dbconfig
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor(buffered=True)  # buffered защищает от "Unread result"
            return self
        except Exception as e:
            print(f"Ошибка подключения к MySQL: {e}")
            # current_app.logger.error()
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            try:
                self.cursor.close()
            except Exception as e:
                print(f" {e.__class__.__name__}: {e}")
                # current_app.logger.error(f" {e.__class__.__name__}: {e}")
        if self.connection:
            try:
                self.connection.close()
            except Exception as e:
                print(f" {e.__class__.__name__}: {e}")
                # current_app.logger.error(f" {e.__class__.__name__}: {e}")


    def fetchall(self) -> list:
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def commit(self):
        self.connection.commit()

    def execute(self, query: str, params: tuple = None):
        try:
            self.cursor.execute(query, params or ())
            # current_app.logger.info(query)
        except Exception as e:
            print(f"{e.__class__.__name__}: {e}")
            # current_app.logger.exception(f"{e.__class__.__name__}: {e}")
            raise


class Table:
    '''
    Class Table for table description
    '''
    def __init__(self, table_name):
        self.table_name = table_name


    def __str__(self):
        return self.table_name

    def get_column(self):
        with MySQLConnection() as my_connect:
            my_connect.execute(f'DESCRIBE {self.table_name};')
        return [str(f"{self.table_name}.{colum[0]}") for colum in my_connect.cursor.fetchall()]

    def get_describe(self):
        with MySQLConnection() as my_connect:
            my_connect.execute(f'DESCRIBE {self.table_name};')
        return my_connect.cursor.fetchall()

    def count_rows(self):
        with MySQLConnection() as my_connect:
            my_connect.execute(f'SELECT COUNT(*) FROM {self.table_name}')
        return int(my_connect.cursor.fetchone()[0])


class Query:
    def __init__(self, table):
        self.table = table
        self.fields = ["*"]
        self.joins = []
        self.filters = []
        self.params = []
        self.limit = None
        self.offset = None
        self.ordering = []
        self.distinct = False

    def select(self, fields):
        if fields:
            print(fields)
            self.fields = [field for field in fields]
        return self

    def join(self, table_class, on_from, on_too, join_type="INNER"):
        self.joins.append({
            "type": join_type,
            "table": table_class,
            "on_from": on_from,
            "on_too": on_too
        })
        return self

    def filter(self, colum: str, compare: str, value):
        compares = ['>', '<', '=', '!=', '<>', '>=', '<=', 'like']
        if compare not in compares:
            raise ValueError("Invalid compare operator")
        condition = f"{colum} {compare} '{value}'"
        self.filters.append(condition)
        return self

    def set_distinct(self):
        self.distinct=True
        return self

    def set_order(self, column, direction="ASC"):
        direction = direction.upper()
        if direction not in ("ASC", "DESC"):
            raise ValueError("Ordering must be 'ASC' or 'DESC'")
        self.ordering.append((column, direction))
        return self

    def set_limit(self, limit: int):
        self.limit = limit
        return self

    def set_offset(self, page: int):
        self.offset = (page - 1) * PER_PAGE
        return self

    def build(self):
        query = f"SELECT "

        if self.distinct:
            query += "DISTINCT "

        query += f"{', '.join(self.fields)} FROM {self.table}"

        if self.joins:
            for join in self.joins:
                query += f" {join['type']} JOIN {join['table']} ON {join['on_from']} = {join['on_too']}"

        if self.filters:
            query += " WHERE " + " AND ".join(self.filters)

        if self.ordering:
            ordering_clauses = [f"{col} {direction}" for col, direction in self.ordering]
            query += " ORDER BY " + ", ".join(ordering_clauses)

        if self.limit is not None:
            query += f" LIMIT {self.limit}"

        if self.offset is not None:
            query += f" OFFSET {self.offset}"

        return query