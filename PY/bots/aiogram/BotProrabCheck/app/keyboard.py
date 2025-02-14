from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[
    [KeyboardButton(text='Каталог')],
    [KeyboardButton(text='Контакты'), KeyboardButton(text='О нас')]
    ],
    resize_keyboard=True, input_field_placeholder='Выбери пункт...'
) # input_field_placeholder меняет текст над кнопками, но в приложении под мак этого по какой-то причине не видно(хз баг ебаный)


catalog = InlineKeyboardMarkup(
    inline_keyboard=[
    [InlineKeyboardButton(text='Глэки', callback_data='Glock'), InlineKeyboardButton(text='Крэки', callback_data='Crack')],
    [InlineKeyboardButton(text='Открывашки', callback_data='lockpick')]
    ]
)

back = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='back')]
    ]
)