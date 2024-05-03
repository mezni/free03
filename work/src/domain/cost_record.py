import uuid
from pydantic import BaseModel



class CostRecord(BaseModel):

    cost_record_code: uuid.UUID
    cost_record_org_name: str
    cost_record_account_name: str
    cost_record_period_name: str