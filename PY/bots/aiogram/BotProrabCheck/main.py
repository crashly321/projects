import asyncio
from aiogram import Bot, Dispatcher, F

from app.handlers import router

async def main():
    bot = Bot(token='7575636058:AAGYv7xtuCrY6hR2KS-uq4J5wI68AphgeEQ')
    dp = Dispatcher()
    dp.include_router(router)
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print('Выключил ботика!')

if __name__ == '__main__':
    asyncio.run(main())