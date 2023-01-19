import logging

from injector import Injector

from flask import Flask
from flask_restful import Api

from src.service.config.base_config import BaseConfig
from src.service.config.runtime_config import RuntimeConfig

from flask_injector import FlaskInjector

from src.service.core.service_app_service.price_coefficient_service import PriceCoefficientService
from src.service.core.service_app_service.request_threshold_coefficient_service import \
    RequestThresholdCoefficientService
from src.service.core.service_app_service_contract.connection.icache_connection import ICacheConnection
from src.service.core.service_app_service_contract.connection.idatabase_connection import IDatabaseConnection
from src.service.core.service_app_service_contract.connection.imessage_publisher_connection import \
    IMessagePublisherConnection
from src.service.core.service_app_service_contract.repository.iregion_price_coefficient_repository import \
    IRegionPriceCoefficientRepository
from src.service.core.service_app_service_contract.repository.irequest_threshold_coefficient_repository import \
    IRequestThresholdCoefficientRepository
from src.service.core.service_app_service_contract.service_app_service.iprice_coefficient_service import \
    IPriceCoefficientService
from src.service.core.service_app_service_contract.service_app_service.irequest_threshold_coefficient_service import \
    IRequestThresholdCoefficientService
from src.service.infrastructure.connection.cache_connection import CacheConnection
from src.service.infrastructure.connection.database_connection import DatabaseConnection
from src.service.infrastructure.connection.message_publisher_connection import MessagePublisherConnection
from src.service.infrastructure.repository.region_price_coefficient_repository import RegionPriceCoefficientRepository
from src.service.infrastructure.repository.request_threshold_coefficient_repository import \
    RequestThresholdCoefficientRepository
from src.service.service_agent.rest_service.price_coefficient_rest_service import PriceCoefficientRestService
from src.service.service_agent.rest_service.request_threshold_coefficient_rest_service import \
    RequestThresholdCoefficientRestService

injector = Injector()
injector.binder.bind(IDatabaseConnection, DatabaseConnection)
injector.binder.bind(ICacheConnection, CacheConnection)
injector.binder.bind(IMessagePublisherConnection, MessagePublisherConnection)

injector.binder.bind(IRequestThresholdCoefficientRepository, RequestThresholdCoefficientRepository)
injector.binder.bind(IRegionPriceCoefficientRepository, RegionPriceCoefficientRepository)

injector.binder.bind(IRequestThresholdCoefficientService, RequestThresholdCoefficientService)
injector.binder.bind(IPriceCoefficientService, PriceCoefficientService)

app = Flask(__name__)
api = Api(app)
api.add_resource(RequestThresholdCoefficientRestService, '/', '/<string:pk>')
api.add_resource(PriceCoefficientRestService, '/price/coefficient')
FlaskInjector(app=app, injector=injector)
if __name__ == '__main__':
    BaseConfig.configure(RuntimeConfig)
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
    # from waitress import serve
    # serve(app, host=RuntimeConfig.FLASK_HOST, port=RuntimeConfig.FLASK_PORT)
