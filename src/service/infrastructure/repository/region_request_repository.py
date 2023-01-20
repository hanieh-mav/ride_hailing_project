from datetime import datetime

from injector import inject

from src.service.core.service_app_service_contract.connection.idatabase_connection import IDatabaseConnection
from src.service.core.service_app_service_contract.repository.iregion_request_repository import IRegionRequestRepository
from src.service.core.service_model.region_request_model import RegionRequestModel


class RegionRequestRepository(IRegionRequestRepository):

    @inject
    def __init__(self, database_connection: IDatabaseConnection) -> None:
        self.__database_connection = database_connection

    def add(self, model: RegionRequestModel) -> None:
        with self.__database_connection.ms_sql_server_session(has_transaction=True) as session:
            session.add(model)

    def get_count_of_request_for_region_id_in_datetime_range(self, region_id: int, datetime_value: datetime) -> int:
        with self.__database_connection.ms_sql_server_session() as session:
            return session.query(RegionRequestModel).filter(RegionRequestModel.region_id == region_id).filter(
                RegionRequestModel.entry_date >= datetime_value).count()
