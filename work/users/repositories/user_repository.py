from typing import Dict
from abc import ABC, abstractmethod


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, payload: Dict):
        pass
