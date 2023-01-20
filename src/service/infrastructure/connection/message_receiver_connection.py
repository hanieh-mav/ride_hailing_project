import json
import logging

from confluent_kafka import Consumer

from src.service.config.runtime_config import RuntimeConfig
from src.service.core.service_app_service_contract.connection.imessage_receiver_connection import \
    IMessageReceiverConnection


class MessageReceiverConnection(IMessageReceiverConnection):

    def __init__(self) -> None:
        self.__broker_list: list[str] = RuntimeConfig.KAFKA_BROKERS_LIST
        self.__kafka_user_name: str = RuntimeConfig.KAFKA_USER_NAME
        self.__kafka_password: str = RuntimeConfig.KAFKA_PASSWORD
        self.__kafka_cert_pem: str = RuntimeConfig.KAFKA_CERT_PEM
        self.__kafka_session_timeout_ms: int = RuntimeConfig.KAFKA_SESSION_TIMEOUT_MS
        self.__kafka_auto_offset_reset: str = RuntimeConfig.KAFKA_AUTO_OFFSET_RESET
        self.__kafka_topic_list: list[str] = RuntimeConfig.KAFKA_TOPIC_LIST
        self.__kafka_consumer_group_id: str = RuntimeConfig.KAFKA_CONSUMER_GROUP_ID
        self.__client: Consumer = self.__get_client()
        self.__client.subscribe(self.__kafka_topic_list)

    def __get_client(self) -> Consumer:
        broker_list_csv = ",".join(self.__broker_list)
        config = {'bootstrap.servers': broker_list_csv, 'group.id': self.__kafka_consumer_group_id,
                  'session.timeout.ms': self.__kafka_session_timeout_ms,
                  'auto.offset.reset': self.__kafka_auto_offset_reset}

        if self.__kafka_user_name and self.__kafka_password and self.__kafka_cert_pem:
            config |= {'sasl.username': self.__kafka_user_name, 'sasl.password': self.__kafka_password,
                       'security.protocol': 'SASL_SSL', 'sasl.mechanisms': 'SCRAM-SHA-512',
                       'ssl.endpoint.identification.algorithm': 'none', 'ssl.ca.pem': self.__kafka_cert_pem}

        return Consumer(config)

    def receive(self) -> str:
        try:
            if message := self.__client.poll():
                return json.loads(message.value().decode('utf8'))
        except Exception as error:
            logging.exception(f"Consumer error: {error}")
