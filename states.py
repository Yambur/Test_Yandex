"""from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


class DialogStates(StatesGroup):
    waiting_for_input = State()
"""

from aiogram.dispatcher.filters.state import StatesGroup, State


class ChatStates(StatesGroup):
    YANDEX_GPT_CHAT = State()
