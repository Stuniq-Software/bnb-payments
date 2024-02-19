import psycopg2
import psycopg2.extensions
import os
from typing import Optional

connection: Optional[psycopg2.extensions.connection] = None
cursor: Optional[psycopg2.extensions.cursor] = None


def initialize_connection() -> tuple[psycopg2.extensions.connection, psycopg2.extensions.cursor]:
    global connection, cursor
    connection = psycopg2.connect(
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "postgres")
    )
    cursor = connection.cursor()
    return connection, cursor


class Database:
    _connection: psycopg2.extensions.connection
    _cursor: psycopg2.extensions.cursor

    def __init__(self):
        if connection is None:
            initialize_connection()
        self._connection = connection
        self._cursor = cursor

    def get_cursor(self):
        if self._cursor is None:
            self._cursor = self._connection.cursor()
        return self._cursor

    def execute_query(self, query: str, params: tuple = None, auto_commit=False) -> tuple[bool, Optional[str]]:
        try:
            assert self._connection is not None, "Connection is not initialized"
            assert self._cursor is not None, "Cursor is not initialized"
            self._cursor.execute(query, params)
            if auto_commit:
                self._connection.commit()
            return True, None
        except AssertionError as e:
            print(e)
            return False, str(e)
        except Exception as e:
            print(e)
            self._connection.rollback()
            return False, str(e)

    def commit(self):
        self._connection.commit()

    def rollback(self):
        self._connection.rollback()

    def close(self):
        self._cursor.close()
        self._connection.close()

        global connection, cursor
        connection = None
        cursor = None
