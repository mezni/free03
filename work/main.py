import asyncio
from typing import List, Dict
import pandas as pd


class Reader:
    def read_csv(self, file_path: str) -> List[Dict]:
        df = pd.read_csv(file_path)
        data = df.to_dict("records")
        return data


class Validator:
    def __init__(self, column_mapping):
        self.column_mapping = column_mapping

    def validate(self, data: List[Dict]) -> List[Dict]:

        costs = []
        cost = {}
        for record in data:
            cost = {}
            for attr, col in self.column_mapping.items():
                cost[attr] = record[col]
            costs.append(cost)
        return costs


async def main():
    aws_mapping = {
        "org_name": "Client",
        "period_name": "Date",
        "provider_name": "Provider",
        "account_name": "SubscriptionName",
        "service_name": "ServiceName",
        "resource_name": "Resource",
        "resource_id": "ResourceId",
        "region_name": "ResourceLocation",
        "cost": "CostUSD",
        "currency": "Currency",
    }
    reader = Reader()
    data = reader.read_csv("tests/aws_data.csv")
    validator = Validator(aws_mapping)
    costs = validator.validate(data)
    for c in costs:
        print(c)


asyncio.run(main())
