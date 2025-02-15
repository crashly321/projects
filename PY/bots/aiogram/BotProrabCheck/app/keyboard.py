from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from app.database.requests import get_categories, get_category_item
from aiogram.utils.keyboard import InlineKeyboardBuilder

main = ReplyKeyboardMarkup(
    keyboard=[
    [KeyboardButton(text='Каталог')],
    [KeyboardButton(text='Контакты'), KeyboardButton(text='О нас')]
    ],
    resize_keyboard=True, input_field_placeholder='Выбери пункт...'
) # input_field_placeholder меняет текст над кнопками, но в приложении под мак этого по какой-то причине не видно(хз баг ебаный)

back = InlineKeyboardMarkup(
inline_keyboard=[
[InlineKeyboardButton(text='На главную...', 
                      callback_data='to_main')]
]
)

async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, 
                                          callback_data=f'category_{category.id}'))
    return keyboard.adjust(2).as_markup()


async def items(category_id):
    all_items = await get_category_item(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, 
                                          callback_data=f'item_{item.id}'))
    keyboard.add(InlineKeyboardButton(text='На главную...', 
                                      callback_data='to_main'))
    return keyboard.adjust(2).as_markup()

