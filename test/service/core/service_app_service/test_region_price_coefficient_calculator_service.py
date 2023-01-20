from unittest.mock import MagicMock

from src.service.core.service_app_service.region_price_coefficient_calculator_service import \
    RegionPriceCoefficientCalculatorService
from src.service.core.service_model import RegionPriceCoefficientModel


class TestRegionPriceCoefficientCalculatorService:

    def test_when_not_exist_price_coefficient_expect_add_price_coefficient_repository_never_call(self):
        mocked_region_repository = MagicMock()
        mocked_request_region_repository = MagicMock()
        mocked_price_coefficient_repository = MagicMock()
        mocked_request_threshold_coefficient_repository = MagicMock()

        mocked_region_repository.get_all_region_id_list.return_value = [10]
        mocked_request_threshold_coefficient_repository.get_price_coefficient_by_request_threshold.return_value = None
        mocked_price_coefficient_repository.add.return_value = None

        service = RegionPriceCoefficientCalculatorService(mocked_region_repository,
                                                          mocked_request_region_repository,
                                                          mocked_price_coefficient_repository,
                                                          mocked_request_threshold_coefficient_repository)
        service.calculate_price_coefficient()
        mocked_price_coefficient_repository.add.assert_not_called()

    def test_when_not_exist_price_coefficient_expect_update_price_coefficient_repository_never_call(self):
        mocked_region_repository = MagicMock()
        mocked_request_region_repository = MagicMock()
        mocked_price_coefficient_repository = MagicMock()
        mocked_request_threshold_coefficient_repository = MagicMock()

        mocked_region_repository.get_all_region_id_list.return_value = [10]
        mocked_request_threshold_coefficient_repository.get_price_coefficient_by_request_threshold.return_value = None
        mocked_price_coefficient_repository.update.return_value = None

        service = RegionPriceCoefficientCalculatorService(mocked_region_repository,
                                                          mocked_request_region_repository,
                                                          mocked_price_coefficient_repository,
                                                          mocked_request_threshold_coefficient_repository)
        service.calculate_price_coefficient()
        mocked_price_coefficient_repository.update.assert_not_called()

    def test_when_not_exist_price_coefficient_region_model_expect_add_price_coefficient_repository_call_once(self):
        mocked_region_repository = MagicMock()
        mocked_request_region_repository = MagicMock()
        mocked_price_coefficient_repository = MagicMock()
        mocked_request_threshold_coefficient_repository = MagicMock()

        mocked_region_repository.get_all_region_id_list.return_value = [10]
        mocked_request_threshold_coefficient_repository.get_price_coefficient_by_request_threshold.return_value = 10
        mocked_price_coefficient_repository.add.return_value = None
        mocked_price_coefficient_repository.get_by_region_id.return_value = None

        service = RegionPriceCoefficientCalculatorService(mocked_region_repository,
                                                          mocked_request_region_repository,
                                                          mocked_price_coefficient_repository,
                                                          mocked_request_threshold_coefficient_repository)
        service.calculate_price_coefficient()
        mocked_price_coefficient_repository.add.assert_called_once()

    def test_when_exist_price_coefficient_region_model_expect_update_price_coefficient_repository_call_once(self):
        mocked_region_repository = MagicMock()
        mocked_request_region_repository = MagicMock()
        mocked_price_coefficient_repository = MagicMock()
        mocked_request_threshold_coefficient_repository = MagicMock()

        mocked_region_repository.get_all_region_id_list.return_value = [10]
        mocked_request_threshold_coefficient_repository.get_price_coefficient_by_request_threshold.return_value = 10
        mocked_price_coefficient_repository.update.return_value = None
        mocked_price_coefficient_repository.get_by_region_id.return_value = RegionPriceCoefficientModel()

        service = RegionPriceCoefficientCalculatorService(mocked_region_repository,
                                                          mocked_request_region_repository,
                                                          mocked_price_coefficient_repository,
                                                          mocked_request_threshold_coefficient_repository)
        service.calculate_price_coefficient()
        mocked_price_coefficient_repository.update.assert_called_once()
