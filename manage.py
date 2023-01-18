import logging

from injector import Injector

from flask import Flask
from flask_restful import Api

from src.service.config.base_config import BaseConfig
from src.service.config.runtime_config import RuntimeConfig

from flask_injector import FlaskInjector

from src.service.core.service_app_service.request_threshold_coefficient_service import \
    RequestThresholdCoefficientService
from src.service.core.service_app_service_contract.connection.icache_connection import ICacheConnection
from src.service.core.service_app_service_contract.connection.idatabase_connection import IDatabaseConnection
from src.service.core.service_app_service_contract.repository.irequest_threshold_coefficient_repository import \
    IRequestThresholdCoefficientRepository
from src.service.core.service_app_service_contract.service_app_service.irequest_threshold_coefficient_service import \
    IRequestThresholdCoefficientService
from src.service.infrastructure.connection.cache_connection import CacheConnection
from src.service.infrastructure.connection.database_connection import DatabaseConnection
from src.service.infrastructure.repository.request_threshold_coefficient_repository import \
    RequestThresholdCoefficientRepository
from src.service.service_agent.rest_service.request_threshold_coefficient_rest_service import \
    RequestThresholdCoefficientRestService

injector = Injector()
injector.binder.bind(IDatabaseConnection, DatabaseConnection)
injector.binder.bind(ICacheConnection, CacheConnection)
injector.binder.bind(IRequestThresholdCoefficientRepository, RequestThresholdCoefficientRepository)
injector.binder.bind(IRequestThresholdCoefficientService, RequestThresholdCoefficientService)

app = Flask(__name__)
api = Api(app)
api.add_resource(RequestThresholdCoefficientRestService, '/', '/<string:pk>')
FlaskInjector(app=app, injector=injector)
if __name__ == '__main__':
    BaseConfig.configure(RuntimeConfig)
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
    # from waitress import serve
    # serve(app, host=RuntimeConfig.FLASK_HOST, port=RuntimeConfig.FLASK_PORT)
