from injector import inject

from src.service.core.service_app_service_contract.repository.iregion_price_coefficient_repository import \
    IRegionPriceCoefficientRepository
from src.service.core.service_app_service_contract.repository.iregion_repository import IRegionRepository
from src.service.core.service_app_service_contract.repository.iregion_request_repository import IRegionRequestRepository
from src.service.core.service_app_service_contract.repository.irequest_threshold_coefficient_repository import \
    IRequestThresholdCoefficientRepository
from src.service.core.service_app_service_contract.service_app_service.iregion_price_coefficient_calculator_service import \
    IRegionPriceCoefficientCalculatorService
from datetime import datetime, timedelta, timezone

from src.service.core.service_model.region_price_coefficient_model import RegionPriceCoefficientModel


class RegionPriceCoefficientCalculatorService(IRegionPriceCoefficientCalculatorService):

    @inject
    def __init__(self, region_repository: IRegionRepository,
                 request_region_repository: IRegionRequestRepository,
                 price_coefficient_repository: IRegionPriceCoefficientRepository,
                 request_threshold_coefficient_repository: IRequestThresholdCoefficientRepository) -> None:
        self.__region_repository = region_repository
        self.__request_region_repository = request_region_repository
        self.__price_coefficient_repository = price_coefficient_repository
        self.__request_threshold_coefficient_repository = request_threshold_coefficient_repository

    def calculate_price_coefficient(self) -> None:
        ten_minute_before_now_datetime: datetime = datetime.now(timezone.utc) - timedelta(minutes=10)
        if region_id_list := self.__region_repository.get_all_region_id_list():
            for region_id in region_id_list:
                self.__calculate_price_coefficient_for_region(region_id, ten_minute_before_now_datetime)

    def __calculate_price_coefficient_for_region(self, region_id: int, datetime_variable: datetime):
        count_of_request: int = self.__request_region_repository.get_count_of_request_for_region_id_in_datetime_range(
            region_id, datetime_variable)
        if price_coefficient := \
                self.__request_threshold_coefficient_repository.get_price_coefficient_by_request_threshold(
                    count_of_request):
            if exist_model := self.__price_coefficient_repository.get_by_region_id(region_id):
                exist_model.price_coefficient = price_coefficient
                self.__price_coefficient_repository.update(exist_model)
            else:
                model: RegionPriceCoefficientModel = RegionPriceCoefficientModel(region_id=region_id,
                                                                                 price_coefficient=price_coefficient)
                self.__price_coefficient_repository.add(model)
