import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.database.models import async_main

async def main():
	bot = Bot(token='7575636058:AAGYv7xtuCrY6hR2KS-uq4J5wI68AphgeEQ')
	dp = Dispatcher()
	dp.include_router(router)

	await async_main()
	await dp.start_polling(bot)
	

if __name__ == '__main__':
	asyncio.run(main())