from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, URL
from sqlalchemy.orm import sessionmaker, Session

from src.service.config.runtime_config import RuntimeConfig
from src.service.core.service_app_service_contract.connection.idatabase_connection import IDatabaseConnection


class DatabaseConnection(IDatabaseConnection):

    def __init__(self) -> None:
        self.__engine: Engine = self.__create_engine()

    @staticmethod
    def __create_engine() -> Engine:
        url = URL.create(drivername=RuntimeConfig.DATABASE_DRIVER_NAME,
                         username=RuntimeConfig.DATABASE_USERNAME,
                         password=RuntimeConfig.DATABASE_PASSWORD, host=RuntimeConfig.DATABASE_HOST,
                         port=RuntimeConfig.DATABASE_PORT, database=RuntimeConfig.DATABASE_NAME)

        return create_engine(url, pool_size=RuntimeConfig.DATABASE_POOL_SIZE,
                             max_overflow=RuntimeConfig.DATABASE_MAX_OVERFLOW)

    def __session_maker(self) -> sessionmaker:
        return sessionmaker(self.__engine)

    def ms_sql_server_session(self, has_transaction: bool = None) -> Session:
        session_factory = self.__session_maker()
        return session_factory.begin() if has_transaction else session_factory()
