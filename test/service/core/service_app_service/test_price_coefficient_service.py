from unittest.mock import MagicMock
from pytest import raises

from src.service.core.service_app_service.price_coefficient_service import PriceCoefficientService


class TestPriceCoefficientService:

    def test_when_place_id_not_for_tehran_expect_raise_value_error(self):
        mocked_message_publisher = MagicMock()
        mocked_region_price_coefficient_repository = MagicMock()
        mocked_request_threshold_coefficient_repository = MagicMock()
        service = PriceCoefficientService(mocked_message_publisher, mocked_region_price_coefficient_repository,
                                          mocked_request_threshold_coefficient_repository)

        with raises(ValueError):
            service.get_price_coefficient(latitude=35.896258, longitude=51.268074)

    def test_when_everything_ok_expect_message_publisher_publish_call_once(self):
        mocked_message_publisher = MagicMock()
        mocked_message_publisher.publish.return_value = None
        mocked_region_price_coefficient_repository = MagicMock()
        mocked_request_threshold_coefficient_repository = MagicMock()
        service = PriceCoefficientService(mocked_message_publisher, mocked_region_price_coefficient_repository,
                                          mocked_request_threshold_coefficient_repository)
        service.get_price_coefficient(latitude=35.701805, longitude=51.268074)
        mocked_message_publisher.publish.assert_called_once()

    def test_when_exist_price_coefficient_expect_return_10(self):
        mocked_message_publisher = MagicMock()
        mocked_region_price_coefficient_repository = MagicMock()
        mocked_region_price_coefficient_repository.get_price_coefficient_by_region_id.return_value = 10
        mocked_request_threshold_coefficient_repository = MagicMock()
        service = PriceCoefficientService(mocked_message_publisher, mocked_region_price_coefficient_repository,
                                          mocked_request_threshold_coefficient_repository)
        result = service.get_price_coefficient(latitude=35.701805, longitude=51.268074)
        assert result == 10

    def test_when_exist_price_coefficient_expect_call_get_price_coefficient_by_region_id_once(self):
        mocked_message_publisher = MagicMock()
        mocked_region_price_coefficient_repository = MagicMock()
        mocked_region_price_coefficient_repository.get_price_coefficient_by_region_id.return_value = 10
        mocked_request_threshold_coefficient_repository = MagicMock()
        service = PriceCoefficientService(mocked_message_publisher, mocked_region_price_coefficient_repository,
                                          mocked_request_threshold_coefficient_repository)
        service.get_price_coefficient(latitude=35.701805, longitude=51.268074)
        mocked_region_price_coefficient_repository.get_price_coefficient_by_region_id.assert_called_once()

    def test_when_not_exist_price_coefficient_expect_return_19(self):
        mocked_message_publisher = MagicMock()
        mocked_region_price_coefficient_repository = MagicMock()
        mocked_request_threshold_coefficient_repository = MagicMock()
        mocked_region_price_coefficient_repository.get_price_coefficient_by_region_id.return_value = None
        mocked_request_threshold_coefficient_repository.get_price_coefficient_by_request_threshold.return_value = 19

        service = PriceCoefficientService(mocked_message_publisher, mocked_region_price_coefficient_repository,
                                          mocked_request_threshold_coefficient_repository)
        result = service.get_price_coefficient(latitude=35.701805, longitude=51.268074)
        assert result == 19

    def test_not_when_exist_price_coefficient_expect_call_get_price_coefficient_by_request_threshold_once(self):
        mocked_message_publisher = MagicMock()
        mocked_region_price_coefficient_repository = MagicMock()
        mocked_request_threshold_coefficient_repository = MagicMock()
        mocked_region_price_coefficient_repository.get_price_coefficient_by_region_id.return_value = None
        mocked_request_threshold_coefficient_repository.get_price_coefficient_by_request_threshold.return_value = 19

        service = PriceCoefficientService(mocked_message_publisher, mocked_region_price_coefficient_repository,
                                          mocked_request_threshold_coefficient_repository)
        service.get_price_coefficient(latitude=35.701805, longitude=51.268074)
        mocked_request_threshold_coefficient_repository.get_price_coefficient_by_request_threshold.assert_called_once()
