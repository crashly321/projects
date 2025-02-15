from aiogram import F, Router, Bot 
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

import app.keyboard as kb
import app.database.requests as rq

router = Router()
global bot
bot = Bot(token='7575636058:AAGYv7xtuCrY6hR2KS-uq4J5wI68AphgeEQ')



@router.message(CommandStart())
async def start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Добро пожаловать!', reply_markup=kb.main)


@router.message(Command('help'))
async def help(message: Message):
    await message.reply(f'Пока что ты можешь использовать только /start')



@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Наш скромный каталог брендов:', reply_markup=await kb.categories())
    
@router.message(F.text == 'Контакты')
async def catalog(message: Message):
    await message.answer('Номер телефона: 8-900-555-55-35\nЭлектронная почта: tochnonenaeb@naeb.com')

@router.message(F.text == 'О нас')
async def catalog(message: Message):
    await message.answer('Мы сильные и независимые люди!')




@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('Вы выбрали бренд!')
    await bot.edit_message_text(chat_id=callback.message.chat.id, 
                                message_id=callback.message.message_id, 
                                text='Товары данного бренда:', 
                                reply_markup=await kb.items(callback.data.split('_')[1]))

@router.callback_query(F.data.startswith('item_'))
async def category(callback: CallbackQuery):
    item_data = await rq.get_item(callback.data.split('_')[1])

    await callback.answer('Вы выбрали товар!')
    await bot.edit_message_text(chat_id=callback.message.chat.id, 
                                message_id=callback.message.message_id, 
                                text=f'Название: {item_data.name}, цена: {item_data.price}₽\nОписание:\n{item_data.description}', 
                                reply_markup=kb.back)


@router.callback_query(F.data == 'to_main')
async def back_to_main(callback: CallbackQuery):
    await callback.answer('Вы вернулись!')
    await bot.edit_message_text(chat_id=callback.message.chat.id, 
                                message_id=callback.message.message_id, 
                                text='Наш скромный каталог брендов:', 
                                reply_markup=await kb.categories())
