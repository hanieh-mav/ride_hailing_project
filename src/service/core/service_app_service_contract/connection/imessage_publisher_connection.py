from abc import ABC, abstractmethod


class IMessagePublisherConnection(ABC):

    @abstractmethod
    def publish(self, message: str) -> None:
        raise NotImplementedError
