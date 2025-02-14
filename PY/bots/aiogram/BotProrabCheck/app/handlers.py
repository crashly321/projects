import asyncio
from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

import app.keyboard as kb

router = Router()
global bot
bot = Bot(token='7575636058:AAGYv7xtuCrY6hR2KS-uq4J5wI68AphgeEQ')

@router.message(CommandStart())
async def start(message: Message):
    await message.answer('привет', reply_markup=kb.main)
    await message.answer('Наш скромный каталог товаров:', reply_markup=kb.catalog)
    print(f'\n\n\nПользователь {message.from_user.username}-{message.from_user.id} воспользовался ботом!\n\n\n')

@router.message(Command('help'))
async def help(message: Message):
    await message.reply(f'Пока что ты можешь использовать только /start')

@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Наш скромный каталог товаров:', reply_markup=kb.catalog)
    
@router.message(F.text == 'Контакты')
async def catalog(message: Message):
    await message.answer('Номер телефона: 8-900-555-55-35\nЭлектронная почта: tochnonenaeb@naeb.com')

@router.message(F.text == 'О нас')
async def catalog(message: Message):
    await message.answer('Мы сильные и независимые люди!')


@router.callback_query(F.data == 'Glock')
async def cat_glock(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию "Глэки"')
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="Пшлнх, ты не нигга!", reply_markup=kb.back)

@router.callback_query(F.data == 'Crack')
async def cat_glock(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию "Крэки"')
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Только с разрешения главного нигги!', reply_markup=kb.back)

@router.callback_query(F.data == 'lockpick')
async def cat_glock(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию "Открывашки"')
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Пшлнх, ты не нигга!', reply_markup=kb.back)

@router.callback_query(F.data == 'back')
async def cat_glock(callback: CallbackQuery):
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Наш скромный каталог товароy:', reply_markup=kb.catalog)