from role_usecase import RoleUseCase
from role_repository import RoleRepository
from role_service import RoleService
from uuid import UUID


def main():
    # Initialize repositories
    role_repository = RoleRepository()

    # Initialize services
    role_service = RoleService(role_repository)

    # Initialize use cases
    role_use_case = RoleUseCase(role_service)

    # Create roles
    admin_role = role_use_case.create_role(
        name="Admin", description="Administrator role"
    )
    user_role = role_use_case.create_role(name="User", description="Regular user role")

    roles = role_use_case.list_roles()
    for r in roles:
        print(r)


if __name__ == "__main__":
    main()
