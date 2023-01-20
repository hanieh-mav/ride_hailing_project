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
