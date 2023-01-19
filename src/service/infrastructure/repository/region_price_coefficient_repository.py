from typing import Union

from injector import inject

from src.service.core.service_app_service_contract.connection.icache_connection import ICacheConnection
from src.service.core.service_app_service_contract.connection.idatabase_connection import IDatabaseConnection
from src.service.core.service_app_service_contract.repository.iregion_price_coefficient_repository import \
    IRegionPriceCoefficientRepository
from src.service.core.service_model.region_model import RegionModel
from src.service.core.service_model.region_price_coefficient_model import RegionPriceCoefficientModel


class RegionPriceCoefficientRepository(IRegionPriceCoefficientRepository):
    key_pattern: str = 'cache:price_coefficient:{region_id}'

    @inject
    def __init__(self, database_connection: IDatabaseConnection, cache_connection: ICacheConnection) -> None:
        self.__database_connection = database_connection
        self.__cache_connection = cache_connection

    def get_price_coefficient_by_region_id(self, region_id: int) -> Union[int, float, None]:
        if cached_price_coefficient := self.__get_cached_price_coefficient(region_id):
            return cached_price_coefficient
        with self.__database_connection.ms_sql_server_session() as session:
            if model := \
                    session.query(RegionPriceCoefficientModel).join(RegionModel).filter(
                        RegionModel.place_id == region_id).one_or_none():
                price_coefficient: int = model.price_coefficient
                self.__cache_price_coefficient(region_id, price_coefficient)
                return price_coefficient

    def __get_cached_price_coefficient(self, region_id: int) -> int:
        key = self.key_pattern.format(region_id=region_id)
        if data := self.__cache_connection.get_cached_data(key):
            return data

    def __cache_price_coefficient(self, region_id: int, price_coefficient: int):
        key = self.key_pattern.format(region_id=region_id)
        self.__cache_connection.cache_data(key, price_coefficient)
