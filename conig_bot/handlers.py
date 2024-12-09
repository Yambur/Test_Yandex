import logging
from aiogram import types
from aiogram.client.session import aiohttp
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from main import dp, LOADING_MESSAGE, yandex_api, ChatStates, get_main_menu, bot


@dp.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    await message.answer("Выберите нейросеть:", reply_markup=get_main_menu())


@dp.message(lambda message: message.text == 'YandexGPT')
async def yandexgpt_start(message: types.Message, state: FSMContext):
    user_name = message.from_user.first_name
    await message.answer(f"Привет, {user_name}, я нейросеть YandexGPT, давай общаться и делиться идеями.")
    await state.set_state(ChatStates.waiting_for_question)


@dp.message(ChatStates.waiting_for_question)
async def handle_question(message: types.Message, state: FSMContext):
    logging.info(f"User question: {message.text}")

    # Извлекаем текущий диалог из Redis
    current_data = await state.get_data()
    dialog = current_data.get('dialog', [])

    # Добавляем текущий вопрос пользователя в диалог
    dialog.append({"role": "user", "text": message.text})

    loading_message = await message.answer(LOADING_MESSAGE)
    async with aiohttp.ClientSession() as session:
        response_json = await yandex_api.get_response_from_yandex_gpt(message.text, session, dialog)

    logging.info(f"Ответ от YandexGPT API: {response_json}")

    if 'result' in response_json and 'alternatives' in response_json['result']:
        alternatives = response_json['result']['alternatives']
        if alternatives:
            assistant_message = alternatives[0]['message']['text']
            # Добавляем ответ от YandexGPT в диалог
            dialog.append({"role": "assistant", "text": assistant_message})
            # Сохраняем обновленный диалог в Redis
            await state.update_data(dialog=dialog)
            await bot.delete_message(chat_id=message.chat.id, message_id=loading_message.message_id)
            await message.answer(assistant_message, parse_mode=ParseMode.MARKDOWN)
        else:
            await message.answer("Ошибка при получении ответа от YandexGPT API.")
    else:
        await message.answer("Ошибка при получении ответа от YandexGPT API.")

    await state.set_state(ChatStates.waiting_for_question)


def setup_handlers(dispatcher):
    dispatcher.message.register(send_welcome, Command(commands=['start']))
    dispatcher.message.register(yandexgpt_start, lambda message: message.text == 'YandexGPT')
    dispatcher.message.register(handle_question, ChatStates.waiting_for_question)