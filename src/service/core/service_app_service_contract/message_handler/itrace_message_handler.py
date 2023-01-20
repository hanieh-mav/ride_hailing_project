from abc import ABC, abstractmethod


class ITraceMessageHandler(ABC):

    @abstractmethod
    def trace_message(self) -> None:
        raise NotImplementedError
