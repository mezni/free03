import json


class UsageJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                "usage_id": o.usage_id,
                "resource_id": o.resource_id,
                "period": o.period,
                "usage_amount": o.usage_amount,
                "usage_currency": o.usage_currency,
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
