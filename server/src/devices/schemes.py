from pydantic import BaseModel, Field, field_validator
from typing import Dict, Optional


class PortConfig(BaseModel):
    enabled: bool = Field(..., description="Включен ли порт")
    name: Optional[str] = None
    low_level_boundary: Optional[int] = None
    medium_level_boundary: Optional[int] = None

    @field_validator("low_level_boundary", "medium_level_boundary")
    def boundary_must_be_positive(cls, value):
        if value < 0:
            raise ValueError("Граница должна быть положительным числом")
        return value


class DeviceConfig(BaseModel):
    name: str = Field(..., description="Имя устройства")
    ports: Dict[str, PortConfig] = Field(
        ..., description="Конфигурация портов (ключ - идентификатор порта)"
    )


class RegisterRequestModel(BaseModel):
    deviceToken: str = Field(..., description="Токен устройства")
    password: str = Field(..., description="Пароль")
    config: DeviceConfig = Field(..., description="Конфигурация устройства")