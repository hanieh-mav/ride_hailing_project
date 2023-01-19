import logging
from typing import Union

from flask import request, abort, Response
from flask_restful import Resource
from injector import inject

from src.service.core.service_app_service_contract.service_app_service.iprice_coefficient_service import \
    IPriceCoefficientService
from src.service.utils.validation import Validation


class PriceCoefficientRestService(Resource):

    @inject
    def __init__(self, service: IPriceCoefficientService):
        self.__service = service

    def get(self):
        try:
            requested_data: dict = request.args
            latitude: Union[str, None] = requested_data.get('latitude')
            longitude: Union[str, None] = requested_data.get('longitude')
            self.__validate_get_method_requested_data(latitude, longitude)
            float_latitude: float = float(latitude)
            float_longitude: float = float(longitude)
            return self.__service.get_price_coefficient(float_latitude, float_longitude)
        except Exception as error:
            logging.exception(error)
            abort(400, {'error_description': error.args[0]})

    @staticmethod
    def __validate_get_method_requested_data(latitude: Union[str, None], longitude: Union[str, None]):
        Validation.validate_variable_existence(latitude)
        Validation.validate_variable_existence(longitude)
        Validation.validate_is_float_type(float(latitude))
        Validation.validate_is_float_type(float(longitude))
