from src.interactor.dtos.period import PeriodInputDto


def test_period_dto_input_valid(fixture_period_valid):

    input_dto = PeriodInputDto(
        period_code=fixture_period_valid["period_code"],
        period_name=fixture_period_valid["period_name"],
    )
    assert input_dto.period_code == fixture_period_valid["period_code"]
    assert input_dto.period_name == fixture_period_valid["period_name"]
    assert input_dto.to_dict() == fixture_period_valid
