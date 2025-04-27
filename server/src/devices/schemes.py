from pydantic import BaseModel, Field, field_validator
from typing import Dict, Optional


class PortConfig(BaseModel):
    enabled: bool
    name: Optional[str] = None
    low_level_boundary: Optional[int] = None
    medium_level_boundary: Optional[int] = None

    @field_validator("low_level_boundary", "medium_level_boundary")
    def boundary_must_be_positive(cls, value):
        if value < 0:
            raise ValueError("The boundary must be a positive number.")
        return value


class DeviceConfig(BaseModel):
    name: str
    ports: Dict[str, PortConfig]


class RegisterRequestModel(BaseModel):
    deviceToken: str
    password: str
    config: DeviceConfig


class PortData(BaseModel):
    value: int


class UpdateDataRequestModel(BaseModel):
    deviceToken: str
    password: str
    ports: Dict[str, PortData]