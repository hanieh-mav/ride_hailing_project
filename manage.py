import logging

from apscheduler.triggers.cron import CronTrigger
from injector import Injector

from flask import Flask
from flask_restful import Api
from sqlalchemy_utils import database_exists, create_database
from waitress import serve

from src.service.config.base_config import BaseConfig
from src.service.config.runtime_config import RuntimeConfig

from flask_injector import FlaskInjector

from src.service.core.service_app_service.price_coefficient_service import PriceCoefficientService
from src.service.core.service_app_service.region_price_coefficient_calculator_service import \
    RegionPriceCoefficientCalculatorService
from src.service.core.service_app_service.region_request_service import RegionRequestService
from src.service.core.service_app_service.request_threshold_coefficient_service import \
    RequestThresholdCoefficientService
from src.service.core.service_app_service_contract.connection.icache_connection import ICacheConnection
from src.service.core.service_app_service_contract.connection.idatabase_connection import IDatabaseConnection
from src.service.core.service_app_service_contract.connection.imessage_publisher_connection import \
    IMessagePublisherConnection
from src.service.core.service_app_service_contract.connection.imessage_receiver_connection import \
    IMessageReceiverConnection
from src.service.core.service_app_service_contract.repository.iregion_price_coefficient_repository import \
    IRegionPriceCoefficientRepository
from src.service.core.service_app_service_contract.repository.iregion_repository import IRegionRepository
from src.service.core.service_app_service_contract.repository.iregion_request_repository import IRegionRequestRepository
from src.service.core.service_app_service_contract.repository.irequest_threshold_coefficient_repository import \
    IRequestThresholdCoefficientRepository
from src.service.core.service_app_service_contract.service_app_service.iprice_coefficient_service import \
    IPriceCoefficientService
from src.service.core.service_app_service_contract.service_app_service.iregion_request_service import \
    IRegionRequestService
from src.service.core.service_app_service_contract.service_app_service.irequest_threshold_coefficient_service import \
    IRequestThresholdCoefficientService
from src.service.core.service_model.base import Base
from src.service.infrastructure.connection.cache_connection import CacheConnection
from src.service.infrastructure.connection.database_connection import DatabaseConnection
from src.service.infrastructure.connection.message_publisher_connection import MessagePublisherConnection
from src.service.infrastructure.connection.message_receiver_connection import MessageReceiverConnection
from src.service.infrastructure.repository.region_price_coefficient_repository import RegionPriceCoefficientRepository
from src.service.infrastructure.repository.region_repository import RegionRepository
from src.service.infrastructure.repository.region_request_repository import RegionRequestRepository
from src.service.infrastructure.repository.request_threshold_coefficient_repository import \
    RequestThresholdCoefficientRepository
from src.service.service_agent.message_handler.trace_message_handler import TraceMessageHandler
from src.service.service_agent.rest_service.price_coefficient_rest_service import PriceCoefficientRestService
from src.service.service_agent.rest_service.request_threshold_coefficient_rest_service import \
    RequestThresholdCoefficientRestService

import click

injector = Injector()
injector.binder.bind(IDatabaseConnection, DatabaseConnection)
injector.binder.bind(ICacheConnection, CacheConnection)
injector.binder.bind(IMessagePublisherConnection, MessagePublisherConnection)
injector.binder.bind(IMessageReceiverConnection, MessageReceiverConnection)

injector.binder.bind(IRequestThresholdCoefficientRepository, RequestThresholdCoefficientRepository)
injector.binder.bind(IRegionPriceCoefficientRepository, RegionPriceCoefficientRepository)
injector.binder.bind(IRegionRepository, RegionRepository)
injector.binder.bind(IRegionRequestRepository, RegionRequestRepository)

injector.binder.bind(IRequestThresholdCoefficientService, RequestThresholdCoefficientService)
injector.binder.bind(IPriceCoefficientService, PriceCoefficientService)
injector.binder.bind(IRegionRequestService, RegionRequestService)

app = Flask(__name__)
api = Api(app)
api.add_resource(RequestThresholdCoefficientRestService, '/', '/<string:pk>')
api.add_resource(PriceCoefficientRestService, '/price/coefficient')
FlaskInjector(app=app, injector=injector)


@click.group()
def cli():
    pass


def start_trace_message_process():
    process = injector.get(TraceMessageHandler)
    process.trace_message()


def start_calculator_process():
    process = injector.get(RegionPriceCoefficientCalculatorService)
    from apscheduler.schedulers.blocking import BlockingScheduler
    scheduler = BlockingScheduler()
    scheduler.add_job(func=process.calculate_price_coefficient,
                      trigger=get_cron_trigger_from_string_expression(
                          RuntimeConfig.SCHEDULED_TIME_FOR_CALCULATOR_PROCESS)
                      )

    scheduler.start()


def get_cron_trigger_from_string_expression(string_expression: str) -> CronTrigger:
    vals = string_expression.split()
    vals = [(None if w == '?' else w) for w in vals]
    return CronTrigger(year=vals[0], month=vals[1], week=vals[2], day=vals[3], hour=vals[4], minute=vals[5],
                       second=vals[6])


def start_rest_service():
    serve(app, host=RuntimeConfig.FLASK_HOST, port=RuntimeConfig.FLASK_PORT)


@cli.command()
def start_service():
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor() as executor:
        executor.submit(start_rest_service)
        executor.submit(start_calculator_process)
        executor.submit(start_trace_message_process)


def creat_database():
    database = injector.get(DatabaseConnection)
    engine = database.engine
    if not database_exists(engine.url):
        create_database(engine.url)

        connection = engine.connect()
        schema_query = 'create schema "ride.hailing"'
        connection.execute(schema_query)
        Base.metadata.create_all(engine)


if __name__ == '__main__':
    BaseConfig.configure(RuntimeConfig)
    logging.basicConfig(level=logging.DEBUG)
    creat_database()

    cli()
