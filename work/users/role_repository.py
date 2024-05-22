from typing import List, Optional
from role_entity import Role
from uuid import UUID


class RoleRepository:
    def __init__(self):
        self.roles = []

    def add_role(self, role: Role):
        self.roles.append(role)

    def get_all_roles(self) -> List[Role]:
        return self.roles

    def find_role_by_id(self, role_id: UUID) -> Optional[Role]:
        return next((role for role in self.roles if role.id == role_id), None)

    def find_role_by_name(self, name: str) -> Optional[Role]:
        return next((role for role in self.roles if role.name == name), None)
