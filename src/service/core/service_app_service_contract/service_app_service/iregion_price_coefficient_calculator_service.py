from abc import ABC, abstractmethod


class IRegionPriceCoefficientCalculatorService(ABC):

    @abstractmethod
    def calculate_price_coefficient(self) -> None:
        raise NotImplementedError
