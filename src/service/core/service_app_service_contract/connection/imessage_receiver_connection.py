from abc import ABC, abstractmethod


class IMessageReceiver(ABC):

    @abstractmethod
    def receive(self) -> str:
        raise NotImplementedError
