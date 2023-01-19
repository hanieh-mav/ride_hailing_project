from abc import ABC, abstractmethod
from typing import Any, Union


class ICacheConnection(ABC):

    @abstractmethod
    def cache_data(self, key: str, value: Union[dict, list[dict], int]) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_cached_data(self, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_cached_data(self, key: str) -> Union[None, dict, list[dict], int]:
        raise NotImplementedError
