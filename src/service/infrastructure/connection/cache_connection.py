from typing import  Union

import redis
import ujson

from src.service.config.runtime_config import RuntimeConfig
from src.service.core.service_app_service_contract.connection.icache_connection import ICacheConnection


class CacheConnection(ICacheConnection):

    def __init__(self):
        self.__connection = redis.Redis(host=RuntimeConfig.CACHE_HOST, port=RuntimeConfig.CACHE_PORT,
                                        db=RuntimeConfig.CACHE_DB_NUMBER)

    def cache_data(self, key: str, value: Union[dict, list[dict]]) -> None:
        data: str = ujson.dumps(value)
        self.__connection.set(key, data)

    def get_cached_data(self, key: str) -> Union[None, dict, list[dict]]:
        if result := self.__connection.get(key):
            return ujson.loads(result)

    def remove_cached_data(self, key: str) -> None:
        self.__connection.delete(key)
