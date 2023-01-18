from abc import ABC, abstractmethod


class ICacheConnection(ABC):

    @abstractmethod
    def get_client(self):
        raise NotImplementedError
