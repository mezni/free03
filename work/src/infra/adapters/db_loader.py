from typing import List, Dict
from src.interractor.interfaces.data_writer import DataLoader


class DatabaseDataLoader(DataLoader):
    def load_data(self, data: List[Dict]) -> None:
        pass
