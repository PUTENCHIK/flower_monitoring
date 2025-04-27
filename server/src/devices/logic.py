import re
from datetime import datetime
from fastapi import status
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from server.src.devices import RegisterRequestModel, UpdateDataRequestModel
from passlib.context import CryptContext

from server.src.devices.exceptions import DeviceException
from server.src.devices.models import Device, Port

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def _register_device(request: RegisterRequestModel, db: AsyncSession):
    db_device = Device(
        deviceToken=request.deviceToken,
        password=get_password_hash(request.password),
        name=request.config.name,
        created_at=datetime.now()
    )
    db.add(db_device)
    await db.flush()

    for port_number_str, port_config in request.config.ports.items():
        try:
            port_number = int(re.findall("\\d+", port_number_str)[0])
        except IndexError:
            raise DeviceException(status.HTTP_400_BAD_REQUEST, "Invalid port name specified")

        if port_number < 0:
            raise DeviceException(status.HTTP_400_BAD_REQUEST, "Invalid port name specified")

        db_port = Port(
            device_id=db_device.id,
            port_number=port_number,
            enabled=port_config.enabled,
            name=port_config.name,
            low_level_boundary=port_config.low_level_boundary,
            medium_level_boundary=port_config.medium_level_boundary,
        )
        db.add(db_port)

    await db.commit()
    await db.refresh(db_device)


async def _update_data(request: UpdateDataRequestModel, db: AsyncSession):
    device = await db.execute(select(Device).filter(Device.deviceToken == request.deviceToken))
    device = device.scalars().first()

    if not device:
        raise DeviceException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid deviceToken")

    if verify_password(request.password, device.password):
        raise DeviceException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    for port_number_str, port_config in request.ports.items():
        try:
            port_number = int(re.findall("\\d+", port_number_str)[0])
        except IndexError:
            raise DeviceException(status.HTTP_400_BAD_REQUEST, "Invalid port name")

        if port_number < 0:
            raise DeviceException(status.HTTP_400_BAD_REQUEST, "Invalid port name")

        port = await db.execute(select(Port).filter(and_(Port.device_id == device.id, Port.port_number == port_number)))
        port = port.scalars().first()

        if not port:
            raise DeviceException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid port")

        port.sensor_value = port_config.value

        db.add(port)

    await db.flush()
    await db.commit()
