from pytest import fixture
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from src.service.config.base_config import BaseConfig
from src.service.config.runtime_config import RuntimeConfig
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

from src.service.core.service_model.base import Base

BaseConfig.configure(RuntimeConfig)

from typing import Union

import redis
import ujson

from src.service.config.runtime_config import RuntimeConfig
from src.service.core.service_app_service_contract.connection.icache_connection import ICacheConnection


class CacheConnection:

    def __init__(self):
        self.connection = redis.Redis(host=RuntimeConfig.CACHE_HOST, port=RuntimeConfig.CACHE_PORT,
                                      db=4)

    def cache_data(self, key, value) -> None:
        data: str = ujson.dumps(value)
        self.connection.set(key, data)

    def get_cached_data(self, key):
        if result := self.connection.get(key):
            return ujson.loads(result)

    def remove_cached_data(self, key) -> None:
        self.connection.delete(key)


class DatabaseConnection:

    def __init__(self) -> None:
        self.engine = self.__create_engine()

    @staticmethod
    def __create_engine():
        connection_string: str = f'postgresql+psycopg2://{RuntimeConfig.DATABASE_USERNAME}:{RuntimeConfig.DATABASE_PASSWORD}@{RuntimeConfig.DATABASE_HOST}:{RuntimeConfig.DATABASE_PORT}/Test'

        return create_engine(connection_string)

    def __session_maker(self):
        return sessionmaker(self.engine)

    def ms_sql_server_session(self, has_transaction: bool = None):
        session_factory = self.__session_maker()
        return session_factory.begin() if has_transaction else session_factory()



@fixture()
def create_database_and_delete_after_test():
    database_connection = DatabaseConnection()
    engine = database_connection.engine
    if not database_exists(engine.url):
        create_database(engine.url)

    connection = engine.connect()
    schema_query = 'create schema "ride.hailing"'
    connection.execute(schema_query)
    Base.metadata.create_all(engine)
    yield database_connection, connection
    drop_database(engine.url)
    connection.close()


@fixture()
def create_cache_connection_and_delete_after_test():
    connection = CacheConnection()
    yield connection
    connection.connection.flushdb()
