from typing import List, Optional
from role_entity import Role
from uuid import UUID
from tinydb import TinyDB, Query

def serializer(item):
    data=item
    uuid = str(data['code'])
    del data['code']
    data['code']=uuid
    return data

class RoleRepository:
    def __init__(self, db):
        self.db = db
        self.table = self.db.table('roles')

    def add_role(self, role: Role):
        self.table.insert(serializer(role.dict()))
        self.db.storage.flush()

    def get_all_roles(self) -> List[Role]:
        roles = self.table.all()
        return [Role(**role) for role in roles]

    def find_role_by_id(self, code: UUID) -> Optional[Role]:
        RoleQuery = Query()
        role = self.table.get(RoleQuery.code == str(code))
        return Role(**role) if role else None

    def find_role_by_name(self, name: str) -> Optional[Role]:
        RoleQuery = Query()
        role = self.table.get(RoleQuery.name == name)
        return Role(**role) if role else None
