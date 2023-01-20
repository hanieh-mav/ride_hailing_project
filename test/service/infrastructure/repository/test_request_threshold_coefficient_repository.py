from pytest import fixture

from src.service.config.base_config import BaseConfig
from src.service.config.runtime_config import RuntimeConfig
from src.service.core.service_model import RequestThresholdCoefficientModel
from src.service.infrastructure.connection.database_connection import DatabaseConnection
from src.service.infrastructure.repository.request_threshold_coefficient_repository import \
    RequestThresholdCoefficientRepository

from test.service.infrastructure.repository.fixture import create_database_and_delete_after_test, \
    create_cache_connection_and_delete_after_test
from unittest.mock import MagicMock


class TestRequestThresholdCoefficientRepository:

    def test_when_add_model_expect_added_model_has_expected_values(self, create_database_and_delete_after_test):
        database_connection, conn = create_database_and_delete_after_test
        cache_connection = MagicMock()
        repository = RequestThresholdCoefficientRepository(database_connection, cache_connection)
        model = RequestThresholdCoefficientModel(request_threshold=56, price_coefficient=1.23)
        repository.add(model)

        query = f'''select * from "ride.hailing"."RequestThresholdCoefficient"
            where "RequestThreshold"={56}'''
        data = conn.execute(query).fetchone()
        dict_data = dict(data)
        assert dict_data.get('RequestThreshold') == 56
        assert dict_data.get('PriceCoefficient') == 1.23

    def test_when_update_model_expect_updated_model_has_expected_values(self, create_database_and_delete_after_test,
                                                                        create_cache_connection_and_delete_after_test):
        database_connection, conn = create_database_and_delete_after_test
        cache_connection = create_cache_connection_and_delete_after_test
        repository = RequestThresholdCoefficientRepository(database_connection, cache_connection)

        query = """insert into "ride.hailing"."RequestThresholdCoefficient"  ("RequestThreshold","PriceCoefficient")
                        values (12,13)"""
        conn.execute(query)

        with database_connection.ms_sql_server_session() as session:
            exit_model = session.query(RequestThresholdCoefficientModel).filter(
                RequestThresholdCoefficientModel.request_threshold == 12).one()

        cache_key_pattern = repository.key_pattern.format(pk=exit_model.id)
        cache_connection.cache_data(cache_key_pattern, exit_model.make_dict_data())

        exit_model.request_threshold = 89
        repository.update(exit_model)

        with database_connection.ms_sql_server_session() as session:
            update_model = session.query(RequestThresholdCoefficientModel).filter(
                RequestThresholdCoefficientModel.request_threshold == 89).one()

        assert update_model.request_threshold == 89
        assert update_model.price_coefficient == 13
        assert cache_connection.get_cached_data(cache_key_pattern) is None



    def test_when_update_model_expect_updated_model_has_expected_values(self, create_database_and_delete_after_test,
                                                                        create_cache_connection_and_delete_after_test):
        database_connection, conn = create_database_and_delete_after_test
        cache_connection = create_cache_connection_and_delete_after_test
        repository = RequestThresholdCoefficientRepository(database_connection, cache_connection)

        query = """insert into "ride.hailing"."RequestThresholdCoefficient"  ("RequestThreshold","PriceCoefficient")
                        values (12,13)"""
        conn.execute(query)

        with database_connection.ms_sql_server_session() as session:
            exit_model = session.query(RequestThresholdCoefficientModel).filter(
                RequestThresholdCoefficientModel.request_threshold == 12).one()

        cache_key_pattern = repository.key_pattern.format(pk=exit_model.id)
        cache_connection.cache_data(cache_key_pattern, exit_model.make_dict_data())

        exit_model.request_threshold = 89
        repository.update(exit_model)

        with database_connection.ms_sql_server_session() as session:
            update_model = session.query(RequestThresholdCoefficientModel).filter(
                RequestThresholdCoefficientModel.request_threshold == 89).one()

        assert update_model.request_threshold == 89
        assert update_model.price_coefficient == 13
        assert cache_connection.get_cached_data(cache_key_pattern) is None
