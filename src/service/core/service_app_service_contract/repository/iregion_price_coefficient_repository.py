from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Union

from sqlalchemy import Column, DateTime, Integer, Float, ForeignKey

from src.service.core.service_model import Base
from src.service.core.service_model.region_model import RegionModel


class IRegionPriceCoefficientRepository(ABC):

    @abstractmethod
    def get_price_coefficient_by_region_id(self, region_id: int) -> Union[int, float, None]:
        raise NotImplementedError
