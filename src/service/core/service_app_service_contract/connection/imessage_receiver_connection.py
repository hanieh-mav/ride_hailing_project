from abc import ABC, abstractmethod


class IMessageReceiverConnection(ABC):

    @abstractmethod
    def receive(self) -> str:
        raise NotImplementedError
