import uuid

usage_input = [
    {
        "resource_id": uuid.UUID("6c19bceb-0472-450c-8d23-97c755a137f8"),
        "resource_name": "i-37854322484",
        "period": "2024-04-01",
        "usage_amount": 0.0127,
        "usage_currency": "USD",
    },
    {
        "resource_id": uuid.UUID("6c19bceb-0472-450c-8d23-97c755a137f8"),
        "resource_name": "i-37854322484",
        "period": "2024-04-02",
        "usage_amount": 0.0123,
        "usage_currency": "USD",
    },
    {
        "resource_id": uuid.UUID("6c19bceb-0472-450c-8d23-97c755a137f8"),
        "resource_name": "i-37854322484",
        "period": "2024-04-01",
        "usage_amount": 0.0122,
        "usage_currency": "USD",
    },
]


class Resource:
    def __init__(self, resource_id, resource_name):
        self.resource_id = resource_id
        self.resource_name = resource_name


class Usage:
    def __init__(self, usage_id, resource_id, period, usage_amount, usage_currency):
        self.usage_id = usage_id
        self.resource_id = resource_id
        self.period = period
        self.usage_amount = usage_amount
        self.usage_currency = usage_currency


for u in usage_input:
    print(u)
