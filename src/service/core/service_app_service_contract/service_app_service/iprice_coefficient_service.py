from abc import ABC, abstractmethod
from typing import Union


class IPriceCoefficientService(ABC):

    @abstractmethod
    def get_price_coefficient(self, latitude: float, longitude: float) -> Union[int, float, None]:
        raise NotImplementedError
