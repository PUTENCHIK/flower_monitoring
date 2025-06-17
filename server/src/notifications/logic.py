from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from src.devices import verify_password
from src.notifications.models import Notification
from src.notifications.exceptions import BotDeviceException, NotificationException
from src.notifications.schemes import NotificationRequestModel, UpdateNotificationRequestModel, GetNotificationsRequestModel, \
                            DeleteNotificationRequestModel
from passlib.context import CryptContext
from src.devices.models import Device, DeviceChatIDs
from datetime import datetime


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_device_by_token(device_token: str, db: AsyncSession) -> Device | None:
    result = await db.execute(select(Device).filter(Device.deviceToken == device_token))
    return result.scalar_one_or_none()


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


async def check_notification(request: NotificationRequestModel, device_id: int, db: AsyncSession) -> Notification | None:
    result = await db.execute(
        select(Notification)
        .filter(Notification.device_id == device_id, 
                Notification.time == request.time, 
                Notification.days == request.days)
    )

    return result.scalar_one_or_none()


async def get_notification_by_id(notification_id: int, db: AsyncSession) -> Notification | None:
    result = await db.execute(select(Notification).filter(Notification.id == notification_id))
    return result.scalar_one_or_none()


async def _create_notification(request: UpdateNotificationRequestModel, db: AsyncSession):
    device = await get_device_by_token(request.deviceToken, db)

    if not device:
        raise NotificationException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid deviceToken")

    if not verify_password(request.password, device.password):
        raise NotificationException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    
    
    found_notification = await check_notification(request, device.id, db)

    if found_notification is not None:
        raise NotificationException(status.HTTP_400_BAD_REQUEST, "The notification is already created")

    db_notification = Notification(
        device_id=device.id,
        message=request.message,
        days=request.days,
        time=request.time,
        enabled=request.enabled,
        created_at=datetime.now()
    )

    db.add(db_notification)
    await db.commit()
    await db.refresh(db_notification)


async def _update_notification(request: UpdateNotificationRequestModel, db: AsyncSession):
    device = await get_device_by_token(request.deviceToken, db)

    if not device:
        raise NotificationException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid deviceToken")

    if not verify_password(request.password, device.password):
        raise NotificationException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    

    found_notification = await check_notification(request, device.id, db)

    if found_notification is not None:
        raise NotificationException(status.HTTP_400_BAD_REQUEST, "Same notification is already created")


    db_notification = await get_notification_by_id(request.notification_id, db)

    if db_notification is None:
        raise NotificationException(status.HTTP_404_NOT_FOUND, "Notification not found")

    db_notification.message = request.message
    db_notification.days = request.days
    db_notification.time = request.time
    db_notification.enabled = request.enabled

    db.add(db_notification)
    await db.commit()


async def _get_notifications(request: GetNotificationsRequestModel, db: AsyncSession):
    device = await get_device_by_token(request.deviceToken, db)

    if not device:
        raise NotificationException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid deviceToken")
    
    notifications = await db.execute(select(Notification).filter(Notification.device_id == device.id))
    notifications = notifications.scalars().all()

    response = []

    for i, notification in enumerate(notifications):
        response.append({
            "id": notification.id,
            "message": notification.message,
            "days": notification.days,
            "time": notification.time,
            "enabled": notification.enabled
        })

    return response


async def _delete_notification(request: DeleteNotificationRequestModel, db: AsyncSession):
    device = await get_device_by_token(request.deviceToken, db)

    if not device:
        raise NotificationException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid deviceToken")

    if not verify_password(request.password, device.password):
        raise NotificationException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    

    db_notification = await get_notification_by_id(request.notification_id, db)

    if db_notification is None:
        raise NotificationException(status.HTTP_404_NOT_FOUND, "Notification not found")

    db.delete(db_notification)
    await db.commit()