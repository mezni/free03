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
        "period": "2024-04-03",
        "usage_amount": 0.0122,
        "usage_currency": "USD",
    },
    {
        "resource_id": uuid.UUID("e21e035d-d948-4218-b3c4-9bb513c558fd"),
        "resource_name": "i-37854322232",
        "period": "2024-04-01",
        "usage_amount": 0.012,
        "usage_currency": "USD",
    },
]


class Resource:
    def __init__(self, code, resource_id, resource_name):
        self.code = code
        self.resource_id = resource_id
        self.resource_name = resource_name


class Usage:
    def __init__(
        self, code, usage_id, resource_id, period, usage_amount, usage_currency
    ):
        self.code = code
        self.usage_id = usage_id
        self.resource_id = resource_id
        self.period = period
        self.usage_amount = usage_amount
        self.usage_currency = usage_currency


usage = []


class ResourceRepo:
    def __init__(self):
        self.resources = []

    def find_resource(self, resource_id=None, resource_name=None):
        for resource in self.resources:
            if resource_id and resource.resource_id == resource_id:
                return resource.code
            elif resource_name and resource.resource_name == resource_name:
                return resource.code
            else:
                return None

    def add_resource(self, code, resource_id, resource_name):
        self.resources.append(Resource(code, resource_id, resource_name))


resource_repo = ResourceRepo()
for u in usage_input:
    resource_code = resource_repo.find_resource(resource_id=u["resource_id"])
    if not resource_code:
        resource_repo.add_resource(
            code=uuid.uuid4(),
            resource_id=u["resource_id"],
            resource_name=u["resource_name"],
        )

print("fin")
for r in resource_repo.resources:
    print(r.resource_id)
