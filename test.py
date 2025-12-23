import asyncio
from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


# Это функция для отложенного удаления сообщений
async def delete_message(message: Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(TelegramBadRequest):
        await message.delete()


# Этот хэндлер будет срабатывать на команду /start
@dp.message(CommandStart())
async def command_start_process(message: Message):
    await message.answer(
        text=f'Привет, <b>{message.from_user.full_name}</b>!\n\n'
             f'Отправь команду /del, чтобы увидеть отложенное удаление сообщения'
    )


# Этот хэндлер будет срабатывать на команду /del
@dp.message(Command('del'))
async def send_and_del_message(message: Message):
    msg = await message.answer('Это сообщение удалится через 3 секунды')
    asyncio.create_task(delete_message(msg, 3))


dp.run_polling(bot)