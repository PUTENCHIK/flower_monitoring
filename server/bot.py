import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from src.utils.scheduler import scheduler
from src.database import engine
from src.notifications import _add_chat_id_to_device
from src.notifications.exceptions import BotDeviceException

logger = logging.getLogger(__name__)


TELEGRAM_BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set in environment variables.")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def handle_start(message: Message):
    instruction = f"""
Привет! Я FlowerMonitoring бот.

Я предназначен для оповещения пользователей устройств FlowerMonitoring, когда их растения требуют полива.
Но перед этим вам нужно привязать телеграмм аккаунт к устройству через /link)

Доступные команды:
- /start - показать это сообщение
- /link [токен устройства] - привязать телеграмм аккаунт к устройству FlowerMonitoring для получения уведомлений
    """
    markup = ReplyKeyboardRemove()
    await message.answer(instruction, reply_markup=markup)


@dp.message(Command("link"))
async def link_command(message: Message):
    try:
        parts = message.text.split(" ", 1)
        if len(parts) != 2:
            await message.reply("Неверный формат команды. Используйте: /link [идентификатор устройства]")
            return

        device_token = parts[1]

        async with AsyncSession(engine) as db:
            try:
                await _add_chat_id_to_device(device_token, message.chat.id, db)
                await message.reply(f"Чат успешно привязан к устройству {device_token}.")
            except BotDeviceException as exception:
                await message.reply(exception.detail)
                return
            except Exception as e:
                logger.exception(f"Ошибка работы бота: {e}")
                await message.reply("Неизвестная ошибка. Начните сначала или попробуйте использовать команду позже")
                return
    except Exception as e:
        logger.exception(f"Ошибка работы бота: {e}")
        await message.reply("Произошла ошибка при обработке команды. Проверьте формат и повторите попытку.")


async def main():
    try:
        print("Bot started")
        asyncio.create_task(scheduler(bot))
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("Bot stopped")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
