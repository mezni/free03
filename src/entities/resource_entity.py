""" Module for Usage resource"""

import uuid

from pydantic import BaseModel


class Resource(BaseModel):
    """Definition of the Resource entity"""

    resource_id: uuid.UUID
    name: str
