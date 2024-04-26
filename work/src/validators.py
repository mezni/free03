from typing import Dict


class ProviderInputDtoValidator:
    def __init__(self, input_data: Dict) -> None:
        self.input_data = input_data

    def validate(self) -> None:
        pass
