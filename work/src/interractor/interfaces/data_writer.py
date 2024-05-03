from abc import ABC, abstractmethod
from typing import List, Dict


class DataLoader(ABC):
    @abstractmethod
    def load_data(self, data: List[Dict]) -> None:
        pass
