class Organisation:
    def __init__(self, org_id, name, currency):
        self.org_id = org_id
        self.name = name
        self.currency = currency
        self.is_demo = False
        self.is_active = True
        self.created_at = None
        self.updated_at = None
        self.deleted_at = None
