from aiogram.fsm.state import State, StatesGroup

class reg_user(StatesGroup):
	name = State()
	number = State()
	location = State()
	accept = State()
	city_accept = State()

class find_service(StatesGroup):
	set_device = State()
	