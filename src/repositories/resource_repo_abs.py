from abc import ABCMeta, abstractmethod

from src.entities.resource import Resource


class AbstractResourceRepository(metaclass=ABCMeta):
    @abstractmethod
    def insert(self, data: dict) -> Resource:
        raise NotImplementedError
