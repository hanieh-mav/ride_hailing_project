from abc import ABC, abstractmethod


class IRegionRequestService(ABC):

    @abstractmethod
    def save_request_for_region(self, place_id: str) -> None:
        raise NotImplementedError
