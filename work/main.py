import asyncio
from typing import List, Dict
import pandas as pd
import numpy as np


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


class UseCase:
    def __init__(self):
        self.orgs = []
        self.periods = []
        self.accounts = []
        self.services = []
        self.regions = []
        self.resources = []

    def execute(self, data: List[Dict]):
        df = pd.DataFrame(data)
        cols = ["org_name"]
        df_temp = df.groupby(cols).size().reset_index(name="Freq")[cols]
        self.orgs = df_temp.to_dict("records")

        cols = ["period_name"]
        df_temp = df.groupby(cols).size().reset_index(name="Freq")[cols]
        self.periods = df_temp.to_dict("records")

        cols = ["org_name", "provider_name", "account_name"]
        df_temp = df.groupby(cols).size().reset_index(name="Freq")[cols]
        self.accounts = df_temp.to_dict("records")

        cols = ["provider_name", "service_name"]
        df_temp = df.groupby(cols).size().reset_index(name="Freq")[cols]
        self.services = df_temp.to_dict("records")

        cols = ["provider_name", "region_name"]
        df_temp = df.groupby(cols).size().reset_index(name="Freq")[cols]
        self.regions = df_temp.to_dict("records")

        cols = [
            "org_name",
            "provider_name",
            "account_name",
            "resource_name",
            "resource_id",
        ]
        df_temp = df.groupby(cols).size().reset_index(name="Freq")[cols]
        self.resources = df_temp.to_dict("records")


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
    usecase = UseCase()
    usecase.execute(costs)
    print(usecase.resources)


asyncio.run(main())
