import re
from datetime import datetime
from fastapi import status
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import Config
from src.devices import TokenSecuredRequestModel, UpdateDataRequestModel, TokenRequestModel, UpdateConfigRequestModel

from passlib.context import CryptContext

from src.devices.exceptions import DeviceException
from src.devices.models import Device, Port

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_device_by_token(device_token: str, db: AsyncSession) -> Device | None:
    result = await db.execute(select(Device).filter(Device.deviceToken == device_token))
    return result.scalar_one_or_none()


async def _register_device(request: TokenSecuredRequestModel, db: AsyncSession):
    found_device = await get_device_by_token(request.deviceToken, db)
    if found_device is not None:
        raise DeviceException(status.HTTP_400_BAD_REQUEST, "The device is already registered")

    db_device = Device(
        deviceToken=request.deviceToken,
        password=get_password_hash(request.password),
        name="Без названия",
        created_at=datetime.now()
    )
    db.add(db_device)
    await db.flush()

    for i in range(3):
        db_port = Port(
            device_id=db_device.id,
            port_number=i + 1,
            enabled=True,
            name=f"Датчик {i + 1}",
            low_level_boundary=Config.data.default_low_level_boundary,
            medium_level_boundary=Config.data.default_medium_level_boundary,
            min_value=Config.data.min_value,
            max_value=Config.data.max_value,
        )
        db.add(db_port)

    await db.commit()
    await db.refresh(db_device)


async def _update_data(request: UpdateDataRequestModel, db: AsyncSession):
    device = await get_device_by_token(request.deviceToken, db)

    if not device:
        raise DeviceException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid deviceToken")

    if not verify_password(request.password, device.password):
        raise DeviceException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    device.last_activity = datetime.now()

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

        value = port_config.value
        if port_config.value > port.max_value:
            port.max_value = value
        elif port_config.value < port.min_value:
            port.min_value = value

        port.sensor_value = value

    await db.commit()


async def _get_data(request: TokenRequestModel, db: AsyncSession):
    device = await db.execute(select(Device).filter(Device.deviceToken == request.deviceToken))
    device = device.scalars().first()

    if not device:
        raise DeviceException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid deviceToken")

    response = {
        "name": device.name,
        "last_activity": "Данные ещё не приходили" if device.last_activity is None else device.last_activity.strftime("%Y-%m-%d %H:%M"),
        "ports": {}
    }

    ports = await db.execute(select(Port).filter(and_(Port.device_id == device.id)))
    ports = ports.scalars().all()

    for i, port in enumerate(ports):
        if port.sensor_value is not None:
            if not port.enabled:
                continue
            percent_value = 100 - ((port.sensor_value - port.min_value) / (port.max_value - port.min_value)) * 100

            state = "high"
            if percent_value < port.low_level_boundary:
                state = "low"
            elif percent_value < port.medium_level_boundary:
                state = "medium"

            response["ports"][str(port.port_number)] = {
                "name": port.name,
                "value": int(percent_value),
                "state": state
            }

        else:
            response["ports"][str(port.port_number)] = {
                "name": port.name,
                "value": 0,
                "state": "unknown"
            }

    return response


async def _update_config(request: UpdateConfigRequestModel, db: AsyncSession):
    device = await db.execute(select(Device).filter(Device.deviceToken == request.deviceToken))
    device = device.scalars().first()

    if not device:
        raise DeviceException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid deviceToken")

    if not verify_password(request.password, device.password):
        raise DeviceException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    device.name = request.config.name
    device.password = get_password_hash(request.new_password)

    for port_number_str, port_config in request.config.ports.items():
        try:
            port_number = int(re.findall("\\d+", port_number_str)[0])
        except IndexError:
            raise DeviceException(status.HTTP_400_BAD_REQUEST, "Invalid port name specified")

        if port_number < 0:
            raise DeviceException(status.HTTP_400_BAD_REQUEST, "Invalid port name specified")

        port = await db.execute(select(Port).filter(and_(Port.device_id == device.id, Port.port_number == port_number)))
        port = port.scalars().first()

        if not port:
            db_port = Port(
                device_id=device.id,
                port_number=port_number,
                enabled=port_config.enabled,
                name=port_config.name,
                low_level_boundary=port_config.low_level_boundary,
                medium_level_boundary=port_config.medium_level_boundary,
                min_value=Config.data.min_value,
                max_value=Config.data.max_value,
            )
            db.add(db_port)
        else:
            port.enabled = port_config.enabled
            port.name = port_config.name
            port.low_level_boundary = port_config.low_level_boundary
            port.medium_level_boundary = port_config.medium_level_boundary

    await db.commit()


async def _get_config(request: TokenRequestModel, db: AsyncSession):
    device = await db.execute(select(Device).filter(Device.deviceToken == request.deviceToken))
    device = device.scalars().first()

    if not device:
        raise DeviceException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid deviceToken")

    response = {
        "name": device.name,
        "ports": {}
    }

    ports = await db.execute(select(Port).filter(and_(Port.device_id == device.id)))
    ports = ports.scalars().all()

    for i, port in enumerate(ports):
        response["ports"][str(port.port_number)] = {
            "enabled": port.enabled,
            "name": port.name,
            "low_level_boundary": port.low_level_boundary,
            "medium_level_boundary": port.medium_level_boundary
        }

    return response


async def _check_password(request: TokenSecuredRequestModel, db: AsyncSession):
    device = await get_device_by_token(request.deviceToken, db)

    if not device:
        raise DeviceException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid deviceToken")

    if not verify_password(request.password, device.password):
        raise DeviceException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")