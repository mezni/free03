import asyncio
from datetime import datetime, timedelta


async def main():
    usage_data = [
        {
            "organisation": "momentum tech",
            "provider": "aws",
            "period": "2024-04-20",
            "account_id": "367475994817",
            "account_name": "367475994817",
            "resource_id": "",
            "resource_name": "",
            "resource_type": "",
            "resource_location": "us-east-1",
            "service_name": "Amazon Elastic Compute Cloud - Compute",
            "tags": [],
            "meter": "",
            "cost_usd": 4.41,
            "cost": 4.41,
            "currency": "USD",
        },
        {
            "organisation": "momentum tech",
            "provider": "aws",
            "period": "2024-04-20",
            "account_id": "367475994817",
            "account_name": "367475994817",
            "resource_id": "",
            "resource_name": "",
            "resource_type": "",
            "resource_location": "us-east-1",
            "service_name": "EC2 - Other",
            "tags": [],
            "meter": "",
            "cost_usd": 1.52,
            "cost": 1.52,
            "currency": "USD",
        },
        {
            "organisation": "momentum tech",
            "provider": "azure",
            "period": "2024-04-20",
            "account_id": "1ebabb15-8364-4ada-8de3-a26abeb7ad59",
            "account_name": "mom-opportunite-sub",
            "resource_id": "/subscriptions/1ebabb15-8364-4ada-8de3-a26abeb7ad59/resourcegroups/bi-opportunite-dev-rg/providers/microsoft.storage/storageaccounts/datalakeopportunitedev",
            "resource_name": "",
            "resource_location": "East US",
            "resource_type": "microsoft.storage/storageaccounts",
            "service_name": "Storage",
            "tags": [],
            "meter": "",
            "cost_usd": 7.2,
            "cost": 9.9755,
            "currency": "CAD",
        },
    ]


asyncio.run(main())
