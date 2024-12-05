import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
# from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from keyboard import main_menu
from text import extract_text_from_response
from YandexAPI import send_message

from secret import TOKEN_BOT, API_KEY, FOLDER_ID

api_key = API_KEY
folder_id = FOLDER_ID
token = TOKEN_BOT

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {message.from_user.full_name}!"
                         f"я могу кратко отвечать на твои вопросы"
                         f"задай интересующий тебя вопрос и я постараюсь ответить как можно более кратко")


"""class ChatStates(StatesGroup):
    YANDEX_GPT_CHAT = State()  # Состояние для общения с YandexGPT


def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("YandexGPT"))
    return markup


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Выберите нейросеть:", reply_markup=main_menu())


@dp.message_handler(lambda msg: msg.text == 'YandexGPT', state='*')
async def handle_yandex_gpt_button(message: types.Message):
    await message.answer(
        f'Привет, {message.from_user.first_name}, я нейросеть YandexGPT, давай общаться и делиться идеями.')
    await ChatStates.YANDEX_GPT_CHAT.set()
"""

@dp.message()
async def ai_message_handler(message: types.Message) -> None:
    try:
        await message.bot.send_chat_action(message.chat.id, "typing")
        if message.text:
            try:
                await message.answer(extract_text_from_response(send_message(message.text)))
            except TelegramBadRequest:
                await message.answer("Не хочу об этом говорить")
        else:
            await message.answer("Я могу отвечать только на текстовые сообщения!")
    except TypeError:
        await message.answer("Произошла ошибка при обработке сообщения.")


async def main() -> None:
    # Инициализация экземпляра бота с Markdown по умолчанию
    bot = Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    # Запуск обработки событий
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
