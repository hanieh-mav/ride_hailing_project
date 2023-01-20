from abc import ABC, abstractmethod
from typing import Union

from src.service.core.service_model.region_model import RegionModel


class IRegionRepository(ABC):

    @abstractmethod
    def get_id_by_place_id(self, place_id: int) -> Union[int, None]:
        raise NotImplementedError

    @abstractmethod
    def add(self, model: RegionModel) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all_region_id_list(self) -> list[int]:
        raise NotImplementedError
