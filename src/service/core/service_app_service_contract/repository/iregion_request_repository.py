from abc import ABC, abstractmethod

from src.service.core.service_model.region_request_model import RegionRequestModel


class IRegionRequestRepository(ABC):

    @abstractmethod
    def add(self, model: RegionRequestModel) -> None:
        raise NotImplementedError
