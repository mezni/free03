import pytest
from unittest import mock

from src.core.v1.domain import value_objects as v
from src.core.v1.domain import usage as u
from src.core.v1.usecases import usage_list_usecase as uc


@pytest.fixture
def domain_usage():
    usage1 = u.Usage(
        usage_id=v.code,
        resource_id="0661be9f-0260-7f5d-8000-6a4da3317708",
        period="2024-04-14",
        usage_amount=0.013,
        usage_currency="USD",
    )
    usage2 = u.Usage(
        usage_id=v.code,
        resource_id="0661be9f-0260-7f5d-8000-6a4da3317708",
        period="2024-04-15",
        usage_amount=0.012,
        usage_currency="USD",
    )
    usage3 = u.Usage(
        usage_id=v.code,
        resource_id="0661be9f-0260-7f5d-8000-6a4da3317708",
        period="2024-04-16",
        usage_amount=0.012,
        usage_currency="USD",
    )
    usage4 = u.Usage(
        usage_id=v.code,
        resource_id="0661be9f-0260-7f5d-8000-6a4da3317708",
        period="2024-04-17",
        usage_amount=0.014,
        usage_currency="USD",
    )
    return [usage1, usage2, usage3, usage4]


def test_usage_list_without_parameters(domain_usage):
    repo = mock.Mock()
    repo.list.return_value = domain_usage

    usage_list_usecase = uc.UsageListUseCase(repo)
    result = usage_list_usecase.execute()

    repo.list.assert_called_with()
    assert result == domain_usage
