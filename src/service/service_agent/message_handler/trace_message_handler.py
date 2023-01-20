import logging

from injector import inject

from src.service.core.service_app_service_contract.connection.imessage_receiver_connection import \
    IMessageReceiverConnection
from src.service.core.service_app_service_contract.message_handler.itrace_message_handler import ITraceMessageHandler
from src.service.core.service_app_service_contract.service_app_service.iregion_request_service import \
    IRegionRequestService


class TraceMessageHandler(ITraceMessageHandler):


    @inject
    def __init__(self, message_receiver: IMessageReceiverConnection, service: IRegionRequestService) -> None:
        self.__message_receiver = message_receiver
        self.__service = service

    def trace_message(self) -> None:
        while True:
            try:
                if message := self.__message_receiver.receive():
                    self.__service.save_request_for_region(message)
            except Exception as error:
                logging.exception(error)
