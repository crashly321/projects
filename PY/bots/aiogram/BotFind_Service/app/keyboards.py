from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardMarkup, InlineKeyboardButton)

first_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Хочу найти сервис')],
    [KeyboardButton(text='О нас'), KeyboardButton(text='Контакты')],
    [KeyboardButton(text='Работать с нами')]
],
resize_keyboard=True, input_field_placeholder='Выберите пункт...', one_time_keyboard=True)

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Найти сервис')],
    [KeyboardButton(text='О нас'), KeyboardButton(text='Контакты')],
    [KeyboardButton(text='Работать с нами')]
],
resize_keyboard=True, input_field_placeholder='Выберите пункт...')

give_contact = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Поделиться номером...', request_contact=True)]
],
resize_keyboard=True, input_field_placeholder='Номерок? >_<', one_time_keyboard=True)

give_location = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Поделиться гео-локацией...', request_location=True)]
],
resize_keyboard=True, input_field_placeholder='Где вы живете?', one_time_keyboard=True)

give_accept = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Подтверждаю'), KeyboardButton(text='Отмена')],
    [KeyboardButton(text='Указать город самостоятельно')]
],
resize_keyboard=True, input_field_placeholder='Выберите пункт...', one_time_keyboard=True)

privacy_keyboard_check = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Пользовательское соглашение...', callback_data='check_privacy')]
])

privacy_keyboard_check_back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='К регистрации', callback_data='check_privacy_back')]
])
#