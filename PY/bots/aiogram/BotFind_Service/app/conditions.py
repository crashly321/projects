from aiogram.fsm.state import State, StatesGroup

class reg_user(StatesGroup):
	name = State()
	number = State()
	location = State()
	accept = State()
