from json import JSONEncoder

from confluent_kafka import Producer

from src.service.config.runtime_config import RuntimeConfig
from src.service.core.service_app_service_contract.connection.imessage_publisher_connection import \
    IMessagePublisherConnection


class MessagePublisherConnection(IMessagePublisherConnection):

    def __init__(self) -> None:
        self.__broker_list: list[str] = RuntimeConfig.KAFKA_BROKERS_LIST
        self.__kafka_user_name: str = RuntimeConfig.KAFKA_USER_NAME
        self.__kafka_password: str = RuntimeConfig.KAFKA_PASSWORD
        self.__kafka_cert_pem: str = RuntimeConfig.KAFKA_CERT_PEM
        self.__kafka_topic: str = RuntimeConfig.KAFKA_TOPIC
        self.__client: Producer = self.__get_client()

    def __get_client(self) -> Producer:
        broker_list_csv = ",".join(self.__broker_list)
        config = {'bootstrap.servers': broker_list_csv, "queue.buffering.max.ms": 1,
                  "queue.buffering.max.messages": 500}

        if self.__kafka_user_name and self.__kafka_password and self.__kafka_cert_pem:
            config |= {'sasl.username': self.__kafka_user_name, 'sasl.password': self.__kafka_password,
                       'security.protocol': 'SASL_SSL', 'sasl.mechanisms': 'SCRAM-SHA-512',
                       'ssl.endpoint.identification.algorithm': 'none', 'ssl.ca.pem': self.__kafka_cert_pem}

        return Producer(config)

    def publish(self, message: str) -> None:
        encoded_message = JSONEncoder().encode(message).encode('utf8')
        self.__client.produce(self.__kafka_topic, encoded_message)
        self.__client.flush()
