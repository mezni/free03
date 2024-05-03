from abc import ABC, abstractmethod
from typing import List, Dict


class DataReader(ABC):
    @abstractmethod
    def read_data(self, file_path: str) -> List[Dict]:
        pass
