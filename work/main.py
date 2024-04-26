import asyncio

from src.constants import AWS_CONFIG


async def main():
    regions=AWS_CONFIG["Regions"]
    for region in regions:
        print (region["RegionName"])

    services=AWS_CONFIG["Services"]
    for service in services:
        print (service["ServiceCode"],["ServiceName"])
asyncio.run(main())
