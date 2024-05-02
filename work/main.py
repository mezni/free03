import asyncio
from typing import List, Dict
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np


class ReaderRepository(ABC):
    @abstractmethod
    def read_data(self, file_path: str) -> List[Dict]:
        pass


class LoaderRepository(ABC):

    @abstractmethod
    def load_data(self, data: List[Dict]) -> None:
        pass


class Reader(ReaderRepository):
    def read_data(self, file_path: str) -> List[Dict]:
        return []


class Loader(LoaderRepository):
    def load_data(self, data: List[Dict]) -> None:
        pass


class UseCase:
    def __init__(self, data_reader: ReaderRepository, data_loader: LoaderRepository):
        self.data_reader = data_reader
        self.data_loader = data_loader

    def execute(self, file_path: str) -> None:
        data = self.data_reader.read_data(file_path)
        self.data_loader.load_data(data)


async def main():
    reader = Reader()
    loader = Loader()
    usecase = UseCase(reader, loader)
    file_path = "tests/aws_data.csv"
    usecase.execute(file_path)


asyncio.run(main())
