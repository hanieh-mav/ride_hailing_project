from typing import Union

from abc import ABC, abstractmethod


class IRequestThresholdCoefficientService(ABC):

    @abstractmethod
    def add_request_threshold_coefficient(self, request_threshold: Union[int, None],
                                          price_coefficient: Union[int, float, None]):
        raise NotImplementedError

    @abstractmethod
    def update_request_threshold_coefficient(self, pk: str, request_threshold: Union[int, None],
                                             price_coefficient: Union[int, float, None]) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_request_threshold_coefficient_by_pk(self, pk: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_all_request_threshold_coefficient_list(self) -> list[dict]:
        raise NotImplementedError
