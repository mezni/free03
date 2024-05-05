from abc import ABC, abstractmethod
from typing import List


class DatabaseInterface(ABC):
    @abstractmethod
    async def init_db(self) -> None:
        pass
