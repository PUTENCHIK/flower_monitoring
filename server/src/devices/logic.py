import re
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from server.src.devices import RegisterRequestModel
from server.src.devices.models import Device, Port

from passlib.context import CryptContext
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
        port_number = re.findall("\d+", port_number_str)[0]

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
