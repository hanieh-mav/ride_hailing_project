from abc import ABC, abstractmethod

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
