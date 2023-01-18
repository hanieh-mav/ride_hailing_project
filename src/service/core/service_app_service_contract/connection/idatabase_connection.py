from abc import ABC, abstractmethod

from sqlalchemy.orm import Session


class IDatabaseConnection(ABC):

    @abstractmethod
    def ms_sql_server_session(self, has_transaction: bool = None) -> Session:
        raise NotImplementedError
