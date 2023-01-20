from abc import ABC, abstractmethod
from typing import Union


class IRegionPriceCoefficientRepository(ABC):

    @abstractmethod
    def get_price_coefficient_by_region_id(self, region_id: int) -> Union[int, float, None]:
        raise NotImplementedError
