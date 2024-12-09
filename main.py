import logging
import asyncio
import aioredis
from aiogram import Bot, Dispatcher, types
from aiogram.client.session import aiohttp
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from secret import TOKEN_BOT, REDIS_URL, API_KEY, FOLDER_ID
from api.YandexAPI import YandexApi
from states.fsm import ChatStates
from keyboards.markup import get_main_menu

logging.basicConfig(level=logging.INFO)

LOADING_MESSAGE = "Loading..."

bot = Bot(token=TOKEN_BOT)
redis = aioredis.from_url(REDIS_URL)
storage = RedisStorage(redis=redis)
dp = Dispatcher(storage=storage)
yandex_api = YandexApi(API_KEY, FOLDER_ID)


async def main():
    from conig_bot.handlers import setup_handlers
    setup_handlers(dp)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())