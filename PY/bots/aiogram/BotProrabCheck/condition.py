from aiogram.fsm.state import State, StatesGroup


class register(StatesGroup):
    name = State()
    age = State()
    number = State()
