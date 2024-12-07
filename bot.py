import logging
import asyncio
import aioredis
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from secret import TOKEN_BOT, REDIS_URL
from YandexAPI import get_response_from_yandex_gpt
from fsm import ChatStates
from markup import get_main_menu

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN_BOT)
redis = aioredis.from_url(REDIS_URL)
storage = RedisStorage(redis=redis)
dp = Dispatcher(storage=storage)


@dp.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    await message.answer("Выберите нейросеть:", reply_markup=get_main_menu())


@dp.message(lambda message: message.text == 'YandexGPT')
async def yandexgpt_start(message: types.Message, state: FSMContext):
    await message.answer(
        f"Привет, {message.from_user.first_name}, я нейросеть YandexGPT, давай общаться и делиться идеями.")
    await state.set_state(ChatStates.waiting_for_question)


@dp.message(ChatStates.waiting_for_question)
async def handle_question(message: types.Message, state: FSMContext):
    loading_message = await message.answer("Loading…")
    response = get_response_from_yandex_gpt(message.text)
    response_json = response.json()

    logging.info(f"Response from YandexGPT API: {response_json}")

    if 'result' in response_json and 'alternatives' in response_json['result']:
        alternatives = response_json['result']['alternatives']
        if alternatives:
            assistant_message = alternatives[0]['message']['text']
            await bot.delete_message(chat_id=message.chat.id, message_id=loading_message.message_id)
            await message.answer(assistant_message, parse_mode=ParseMode.MARKDOWN)
        else:
            await message.answer("Ошибка при получении ответа от YandexGPT API.")
    else:
        await message.answer("Ошибка при получении ответа от YandexGPT API.")

    await state.set_state(ChatStates.waiting_for_question)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
