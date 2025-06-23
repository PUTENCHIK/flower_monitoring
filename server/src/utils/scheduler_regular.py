import asyncio
import datetime
import logging
from aiogram import Bot
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import engine
from src.devices.models import Device
from src.notifications.models import RegularNotificationChatIDs, RegularNotification
logger = logging.getLogger(__name__)
import pytz


def is_right_time(days: int, time: datetime.time) -> bool:
    moscow_timezone = pytz.timezone('Europe/Moscow')
    now_utc = datetime.datetime.utcnow()
    now_moscow = now_utc.replace(tzinfo=pytz.utc).astimezone(moscow_timezone)
    current_weekday = now_moscow.weekday()
    current_time = now_moscow.time()

    if days & (1 << current_weekday):
        if current_time.hour == time.hour and current_time.minute == time.minute:
            return True
        else:
            return False
    else:
        return False



async def check_and_notify_regular(bot: Bot):
    try:
        async with AsyncSession(engine) as db:
            regular_notifications = await db.execute(select(RegularNotification)
                        .filter(RegularNotification.isActive == True,
                                RegularNotification.deleted_at == None))

            regular_notifications = regular_notifications.scalars().all()

            regular_notifications = [
                notification for notification in regular_notifications
                if is_right_time(notification.days, notification.time)
            ]


            for notification in regular_notifications:
                device = await db.execute(select(Device).filter(and_(Device.id == notification.device_id)))
                device = device.scalar_one_or_none()

                if not device:
                    continue

                chat_ids = await db.execute(select(RegularNotificationChatIDs.chat_id)
                                            .filter(RegularNotificationChatIDs.device_id == device.id, 
                                                    RegularNotificationChatIDs.isActive == True))
                
                chat_ids = chat_ids.scalars().all()

                for chat_id in chat_ids:
                    try:
                        message = f"🗓️ Уведомление, запланированное на {notification.time.strftime('%H:%M')} по МСК: \n\n{notification.message} 💬"
                        await bot.send_message(chat_id, message)
                    except Exception as e:
                        print(f"Не удалось отправить сообщение в чат {chat_id}: {e}")

    except Exception as e:
        logger.exception(f"Check error: {e}")


def calculate_delay_to_start():
    now = datetime.datetime.now()
    next_minute = now + datetime.timedelta(minutes=1)
    next_minute = next_minute.replace(second=0, microsecond=0)
    delay = (next_minute - now).total_seconds()
    return delay


async def scheduler_regular(bot: Bot):
    delay = calculate_delay_to_start()
    await asyncio.sleep(delay + 1)
    await check_and_notify_regular(bot)

    while True:
        delay = calculate_delay_to_start()
        await asyncio.sleep(delay + 1)
        await check_and_notify_regular(bot)