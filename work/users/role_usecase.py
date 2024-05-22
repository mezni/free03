from role_service import RoleService


class RoleUseCase:
    def __init__(self, role_service: RoleService):
        self.role_service = role_service

    def create_role(self, name: str, description: str):
        return self.role_service.create_role(name, description)

    def list_roles(self):
        return self.role_service.get_roles()
