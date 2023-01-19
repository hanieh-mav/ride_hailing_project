from abc import ABC, abstractmethod
from typing import Union

from src.service.core.service_model.request_threshold_coefficient_model import RequestThresholdCoefficientModel


class IRequestThresholdCoefficientRepository(ABC):

    @abstractmethod
    def add(self, model: RequestThresholdCoefficientModel) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_model_by_pk(self, pk: int) -> RequestThresholdCoefficientModel:
        raise NotImplementedError

    @abstractmethod
    def update(self, model: RequestThresholdCoefficientModel) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all_model_list(self) -> list[RequestThresholdCoefficientModel]:
        raise NotImplementedError

    @abstractmethod
    def check_request_threshold_existence(self, request_threshold: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_price_coefficient_by_request_threshold(self, request_threshold: int) -> Union[int, None, float]:
        raise NotImplementedError
