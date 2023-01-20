from unittest.mock import MagicMock

from src.service.core.service_app_service.region_request_service import RegionRequestService


class TestRegionRequestService:

    def test_when_region_id_not_exist_expect_request_region_repository_add_never_call(self):
        mocked_region_repository = MagicMock()
        mocked_request_region_repository = MagicMock()

        mocked_region_repository.get_id_by_place_id.return_value = None
        mocked_request_region_repository.add.return_value = None

        service = RegionRequestService(mocked_region_repository, mocked_request_region_repository)
        service.save_request_for_region('10')

        mocked_request_region_repository.add.assert_not_called()

    def test_when_region_id_not_exist_expect_region_repository_repository_add_call_once(self):
        mocked_region_repository = MagicMock()
        mocked_request_region_repository = MagicMock()

        mocked_region_repository.get_id_by_place_id.return_value = None
        mocked_region_repository.add.return_value = None

        service = RegionRequestService(mocked_region_repository, mocked_request_region_repository)
        service.save_request_for_region('10')

        mocked_region_repository.add.asser_called_once()
