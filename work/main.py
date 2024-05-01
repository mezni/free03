import asyncio
from abc import ABC, abstractmethod
from src.input_reader_usecase import InputReaderUseCase


class InputReader(ABC):
    @abstractmethod
    def read_source(self, source_path):
        raise NotImplementedError


class CSVReader(InputReader):
    def __init__(self):
        pass

    def read_source(self, source_path):
        data = []
        return data


async def main():
    source_type = "csv"
    source_path = ""
    if source_type == "csv":
        input_reader = CSVReader()

    input_reader_usecase = InputReaderUseCase(input_reader)
    input_reader_usecase.execute(source_path)


asyncio.run(main())
