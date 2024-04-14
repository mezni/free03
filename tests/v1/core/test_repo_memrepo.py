import pytest
from unittest import mock

from src.core.v1.domain import value_objects as v
from src.core.v1.domain import usage as u
from src.core.v1.usecases import usage_list_usecase as uc
from src.core.v1.repository import memrepo

@pytest.fixture
def usage_dicts():
    return [
        {
            "usage_id": "0661c1d3-6e76-7505-8000-d49ae24611a0",
            "resource_id": "0661be9f-0260-7f5d-8000-6a4da3317708",
            "period": "2024-04-14",
            "usage_amount": 0.013,
            "usage_currency": "USD",
        },
        {
            "usage_id": "0661c1dc-744c-728e-8000-92b541110ef3",
            "resource_id": "0661be9f-0260-7f5d-8000-6a4da3317708",
            "period": "2024-04-15",
            "usage_amount": 0.012,
            "usage_currency": "USD",
        },
        {
            "usage_id": "0661c1dd-2a73-7510-8000-be4ace4c4140",
            "resource_id": "0661be9f-0260-7f5d-8000-6a4da3317708",
            "period": "2024-04-16",
            "usage_amount": 0.013,
            "usage_currency": "USD",
        },
        {
            "usage_id": "0661c1de-ad04-785b-8000-14737c99b197",
            "resource_id": "0661be9f-0260-7f5d-8000-6a4da3317708",
            "period": "2024-04-17",
            "usage_amount": 0.013,
            "usage_currency": "USD",
        },
        {
            "usage_id": "0661c1df-96b6-7d50-8000-a6f341f24438",
            "resource_id": "0661be9f-0260-7f5d-8000-6a4da3317708",
            "period": "2024-04-18",
            "usage_amount": 0.002,
            "usage_currency": "USD",
        },
    ]


def test_repository_list_without_parameters(usage_dicts):
    repo = memrepo.MemRepo(usage_dicts)

    usages = [u.Usage.from_dict(i) for i in usage_dicts]

    assert repo.list() == usages
