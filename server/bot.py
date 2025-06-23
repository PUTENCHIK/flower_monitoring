import asyncio
import os
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from src.utils import scheduler_critical, scheduler_regular
from src.database import engine
from src.notifications import _add_critical_chat_id, _add_regular_chat_id, _remove_critical_chat_id, _remove_regular_chat_id
from src.notifications.exceptions import BotDeviceException
from aiogram.fsm.context import FSMContext  
from aiogram.fsm.state import State, StatesGroup
import os


class LinkState(StatesGroup):
    choosing_type_link = State()
    choosing_action = State()
    waiting_for_token = State()


logger = logging.getLogger(__name__)


TELEGRAM_BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set in environment variables.")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)


@router.message(CommandStart())
@router.message(lambda message: message.text in ["Начать сначала"])
async def handle_start(message: Message, state: FSMContext):
    instruction = f"""
Привет! Я FlowerMonitoring бот. ✨

Я предназначен для оповещения пользователей устройств FlowerMonitoring, когда их растения требуют полива. 💧
Но перед этим вам нужно привязать чат к устройству через панель команд.⬇️

✉️ О уведомлениях:

Экстренные уведомления будут приходить, когда уровень влажности почвы будет находится в критическом зоне.

Регулярные уведомления будут приходить по расписанию, которое вы сможете настроить на нашем сайте.

"""
    
    await state.clear()

    kb = [
        [
            types.KeyboardButton(text="❗✉️Экстренные уведомления")
        ],
        [
            types.KeyboardButton(text="✏️Регулярные уведомления")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, input_field_placeholder="Выберите тип уведомлений")

    await message.reply(instruction, reply_markup=keyboard, resize_keyboard=True)
    await state.set_state(LinkState.choosing_type_link)


# Обработка выбора типа уведомлений

@router.message(
    LinkState.choosing_type_link, 
    F.text.in_(["❗✉️Экстренные уведомления", "✏️Регулярные уведомления"])
)
async def type_link_chosen(message: Message, state: FSMContext):
    kb = [
        [
            types.KeyboardButton(text="Назад"),
            types.KeyboardButton(text="Привязать к устройству"),
            types.KeyboardButton(text="Отвязать от устройства")
        ]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, input_field_placeholder="Выберите действие")
    await state.update_data(choosen_type_link=message.text.lower())
    await message.answer(text="Теперь, пожалуйста, выберите действие:", reply_markup=keyboard)
    await state.set_state(LinkState.choosing_action)


@router.message(
    LinkState.choosing_action,
    F.text.in_(["Назад"])
)
async def type_link_chosen_back(message: Message, state: FSMContext):
    instruction = "Пожалуйста, выберите тип уведомления:"
    await state.update_data(choosen_type_link='')

    kb = [
        [
            types.KeyboardButton(text="❗✉️Экстренные уведомления")
        ],
        [
            types.KeyboardButton(text="✏️Регулярные уведомления")
        ]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, input_field_placeholder="Выберите тип уведомления")

    await message.answer(instruction, reply_markup=keyboard, resize_keyboard=True)
    await state.set_state(LinkState.choosing_type_link)


@router.message(
    LinkState.choosing_type_link
)
async def type_link_chosen_incorrectly(message: Message):
    instruction = "Я не знаю таких уведомлений\n\n Пожалуйста, выберите одно из названий из панели ниже:"

    kb = [
        [
            types.KeyboardButton(text="❗✉️Экстренные уведомления")
        ],
        [
            types.KeyboardButton(text="✏️Регулярные уведомления")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, input_field_placeholder="Выберите тип уведомлений")

    await message.answer(instruction, reply_markup=keyboard, resize_keyboard=True)

# ---------------------

# Обработка действия

@router.message(
    LinkState.choosing_action, 
    F.text.in_(["Привязать к устройству", "Отвязать от устройства"])
)
async def action_chosen(message: Message, state: FSMContext):
    kb = [
        [
            types.KeyboardButton(text="Назад")
        ]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, input_field_placeholder="Введите токен...")
    await state.update_data(choosen_action=message.text.lower())
    await message.answer(text="Теперь, пожалуйста, введите токен устройства:", reply_markup=keyboard)
    await state.set_state(LinkState.waiting_for_token)


@router.message(
    LinkState.waiting_for_token,
    F.text.in_(["Назад"])
)
async def action_chosen_back(message: Message, state: FSMContext):
    instruction = "Пожалуйста, выберите действие:"
    await state.update_data(choosen_action='')

    kb = [
        [
            types.KeyboardButton(text="Назад"),
            types.KeyboardButton(text="Привязать к устройству"),
            types.KeyboardButton(text="Отвязать от устройства")
        ]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, input_field_placeholder="Выберите действие")

    await message.answer(instruction, reply_markup=keyboard, resize_keyboard=True)
    await state.set_state(LinkState.choosing_action)



@router.message(
    LinkState.choosing_action
)
async def action_chosen_incorrectly(message: Message):
    instruction = "Я не знаю таких действий\n\n Пожалуйста, выберите одно из действий из панели ниже:"

    kb = [
        [
            types.KeyboardButton(text="Назад"),
            types.KeyboardButton(text="Привязать к устройству"),
            types.KeyboardButton(text="Отвязать от устройства")
        ]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, input_field_placeholder="Выберите действие")

    await message.answer(instruction, reply_markup=keyboard, resize_keyboard=True)

# -----------------

# Обработка токена

@router.message(
    LinkState.waiting_for_token
)
async def link_chat(message: Message, state: FSMContext):
    device_token = message.text
    user_data = await state.get_data()

    kb = [
        [
            types.KeyboardButton(text="Начать сначала")
        ]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)

    type_link = user_data["choosen_type_link"]
    action = user_data["choosen_action"]


    async with AsyncSession(engine) as db:
        try:
            if type_link == "❗✉️экстренные уведомления":
                if action == "привязать к устройству":
                    await _add_critical_chat_id(device_token, message.chat.id, db)
                elif action == "отвязать от устройства":
                    await _remove_critical_chat_id(device_token, message.chat.id, db)
                else:
                    await message.reply(f"Такого действия не найдено", reply_markup=keyboard)
                    await state.clear()
                    return

            elif type_link == "✏️регулярные уведомления":
                if action == "привязать к устройству":
                    await _add_regular_chat_id(device_token, message.chat.id, db)
                elif action == "отвязать от устройства":
                    await _remove_regular_chat_id(device_token, message.chat.id, db)
                else:
                    await message.reply(f"Такого действия не найдено", reply_markup=keyboard)
                    await state.clear()
                    return
            else:
                await message.reply(f"Такого типа уведомлений не найдено", reply_markup=keyboard)
                await state.clear()
                return


            if action == "привязать к устройству":
                await message.reply(f"Чат успешно привязан к устройству {device_token}.", reply_markup=keyboard)
            elif action == "отвязать от устройства":
                await message.reply(f"Чат успешно отвязан от устройства {device_token}.", reply_markup=keyboard)

            await state.clear()
            return
            
        except BotDeviceException as exception:
            await message.reply(exception.detail)
            return
        except Exception as e:
            logger.exception(f"Ошибка работы бота: {e}")
            await message.reply("Неизвестная ошибка. Начните сначала или попробуйте позже",
                                 reply_markup=keyboard)
            return



async def main():
    try:
        print("Bot started")
        asyncio.create_task(scheduler_critical(bot))
        asyncio.create_task(scheduler_regular(bot))
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("Bot stopped")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
