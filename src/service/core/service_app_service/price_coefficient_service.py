from typing import Union

from geopy import Nominatim
from injector import inject

from src.service.core.service_app_service_contract.connection.imessage_publisher_connection import \
    IMessagePublisherConnection
from src.service.core.service_app_service_contract.repository.iregion_price_coefficient_repository import \
    IRegionPriceCoefficientRepository
from src.service.core.service_app_service_contract.repository.irequest_threshold_coefficient_repository import \
    IRequestThresholdCoefficientRepository
from src.service.core.service_app_service_contract.service_app_service.iprice_coefficient_service import \
    IPriceCoefficientService


class PriceCoefficientService(IPriceCoefficientService):

    @inject
    def __init__(self, message_publisher: IMessagePublisherConnection,
                 region_price_coefficient_repository: IRegionPriceCoefficientRepository,
                 request_threshold_coefficient_repository: IRequestThresholdCoefficientRepository) -> None:
        self.__geolocator = Nominatim(user_agent="snapp_app")
        self.__message_publisher = message_publisher
        self.__region_price_coefficient_repository = region_price_coefficient_repository
        self.__request_threshold_coefficient_repository = request_threshold_coefficient_repository

    def get_price_coefficient(self, latitude: float, longitude: float) -> Union[int, float, None]:
        region_id: int = self.__get_region_id(latitude, longitude)
        self.__message_publisher.publish(str(region_id))
        return self.__get_price_coefficient_by_region_id(region_id)

    def __get_region_id(self, latitude: float, longitude: float) -> int:
        if address := self.__geolocator.reverse((str(latitude), str(longitude)),
                                                language='en', exactly_one=True):
            if address.raw['address'].get('city') != 'Tehran':
                raise ValueError('This data is not for tehran')

            return address.raw.get('place_id')

    def __get_price_coefficient_by_region_id(self, region_id: int) -> Union[int, float, None]:
        if price_coefficient := self.__region_price_coefficient_repository.get_price_coefficient_by_region_id(
                region_id):
            return price_coefficient
        return self.__request_threshold_coefficient_repository.get_price_coefficient_by_request_threshold(0)
