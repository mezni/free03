from src.entities.resource import Resource
from src.repositories.resource_repo_abs import AbstractResourceRepository


class ResourceRepository(AbstractResourceRepository):
    def insert(self, data: dict) -> Resource:
        resource = Resource(**data)
        return resource
