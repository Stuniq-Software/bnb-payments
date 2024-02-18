import redis
import os
from typing import Optional

connection: Optional[redis.Redis] = None


def initialize_connection() -> redis.Redis:
    global connection
    connection = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=os.getenv("REDIS_PORT", "6379"),
        db=os.getenv("REDIS_DB", "0"),
    )
    print("Redis connection initialized")
    return connection


class RedisSession:
    _connection: redis.Redis

    def __init__(self):
        if connection is None:
            initialize_connection()
        self._connection = connection

    def set(self, key: str, value: str | bytes, expire: int = 0) -> bool:
        try:
            self._connection.set(key, value, ex=expire)
            return True
        except Exception as e:
            print(e)
            return False

    def get(self, key: str) -> Optional[str | bytes]:
        try:
            return self._connection.get(key)
        except Exception as e:
            print(e)
            return None

    def delete(self, key: str) -> bool:
        try:
            self._connection.delete(key)
            return True
        except Exception as e:
            print(e)
            return False
