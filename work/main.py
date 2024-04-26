import asyncio

from src.constants import AWS_CONFIG
from src.entities import Provider
from src.dtos import ProviderInputDto, ProviderOutputtDto
from src.validators import ProviderInputDtoValidator


async def main():
    #    regions = AWS_CONFIG["Regions"]
    #    for region in regions:
    #        print(region["RegionName"])

    provider_input_dto = ProviderInputDto(provider_name="aws")
    print(provider_input_dto.model_dump())

    validator = ProviderInputDtoValidator(provider_input_dto.model_dump())
    validator.validate()


#    repository.create(provider_input_dto)

asyncio.run(main())
