from typing import Union

from injector import inject

from src.service.core.service_app_service_contract.connection.icache_connection import ICacheConnection
from src.service.core.service_app_service_contract.connection.idatabase_connection import IDatabaseConnection
from src.service.core.service_app_service_contract.repository.iregion_repository import IRegionRepository

from src.service.core.service_model.region_model import RegionModel


class RegionRepository(IRegionRepository):
    key_pattern: str = 'cache:region_id:{place_id}'

    @inject
    def __init__(self, database_connection: IDatabaseConnection, cache_connection: ICacheConnection) -> None:
        self.__database_connection = database_connection
        self.__cache_connection = cache_connection

    def add(self, model: RegionModel) -> None:
        with self.__database_connection.ms_sql_server_session(has_transaction=True) as session:
            session.add(model)
            self.__cache_region_id(model.id, model.place_id)

    def get_id_by_place_id(self, place_id: int) -> Union[int, None]:
        if cached_id := self.__get_cached_region_id(place_id):
            return cached_id
        with self.__database_connection.ms_sql_server_session() as session:
            if fetched_data := session.query(RegionModel.id).filter(RegionModel.place_id == place_id).one_or_none():
                region_id: int = fetched_data[0]
                self.__cache_region_id(region_id, place_id)
                return region_id

    def __get_cached_region_id(self, place_id: int) -> Union[int, None]:
        key = self.key_pattern.format(place_id=place_id)
        if data := self.__cache_connection.get_cached_data(key):
            return data

    def __cache_region_id(self, region_id: int, place_id: int):
        key = self.key_pattern.format(place_id=place_id)
        self.__cache_connection.cache_data(key, region_id)
