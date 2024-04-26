""" Usage entities module
"""

from datetime import datetime
from pydantic import BaseModel
from src.types import UUIDType, generate_uuid


class Provider(BaseModel):
    """Definition of the Provider entity"""

    provider_code: UUIDType
    provider_name: str


class Region(BaseModel):
    """Definition of the Region entity"""

    region_code: UUIDType
    provider_code: UUIDType
    region_name: str


class Service(BaseModel):
    """Definition of the Service entity"""

    service_code: UUIDType
    provider_code: UUIDType
    service_name: str
