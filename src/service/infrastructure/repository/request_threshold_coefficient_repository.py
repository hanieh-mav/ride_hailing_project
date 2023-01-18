from typing import Union

from injector import inject

from src.service.core.service_app_service_contract.connection.icache_connection import ICacheConnection
from src.service.core.service_app_service_contract.connection.idatabase_connection import IDatabaseConnection
from src.service.core.service_app_service_contract.repository.irequest_threshold_coefficient_repository import \
    IRequestThresholdCoefficientRepository
from src.service.core.service_model.request_threshold_coefficient_model import RequestThresholdCoefficientModel


class RequestThresholdCoefficientRepository(IRequestThresholdCoefficientRepository):
    key_pattern: str = 'cache:request_threshold_coefficient:{pk}'
    key_pattern_list: str = 'cache:request_threshold_coefficient_list'

    @inject
    def __init__(self, database_connection: IDatabaseConnection, cache_connection: ICacheConnection) -> None:
        self.__database_connection = database_connection
        self.__cache_connection = cache_connection

    def add(self, model: RequestThresholdCoefficientModel) -> None:
        with self.__database_connection.ms_sql_server_session(has_transaction=True) as session:
            session.add(model)

    def update(self, model: RequestThresholdCoefficientModel) -> None:
        with self.__database_connection.ms_sql_server_session(has_transaction=True) as session:
            session.query(RequestThresholdCoefficientModel).filter(
                RequestThresholdCoefficientModel.id == model.id).update(
                {RequestThresholdCoefficientModel.request_threshold: model.request_threshold,
                 RequestThresholdCoefficientModel.price_coefficient: model.price_coefficient}
            )
            self.__remove_cached_model(model.id)

    def get_model_by_pk(self, pk: int) -> RequestThresholdCoefficientModel:
        if cached_model := self.__get_cached_model(pk):
            return cached_model
        with self.__database_connection.ms_sql_server_session() as session:
            model: RequestThresholdCoefficientModel = \
                session.query(RequestThresholdCoefficientModel).filter(RequestThresholdCoefficientModel.id == pk).one()
            self.__cache_model(model)
            return model

    def get_all_model_list(self) -> list[RequestThresholdCoefficientModel]:
        if cached_model_list := self.__get_cached_model_list():
            return cached_model_list
        with self.__database_connection.ms_sql_server_session() as session:
            model_list: list[RequestThresholdCoefficientModel] = session.query(RequestThresholdCoefficientModel).all()
            self.__cache_model_list(model_list)
            return model_list

    def __remove_cached_model(self, pk: int) -> None:
        key: str = self.key_pattern.format(pk=pk)
        self.__cache_connection.remove_cached_data(key)

    def __get_cached_model(self, pk: int) -> Union[None, RequestThresholdCoefficientModel]:
        key = self.key_pattern.format(pk=pk)
        if data := self.__cache_connection.get_cached_data(key):
            return RequestThresholdCoefficientModel(**data)

    def __cache_model(self, model: RequestThresholdCoefficientModel):
        key = self.key_pattern.format(pk=model.id)
        self.__cache_connection.cache_data(key, model.make_dict_data())

    def __cache_model_list(self, model_list: list[RequestThresholdCoefficientModel]):
        model_dict_list: list[dict] = [model.make_dict_data() for model in model_list]
        self.__cache_connection.cache_data(self.key_pattern_list, model_dict_list)

    def __get_cached_model_list(self) -> list[RequestThresholdCoefficientModel]:
        if data_list := self.__cache_connection.get_cached_data(self.key_pattern_list):
            return [RequestThresholdCoefficientModel(**data) for data in data_list]
