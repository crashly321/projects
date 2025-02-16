from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
import requests

import app.keyboards as kb
import app.conditions as conditions

router = Router()
global bot
bot = Bot(token='7575636058:AAGYv7xtuCrY6hR2KS-uq4J5wI68AphgeEQ')


# базовые команды:
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Добро пожаловать, {message.from_user.first_name}!\nУ нас вы сможете найти идеальный тех. сервис для себя. Что вас интерисует?', reply_markup=kb.first_keyboard)

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('В разработке...')


# обработка текстовых команд:
@router.message(F.text == 'Хочу найти сервис')
async def first_time_user(message: Message, state: FSMContext):
    await state.set_state(conditions.reg_user.name)
    await message.answer(
        'Если вы впервые используете наш сервис, понадобится регистрация для дальнейшего использования функционала.\nПожалуйста, напишите ваше "ФИО".\n(Иванов Иван Иванович)')
    # тут допишу переход по состояниям

@router.message(F.text == 'О нас')
async def about_me(message: Message):
    await message.answer('---Информация о нашем сервисе---\nНаш сервис выступает посредником между клиентом и мастером, для более простого поиска наиболее подходящего места, по вашему запросу!')

@router.message(F.text == 'Контакты')
async def contact_me(message: Message):
    await message.answer('Связаться с нами можно по данной почте:\nnashapochta@gmail.com')

@router.message(F.text == 'Работать с нами')
async def work_with_me(message: Message):
    await message.answer('Круто что вы решили расширить свои охваты!')
    await message.answer(
        'Что мы можем предложить развивающемуся бизнесу:\n- Реклама(размещение вашей компании в наших списках)\n- Повышение в списке относительно оценки от пользователей\n- Удобное получение заказов\n- Информация о клиенте(контакты, отзывы от других мастеров)')
    await message.answer('Если вы заинтерисованы, для дальнейшего обсуждения просим связаться с нами по почте: rabochiychat_FindService@gmail.com\nВ письме укажите свои контактные данные - телеграм')


# ловля состояний:
@router.message(conditions.reg_user.name)
async def reg_user_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(conditions.reg_user.number)
    await message.answer(f'Отлично, теперь поделитесь своим номером ;)', reply_markup=kb.give_contact)

@router.message(conditions.reg_user.number, F.contact)
async def reg_user_number(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    await state.set_state(conditions.reg_user.location)
    await message.answer('Осталось указать свой город...', reply_markup=kb.give_location)

@router.message(conditions.reg_user.location, F.location)
async def reg_user_location(message: Message, state: FSMContext):
    # await state.update_data(location=f'{message.location.latitude}, {message.location.longitude}')
    
    
    # кусочек с обработкой адреса через OpenStreetMap
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={message.location.latitude}&lon={message.location.longitude}&zoom=18&addressdetails=1"
    headers = {
        "User-Agent": "FindServiceBot/1.0 (malimama142@gmail.com)"  # Укажи своё приложение и email
    }
    response = requests.get(url, headers=headers).json()

    if 'address' in response:
        address = response['address']
        formatted_address = (
            f"{address.get('city', '')} {address.get('town', '')} {address.get('village', '')}"
        )
        await state.update_data(location=f'{formatted_address.strip()}')
    else:
        await message.answer('К сожалению мы не смогли обнаружить ваш адрес автоматически')
    global reg_data
    reg_data = await state.get_data()
    await state.set_state(conditions.reg_user.accept)
    await message.answer(f'Что я должен запомнить:', reply_markup=kb.give_accept)
    await message.answer(f'Ваше имя: {reg_data['name']}\nВаш номер телефона: {reg_data['number']}\nВаш город: {reg_data['location']}\nПодтвердите регистрацию...\n(Нажав "Подтверждаю", вы принимаете пользовательское соглашение о обработке персональных данных)', reply_markup=kb.privacy_keyboard_check)

@router.message(conditions.reg_user.accept, F.text.in_({'Подтверждаю', 'Отмена'}))
async def reg_user_accept(message: Message, state: FSMContext):
    solution = message.text

    if solution == 'Подтверждаю':
        await message.answer('Ну кайф', reply_markup=kb.main_keyboard)
    elif solution == 'Отмена':
        await message.answer('Начните регистрацию с начала', reply_markup=kb.first_keyboard)

    await state.clear()

@router.callback_query(F.data == 'check_privacy')
async def user_privacy(callback: CallbackQuery):
    await callback.answer('Вы открыли пользовательское соглашение...')
    await bot.edit_message_text(chat_id=callback.message.chat.id, 
                                message_id=callback.message.message_id, 
                                text='Наш скромный каталог товароy:', 
                                reply_markup=kb.privacy_keyboard_check_back)
    
@router.callback_query(F.data == 'check_privacy_back')
async def user_privacy_back(callback: CallbackQuery):
    await callback.answer('Вы закрыли пользовательское соглашение...')
    await bot.edit_message_text(chat_id=callback.message.chat.id, 
                                message_id=callback.message.message_id, 
                                text=f'Ваше имя: {reg_data['name']}\nВаш номер телефона: {reg_data['number']}\nВаш город: {reg_data['location']}\nПодтвердите регистрацию...\n(Нажав "Подтверждаю", вы принимаете пользовательское соглашение о обработке персональных данных)', 
                                reply_markup=kb.privacy_keyboard_check)