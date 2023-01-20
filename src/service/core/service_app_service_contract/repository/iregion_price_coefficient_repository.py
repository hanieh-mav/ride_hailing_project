from abc import ABC, abstractmethod
from typing import Union

from src.service.core.service_model import RegionPriceCoefficientModel


class IRegionPriceCoefficientRepository(ABC):

    @abstractmethod
    def get_price_coefficient_by_region_id(self, region_id: int) -> Union[int, float, None]:
        raise NotImplementedError

    @abstractmethod
    def add(self, model: RegionPriceCoefficientModel) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, model: RegionPriceCoefficientModel) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_region_id(self, region_id: int) -> Union[None, RegionPriceCoefficientModel]:
        raise NotImplementedError
