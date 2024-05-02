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

    def _get_distinct(self, df, cols):
        df_temp = df.groupby(cols).size().reset_index(name="Freq")[cols]
        return df_temp.to_dict("records")

    def _load_structs(self, df):
        self.orgs = self._get_distinct(df, ["org_name"])
        self.periods = self._get_distinct(df, ["period_name"])
        self.accounts = self._get_distinct(
            df, ["org_name", "provider_name", "account_name"]
        )
        self.services = self._get_distinct(df, ["provider_name", "service_name"])
        self.regions = self._get_distinct(df, ["provider_name", "region_name"])
        self.resources = self._get_distinct(
            df,
            [
                "org_name",
                "provider_name",
                "account_name",
                "resource_name",
                "resource_id",
            ],
        )

    def execute(self, data: List[Dict]):
        df = pd.DataFrame(data)
        self._load_structs(df)
        for org in self.orgs:
            print(org)


class Repository:
    def __init__(self):
        self.orgs = []

    def load_orgs(self):
        pass


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


asyncio.run(main())
