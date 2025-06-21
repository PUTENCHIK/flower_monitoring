import asyncio
import logging
from aiogram import Bot
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import Config
from src.database import engine
from src.devices.models import Device, Port
from src.notifications.models import СriticalNotificationChatIDs
logger = logging.getLogger(__name__)


def calc_percent_value(sensor_value, min_value, max_value):
    return 100 - ((sensor_value - min_value) / (max_value - min_value)) * 100


async def check_and_notify_critical(bot: Bot):
    try:
        async with AsyncSession(engine) as db:
            devices = await db.execute(select(Device).filter(and_(Device.last_activity is not None)))

            devices = devices.scalars().all()

            for device in devices:
                if device.name is None:
                    message = f'❗Устройство "{device.deviceToken[0:6]}..." зафиксировало низкий уровень влажности ' \
                              f'почвы в следующих горшках:\n\n'
                else:
                    message = f'❗Устройство "{device.name}" ({device.deviceToken[0:6]}...) зафиксировало низкий уровень ' \
                              f'влажности почвы в следующих горшках:\n\n'

                condition = and_(Port.device_id == device.id,
                                 Port.enabled == True,
                                 calc_percent_value(Port.sensor_value, Port.min_value, Port.max_value) < Port.low_level_boundary)


                ports = await db.execute(select(Port).filter(condition))
                ports = ports.scalars().all()

                if len(ports) == 0:
                    continue

                for port in ports:
                    percent_value = calc_percent_value(port.sensor_value, port.min_value, port.max_value)
                    message += f"Горшок {port.port_number} {port.name} - {round(percent_value)}% (Минимальный порог {port.low_level_boundary}%)\n"

                message += "\nРастения нуждаются в поливе. Проверьте состояние почвы и полейте их как можно скорее.💧"

                chat_ids = await db.execute(select(СriticalNotificationChatIDs.chat_id)
                                            .filter(СriticalNotificationChatIDs.device_id == device.id, 
                                                    СriticalNotificationChatIDs.isActive == True))
                
                chat_ids = chat_ids.scalars().all()

                for chat_id in chat_ids:
                    try:
                        await bot.send_message(chat_id, message)
                    except Exception as e:
                        print(f"Не удалось отправить сообщение в чат {chat_id}: {e}")

    except Exception as e:
        logger.exception(f"Check error: {e}")



async def scheduler_critical(bot: Bot):
    while True:
        await check_and_notify_critical(bot)
        await asyncio.sleep(Config.scheduler.check_critical_interval_hours * 60 * 60)