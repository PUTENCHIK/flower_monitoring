from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.devices.models import Device, DeviceChatIDs
from src.notifications.exceptions import BotDeviceException


async def _add_chat_id_to_device(deviceToken: str, chat_id: int, db: AsyncSession):
    try:
        device = await db.execute(select(Device).filter(Device.deviceToken == deviceToken))
        device = device.scalars().first()

        if not device:
            raise BotDeviceException(detail="Не верный идентификатор устройства")

        new_chat_id = DeviceChatIDs(device_id=device.id, chat_id=chat_id)
        db.add(new_chat_id)
        await db.commit()

    except Exception as e:
        await db.rollback()
        raise
