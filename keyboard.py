from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    menu = ReplyKeyboardMarkup(resize_keyboard=True)
    menu.add(KeyboardButton('YandexGPT'))
    menu.add(KeyboardButton('Скоро...'))
    return menu
