from src.interractor.interfaces.data_reader import DataReader
from src.interractor.interfaces.data_loader import DataLoader


class ProcessDataUseCase:
    def __init__(self, data_reader: DataReader, data_loader: DataLoader):
        self.data_reader = data_reader
        self.data_loader = data_loader

    def execute(self, file_path: str) -> None:
        data = self.data_reader.read_data(file_path)
        self.data_loader.load_data(data)
