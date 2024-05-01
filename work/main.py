import asyncio
from abc import ABC, abstractmethod


class InputReader(ABC):
    @abstractmethod
    def read_source(self, source_path):
        raise NotImplementedError


class CSVReader(InputReader):
    def read_source(self, source_path):
        data = []
        return data


class InputReaderUseCase:
    def __init__(self, input_reader):
        self.input_reader = input_reader

    def execute(self, source_path):
        return self.input_reader.read_source(source_path)


async def main():
    source_type = "csv"
    source_path = ""
    if source_type == "csv":
        input_reader = CSVReader("source_path")

    input_reader_usecase = InputReaderUseCase(input_reader)
    input_reader_usecase.execute(source_path)


asyncio.run(main())
