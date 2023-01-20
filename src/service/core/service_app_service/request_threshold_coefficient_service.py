from typing import Union

from injector import inject

from src.service.core.service_app_service_contract.repository.irequest_threshold_coefficient_repository import \
    IRequestThresholdCoefficientRepository
from src.service.core.service_app_service_contract.service_app_service.irequest_threshold_coefficient_service import \
    IRequestThresholdCoefficientService
from src.service.core.service_model.request_threshold_coefficient_model import RequestThresholdCoefficientModel


class RequestThresholdCoefficientService(IRequestThresholdCoefficientService):

    @inject
    def __init__(self, repository: IRequestThresholdCoefficientRepository) -> None:
        self.__repository = repository

    def add_request_threshold_coefficient(self, request_threshold: Union[int, None],
                                          price_coefficient: Union[int, float, None]):
        if self.__repository.check_request_threshold_existence(request_threshold):
            raise ValueError('This request threshold already exist')
        model = \
            RequestThresholdCoefficientModel(request_threshold=request_threshold, price_coefficient=price_coefficient)
        self.__repository.add(model)

    def update_request_threshold_coefficient(self, pk: str, request_threshold: Union[int, None],
                                             price_coefficient: Union[int, float, None]) -> None:
        if model := self.__repository.get_model_by_pk(int(pk)):
            if request_threshold:
                model.request_threshold = request_threshold
            if price_coefficient:
                model.price_coefficient = price_coefficient
            self.__repository.update(model)

    def get_request_threshold_coefficient_by_pk(self, pk: str) -> dict:
        int_pk: int = int(pk)
        if model := self.__repository.get_model_by_pk(int_pk):
            return model.make_dict_data()

    def get_all_request_threshold_coefficient_list(self) -> list[dict]:
        model_list: list[RequestThresholdCoefficientModel] = self.__repository.get_all_model_list()
        return [model.make_dict_data() for model in model_list]
