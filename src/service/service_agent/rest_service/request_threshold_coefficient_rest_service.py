import logging
from typing import Union

from flask import request, abort, Response
from flask_restful import Resource
from injector import inject

from src.service.core.service_app_service_contract.service_app_service.irequest_threshold_coefficient_service import \
    IRequestThresholdCoefficientService
from src.service.utils.validation import Validation


class RequestThresholdCoefficientRestService(Resource):

    @inject
    def __init__(self, service: IRequestThresholdCoefficientService):
        self.__service = service

    def get(self, pk: str = None):
        try:
            if pk:
                return self.__service.get_request_threshold_coefficient_by_pk(pk)
            return self.__service.get_all_request_threshold_coefficient_list()
        except Exception as error:
            logging.exception(error)
            abort(400, {'error_description': error.args[0]})

    def post(self):
        try:
            requested_data: dict = request.json
            request_threshold: Union[int, None] = requested_data.get('request_threshold')
            price_coefficient: Union[int, float, None] = requested_data.get('price_coefficient')
            self.__validate_post_method_requested_data(request_threshold, price_coefficient)
            self.__service.add_request_threshold_coefficient(request_threshold, price_coefficient)
            return Response(status=201)
        except Exception as error:
            logging.exception(error)
            abort(400, {'error_description': error.args[0]})

    def put(self, pk: str):
        try:
            requested_data: dict = request.json
            request_threshold: Union[int, None] = requested_data.get('request_threshold')
            price_coefficient: Union[int, float, None] = requested_data.get('price_coefficient')
            self.__validate_put_method_requested_data(pk, request_threshold, price_coefficient)
            self.__service.update_request_threshold_coefficient(pk, request_threshold, price_coefficient)
            return Response(status=201)
        except Exception as error:
            logging.exception(error)
            abort(400, {'error_description': error.args[0]})

    @staticmethod
    def __validate_post_method_requested_data(threshold: Union[int, None],
                                              price_coefficient: Union[int, float, None]):
        Validation.validate_variable_existence(threshold)
        Validation.validate_variable_existence(price_coefficient)
        Validation.validate_is_not_negative_integer_type(threshold)
        Validation.validate_is_not_non_negative_float_or_integer_type(price_coefficient)

    @staticmethod
    def __validate_put_method_requested_data(pk: Union[str, None], threshold: Union[int, None],
                                             price_coefficient: Union[int, float, None]):
        if threshold:
            Validation.validate_is_not_negative_integer_type(threshold)
        if price_coefficient:
            Validation.validate_is_not_non_negative_float_or_integer_type(price_coefficient)
        Validation.validate_variable_existence(pk)
        Validation.validate_is_string_type(pk)

