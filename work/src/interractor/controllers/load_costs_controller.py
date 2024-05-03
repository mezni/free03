from src.interractor.interfaces.data_reader import DataReader
from src.interractor.interfaces.data_loader import DataLoader
from src.interractor.usecases.load_costs_usecase import ProcessDataUseCase


class DataController:
    def __init__(self, data_reader: DataReader, data_loader: DataLoader):
        self.process_data_use_case = ProcessDataUseCase(data_reader, data_loader)

    def process_data(self, file_path: str) -> None:
        self.process_data_use_case.execute(file_path)
