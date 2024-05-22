from role_usecase import RoleUseCase
from role_repository import RoleRepository
from role_service import RoleService
from uuid import UUID
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware


def main():
    db_path = "_users.db"
    db = TinyDB(db_path, storage=CachingMiddleware(JSONStorage))

    role_repository = RoleRepository(db)

    # Initialize services
    role_service = RoleService(role_repository)

    # Initialize use cases
    role_use_case = RoleUseCase(role_service)

    # Create roles
    admin_role = role_use_case.create_role(
        name="Admin", description="Administrator role"
    )
    org_manager_role = role_use_case.create_role(
        name="Organisation Manager", description="Organisation Manager"
    )
    manager_role = role_use_case.create_role(name="Manager", description="Manager")
    user_role = role_use_case.create_role(name="User", description="Regular user role")
    roles = role_use_case.list_roles()
    for r in roles:
        print(r)


if __name__ == "__main__":
    main()
