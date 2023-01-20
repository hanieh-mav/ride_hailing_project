from injector import inject

from src.service.core.service_app_service_contract.repository.iregion_repository import IRegionRepository
from src.service.core.service_app_service_contract.repository.iregion_request_repository import IRegionRequestRepository
from src.service.core.service_app_service_contract.service_app_service.iregion_request_service import \
    IRegionRequestService
from src.service.core.service_model.region_model import RegionModel
from src.service.core.service_model.region_request_model import RegionRequestModel


class RegionRequestService(IRegionRequestService):

    @inject
    def __init__(self, region_repository: IRegionRepository,
                 request_region_repository: IRegionRequestRepository) -> None:
        self.__region_repository = region_repository
        self.__request_region_repository = request_region_repository

    def save_request_for_region(self, place_id: str) -> None:
        int_place_id: int = int(place_id)
        if region_id := self.__region_repository.get_id_by_place_id(int_place_id):
            self.__add_region(int_place_id)
        else:
            self.__add_request_for_region(region_id)

    def __add_request_for_region(self, region_id: int) -> None:
        model: RegionRequestModel = RegionRequestModel(region_id=region_id)
        self.__request_region_repository.add(model)

    def __add_region(self, place_id: int):
        region_model: RegionModel = RegionModel(place_id=place_id)
        region_request_model: RegionRequestModel = RegionRequestModel()
        region_model.region_request.append(region_request_model)
        self.__region_repository.add(region_model)
