import uuid

# Entities Layer


class Period:
    def __init__(self, period_code, period):
        self.period_code = period_code
        self.period = period


class Resource:
    def __init__(self, resource_code, resource_id, resource_name):
        self.resource_code = resource_code
        self.resource_id = resource_id
        self.resource_name = resource_name


class Usage:
    def __init__(
        self, usage_code, resource_code, period_code, usage_amount, usage_currency
    ):
        self.usage_code = usage_code
        self.resource_code = resource_code
        self.period_code = period_code
        self.usage_amount = usage_amount
        self.usage_currency = usage_currency


# Use Cases Layer


class LoadUsageInteractor:
    def __init__(self, usage_repo):
        self.usage_repo = usage_repo

    def load_usage(
        self, period, resource_id, resource_name, usage_amount, usage_currency
    ):
        period = self.usage_repo.save_period(period)
        resource = self.usage_repo.save_resource(
            period.period_code, resource_id, resource_name
        )
        usage = self.usage_repo.save_usage(
            period.period_code, resource.resource_code, usage_amount, usage_currency
        )
        return period, resource, usage


# Interfaces/Adapters Layer


class UsageRepository:
    def save_period(self, period):
        # Implementation to save post to a database
        period = Period(uuid.uuid4(), period)
        return period

    def save_resource(self, period_code, resource_id, resource_name):
        # Implementation to save post to a database
        resource = Resource(uuid.uuid4(), resource_id, resource_name)
        return resource

    def save_usage(self, period_code, resource_code, usage_amount, usage_currency):
        # Implementation to save post to a database
        usage = Usage(
            uuid.uuid4(), period_code, resource_code, usage_amount, usage_currency
        )
        return usage


if __name__ == "__main__":
    usage_repo = UsageRepository()
    load_usage_interactor = LoadUsageInteractor(usage_repo)

    period, resource, usage = load_usage_interactor.load_usage(
        "2024-04-01", "i-res", "res", 0.321, "USD"
    )
    print(f"Load created: ")
    print(f"  period  : {period.period_code}  {period.period}")
    print(
        f"  resource: {resource.resource_code}  {resource.resource_id} {resource.resource_name}"
    )
    print(
        f"  usage   : {usage.usage_code}  {usage.period_code} {usage.resource_code} {usage.usage_amount} {usage.usage_currency}"
    )
