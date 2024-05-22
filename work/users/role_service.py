from role_entity import Role
from role_repository import RoleRepository
from uuid import UUID
from typing import Optional, List


class RoleService:
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository

    def create_role(self, name: str, description: str) -> Role:
        role = Role(name=name, description=description)
        self.role_repository.add_role(role)
        return role

    def get_roles(self) -> List[Role]:
        return self.role_repository.get_all_roles()

    def find_role_by_id(self, role_id: UUID) -> Optional[Role]:
        return self.role_repository.find_role_by_id(role_id)
