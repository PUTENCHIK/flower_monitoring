from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from src.devices import verify_password
from src.notifications.models import RegularNotification, RegularNotificationChatIDs, СriticalNotificationChatIDs
from src.notifications.exceptions import BotDeviceException, NotificationException
from src.notifications.schemes import NotificationRequestModel, UpdateNotificationRequestModel, GetNotificationsRequestModel, \
                            DeleteNotificationRequestModel, GetNotificationRequestModel, ChangeStateNotificationRequestModel
from passlib.context import CryptContext
from src.devices.models import Device
from datetime import datetime


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_device_by_token(device_token: str, db: AsyncSession) -> Device | None:
    result = await db.execute(select(Device).filter(Device.deviceToken == device_token))
    return result.scalar_one_or_none()


async def _add_regular_chat_id(deviceToken: str, chat_id: int, db: AsyncSession):
    try:
        device = await db.execute(select(Device).filter(Device.deviceToken == deviceToken))
        device = device.scalars().first()

        if not device:
            raise BotDeviceException(detail="Устройства по такому токену не найдено. Попробуйте ещё раз ввести токен устройства.")
        

        notify_user = await db.execute(select(RegularNotificationChatIDs)
                                       .filter(RegularNotificationChatIDs.device_id == device.id,
                                               RegularNotificationChatIDs.chat_id == chat_id))
        
        notify_user = notify_user.scalars().first()

        if notify_user:
            if notify_user.isActive:
                raise BotDeviceException(detail="Чат уже привязан к устройству")
            else:
                notify_user.isActive = True
        else:
            new_chat_id = RegularNotificationChatIDs(device_id=device.id, chat_id=chat_id, isActive=True)
            db.add(new_chat_id)
        
        await db.commit()

    except Exception as e:
        await db.rollback()
        raise


async def _add_critical_chat_id(deviceToken: str, chat_id: int, db: AsyncSession):
    try:
        device = await db.execute(select(Device).filter(Device.deviceToken == deviceToken))
        device = device.scalars().first()

        if not device:
            raise BotDeviceException(detail="Устройства по такому токену не найдено. Попробуйте ещё раз ввести токен устройства.")
        

        notify_user = await db.execute(select(СriticalNotificationChatIDs)
                                       .filter(СriticalNotificationChatIDs.device_id == device.id,
                                               СriticalNotificationChatIDs.chat_id == chat_id))
        
        notify_user = notify_user.scalars().first()

        if notify_user:
            if notify_user.isActive:
                raise BotDeviceException(detail="Чат уже привязан к устройству")
            else:
                notify_user.isActive = True
        else:
            new_chat_id = СriticalNotificationChatIDs(device_id=device.id, chat_id=chat_id, isActive=True)
            db.add(new_chat_id)
        
        await db.commit()

    except Exception as e:
        await db.rollback()
        raise


async def _remove_regular_chat_id(deviceToken: str, chat_id: int, db: AsyncSession):
    try:
        device = await db.execute(select(Device).filter(Device.deviceToken == deviceToken))
        device = device.scalars().first()

        if not device:
            raise BotDeviceException(detail="Устройства по такому токену не найдено. Попробуйте ещё раз ввести токен устройства.")


        regular_notification = await db.execute(select(RegularNotificationChatIDs)
                                  .filter(RegularNotificationChatIDs.chat_id == chat_id, 
                                          RegularNotificationChatIDs.device_id == device.id))
        
        regular_notification = regular_notification.scalars().first()

        if not regular_notification:
            raise BotDeviceException(detail="Вы и так к этом устройству не были привязаны")


        regular_notification.isActive = False
        await db.commit()

    except Exception as e:
        await db.rollback()
        raise


async def _remove_critical_chat_id(deviceToken: str, chat_id: int, db: AsyncSession):
    try:
        device = await db.execute(select(Device).filter(Device.deviceToken == deviceToken))
        device = device.scalars().first()

        if not device:
            raise BotDeviceException(detail="Устройства по такому токену не найдено. Попробуйте ещё раз ввести токен устройства.")


        critical_notification = await db.execute(select(СriticalNotificationChatIDs)
                                  .filter(СriticalNotificationChatIDs.chat_id == chat_id, 
                                          СriticalNotificationChatIDs.device_id == device.id))
        
        critical_notification = critical_notification.scalars().first()

        if not critical_notification:
            raise BotDeviceException(detail="Вы и так к этом устройству не были привязаны")


        critical_notification.isActive = False
        await db.commit()

    except Exception as e:
        await db.rollback()
        raise



async def check_notification(request: NotificationRequestModel, device_id: int, db: AsyncSession) -> RegularNotification | None:
    result = await db.execute(
        select(RegularNotification)
        .filter(RegularNotification.device_id == device_id, 
                RegularNotification.time == request.time, 
                RegularNotification.days == request.days,
                RegularNotification.message == request.message)
    )

    return result.scalar_one_or_none()


async def get_notification_by_id(notification_id: int, db: AsyncSession) -> RegularNotification | None:
    result = await db.execute(select(RegularNotification).filter(RegularNotification.id == notification_id))
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

    db_notification = RegularNotification(
        device_id=device.id,
        message=request.message,
        days=request.days,
        time=request.time,
        isActive=request.isActive,
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
    db_notification.isActive = request.isActive

    await db.commit()


async def _get_notifications(request: GetNotificationsRequestModel, db: AsyncSession):
    device = await get_device_by_token(request.deviceToken, db)

    if not device:
        raise NotificationException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid deviceToken")
    
    notifications = await db.execute(select(RegularNotification)
                                     .filter(RegularNotification.device_id == device.id,
                                             RegularNotification.deleted_at == None))
    notifications = notifications.scalars().all()

    response = []

    for i, notification in enumerate(notifications):
        response.append({
            "id": notification.id,
            "message": notification.message,
            "days": notification.days,
            "time": notification.time.strftime("%H:%M"),
            "isActive": notification.isActive
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

    db_notification.deleted_at = datetime.now()
    await db.commit()


async def _get_notification(request: GetNotificationRequestModel, db: AsyncSession):
    device = await get_device_by_token(request.deviceToken, db)

    if not device:
        raise NotificationException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid deviceToken")
    
    notification = await db.execute(select(RegularNotification)
                                     .filter(RegularNotification.device_id == device.id,
                                             RegularNotification.id == request.notification_id,
                                             RegularNotification.deleted_at == None))
    
    notification = notification.scalar_one_or_none()

    if not notification:
        raise NotificationException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid notification id")

    response = {
        "id": notification.id,
        "message": notification.message,
        "days": notification.days,
        "time": notification.time.strftime("%H:%M"),
        "isActive": notification.isActive
    }

    return response


async def _change_state_notification(request: ChangeStateNotificationRequestModel, db: AsyncSession):
    device = await get_device_by_token(request.deviceToken, db)

    if not device:
        raise NotificationException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid deviceToken")
    
    if not verify_password(request.password, device.password):
        raise NotificationException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    
    notification = await db.execute(select(RegularNotification)
                                     .filter(RegularNotification.device_id == device.id,
                                             RegularNotification.id == request.notification_id,
                                             RegularNotification.deleted_at == None))
    
    notification = notification.scalar_one_or_none()

    if not notification:
        raise NotificationException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid notification id")

    notification.isActive = request.isActive

    await db.commit()