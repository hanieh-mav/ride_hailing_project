from abc import ABC, abstractmethod
from datetime import datetime

from src.service.core.service_model.region_request_model import RegionRequestModel


class IRegionRequestRepository(ABC):

    @abstractmethod
    def add(self, model: RegionRequestModel) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_count_of_request_for_region_id_in_datetime_range(self, region_id: int, datetime_value: datetime) -> int:
        raise NotImplementedError
