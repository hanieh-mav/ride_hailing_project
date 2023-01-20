from unittest.mock import MagicMock

from src.service.core.service_app_service.request_threshold_coefficient_service import \
    RequestThresholdCoefficientService

from pytest import raises

from src.service.core.service_model import RequestThresholdCoefficientModel


class TestRequestThresholdCoefficientService:

    def test_when_add_request_threshold_coefficient_and_not_exit_model_expect_call_repository_add_once(self):
        mocked_repository = MagicMock()
        mocked_repository.check_request_threshold_existence.return_value = False
        mocked_repository.add.return_value = None

        service = RequestThresholdCoefficientService(mocked_repository)
        service.add_request_threshold_coefficient(request_threshold=10, price_coefficient=45)

        mocked_repository.add.assert_called_once()

    def test_when_add_request_threshold_coefficient_and_not_exit_model_expect_added_model_has_expected_values(self):
        mocked_repository = MagicMock()
        mocked_repository.check_request_threshold_existence.return_value = False
        mocked_repository.add.return_value = None

        service = RequestThresholdCoefficientService(mocked_repository)
        service.add_request_threshold_coefficient(request_threshold=10, price_coefficient=45)

        added_model = mocked_repository.add.call_args[0][0]
        assert added_model.request_threshold == 10
        assert added_model.price_coefficient == 45

    def test_when_add_request_threshold_coefficient_and_exit_model_expect_raise_error(self):
        mocked_repository = MagicMock()
        mocked_repository.check_request_threshold_existence.return_value = True
        service = RequestThresholdCoefficientService(mocked_repository)
        with raises(ValueError):
            service.add_request_threshold_coefficient(request_threshold=10, price_coefficient=45)

    def test_when_update_request_threshold_coefficient_and_not_exit_model_expect_never_call_repository_update(
            self):
        mocked_repository = MagicMock()
        mocked_repository.get_model_by_pk.return_value = None
        mocked_repository.update.return_value = None

        service = RequestThresholdCoefficientService(mocked_repository)
        service.update_request_threshold_coefficient(request_threshold=10, price_coefficient=45, pk='10')

        mocked_repository.update.assert_not_called()

    def test_when_update_request_threshold_coefficient_and_exit_model_expect_call_repository_update_once(
            self):
        mocked_repository = MagicMock()
        mocked_repository.get_model_by_pk.return_value = RequestThresholdCoefficientModel()
        mocked_repository.update.return_value = None

        service = RequestThresholdCoefficientService(mocked_repository)
        service.update_request_threshold_coefficient(request_threshold=10, price_coefficient=45, pk='10')

        mocked_repository.update.assert_called_once()

    def test_when_update_request_threshold_coefficient_and_exit_model_expect_updated_model_has_expected_values(self):
        mocked_repository = MagicMock()
        mocked_repository.get_model_by_pk.return_value = RequestThresholdCoefficientModel()
        mocked_repository.update.return_value = None

        service = RequestThresholdCoefficientService(mocked_repository)
        service.update_request_threshold_coefficient(request_threshold=10, price_coefficient=45, pk='10')

        updated_model = mocked_repository.update.call_args[0][0]
        assert updated_model.request_threshold == 10
        assert updated_model.price_coefficient == 45

    def test_when_get_request_threshold_coefficient_by_pk_not_exist_model_expect_none(self):
        mocked_repository = MagicMock()
        mocked_repository.get_model_by_pk.return_value = None

        service = RequestThresholdCoefficientService(mocked_repository)
        data = service.get_request_threshold_coefficient_by_pk(pk='10')
        assert data is None

    def test_when_get_request_threshold_coefficient_by_pk_exist_model_expect_dict(self):
        mocked_repository = MagicMock()
        mocked_repository.get_model_by_pk.return_value = RequestThresholdCoefficientModel(request_threshold=15,
                                                                                          price_coefficient=15, id=4)

        service = RequestThresholdCoefficientService(mocked_repository)
        data = service.get_request_threshold_coefficient_by_pk(pk='10')
        assert isinstance(data, dict)

    def test_when_get_request_threshold_coefficient_by_pk_exist_model_expect_expected_values(self):
        mocked_repository = MagicMock()
        mocked_repository.get_model_by_pk.return_value = RequestThresholdCoefficientModel(request_threshold=15,
                                                                                          price_coefficient=16, id=4)

        service = RequestThresholdCoefficientService(mocked_repository)
        data = service.get_request_threshold_coefficient_by_pk(pk='10')
        assert data.get('request_threshold') == 15
        assert data.get('price_coefficient') == 16
        assert data.get('id') == 4

    def test_when_get_all_request_threshold_coefficient_list_not_exist_expect_empty_list(self):
        mocked_repository = MagicMock()
        mocked_repository.get_all_model_list.return_value = []

        service = RequestThresholdCoefficientService(mocked_repository)
        data = service.get_all_request_threshold_coefficient_list()
        assert len(data) == 0

    def test_when_get_all_request_threshold_coefficient_list_exist_expect_list_with_len_2(self):
        mocked_repository = MagicMock()
        mocked_repository.get_all_model_list.return_value = [RequestThresholdCoefficientModel(request_threshold=15,
                                                                                              price_coefficient=16,
                                                                                              id=4),
                                                             RequestThresholdCoefficientModel(request_threshold=15,
                                                                                              price_coefficient=16,
                                                                                              id=4)]

        service = RequestThresholdCoefficientService(mocked_repository)
        data = service.get_all_request_threshold_coefficient_list()
        assert len(data) == 2

    def test_when_get_all_request_threshold_coefficient_list_exist_expect_first_item_has_expected_values(self):
        mocked_repository = MagicMock()
        mocked_repository.get_all_model_list.return_value = [RequestThresholdCoefficientModel(request_threshold=15,
                                                                                              price_coefficient=16,
                                                                                              id=4),
                                                             RequestThresholdCoefficientModel(request_threshold=15,
                                                                                              price_coefficient=16,
                                                                                              id=8)]

        service = RequestThresholdCoefficientService(mocked_repository)
        data = service.get_all_request_threshold_coefficient_list()
        first_data = data[0]
        assert first_data.get('request_threshold') == 15
        assert first_data.get('price_coefficient') == 16
        assert first_data.get('id') == 4
