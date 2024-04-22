from src.interactor.dtos.period_create_dtos import CreatePeriodInputDto


def test_period_create_dto(fixture_period_entity_valid):
    input_dto = CreatePeriodInputDto(
        period_name=fixture_period_entity_valid["period_name"]
    )
    assert input_dto.period_name == fixture_period_entity_valid["period_name"]
    assert input_dto.to_dict() == {
        "period_name": fixture_period_entity_valid["period_name"]
    }
