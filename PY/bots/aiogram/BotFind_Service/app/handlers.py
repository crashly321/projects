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
global user_data
user_data = {}

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

@router.message(F.text == 'О нас')
async def about_me(message: Message):
    await message.answer('Наш сервис выступает посредником между клиентом и мастером, для более простого поиска наиболее подходящего места, по вашему запросу!')

@router.message(F.text == 'Контакты')
async def contact_me(message: Message):
    await message.answer('Связаться с нами можно по данной почте:\nnashapochta@gmail.com')

@router.message(F.text == 'Работать с нами')
async def work_with_me(message: Message):
    await message.answer('Круто что вы решили расширить свои охваты!')
    await message.answer(
        'Что мы можем предложить развивающемуся бизнесу:\n- Реклама(размещение вашей компании в наших списках)\n- Повышение в списке относительно оценки от пользователей\n- Удобное получение заказов\n- Информация о клиенте(контакты, отзывы от других мастеров)')
    await message.answer('Если вы заинтерисованы, для дальнейшего обсуждения просим связаться с нами по почте: rabochiychat_FindService@gmail.com\nВ письме укажите свои контактные данные - телеграм')


# ловля состояний регистрации пользователя:
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
    
    global user_data
    user_data[message.from_user.id] = await state.get_data()

    await state.set_state(conditions.reg_user.accept)
    await message.answer(f'Что я должен запомнить:', reply_markup=kb.give_accept)
    await message.answer(f'Ваше ФИО: {user_data[message.from_user.id]['name']}\nВаш номер телефона: {user_data[message.from_user.id]['number']}\nВаш город: {user_data[message.from_user.id]['location']}\nПодтвердите регистрацию...\n(Нажав "Подтверждаю", вы принимаете пользовательское соглашение о обработке персональных данных)', reply_markup=kb.privacy_keyboard_check)

@router.message(conditions.reg_user.accept, F.text.in_({'Подтверждаю', 'Отмена', 'Указать город самостоятельно'}))
async def reg_user_accept(message: Message, state: FSMContext):
    solution = message.text

    if solution == 'Подтверждаю':
        await state.clear()
        await message.answer('Ну кайф', reply_markup=kb.main_keyboard)
    elif solution == 'Отмена':
        await state.clear()
        await message.answer('Начните регистрацию с начала', reply_markup=kb.first_keyboard)
    elif solution == 'Указать город самостоятельно':
        await state.set_state(conditions.reg_user.city_accept)
        await message.answer('Какой  город вы хотите указать? От этого будут зависеть рекомендации!')
    
@router.message(conditions.reg_user.city_accept, F.text)
async def reg_user_city_accept(message: Message, state: FSMContext):
    await state.update_data(location=message.text)

    global user_data
    user_data[message.from_user.id] = await state.get_data()
    await state.set_state(conditions.reg_user.accept)
    await message.answer(f'Что я должен запомнить:', reply_markup=kb.give_accept)
    await message.answer(f'Ваше ФИО: {user_data[message.from_user.id]['name']}\nВаш номер телефона: {user_data[message.from_user.id]['number']}\nВаш город: {user_data[message.from_user.id]['location']}\nПодтвердите регистрацию...\n(Нажав "Подтверждаю", вы принимаете пользовательское соглашение о обработке персональных данных)', reply_markup=kb.privacy_keyboard_check)



@router.callback_query(F.data == 'check_privacy')
async def user_privacy(callback: CallbackQuery):
    await callback.answer('Вы открыли пользовательское соглашение...')
    await bot.edit_message_text(chat_id=callback.message.chat.id, 
                                message_id=callback.message.message_id, 
                                text='Пользовательское соглашение:\n1. Общие положения\n1.1. Администрация обязуется соблюдать конфиденциальность персональных данных Пользователя и обеспечивать их защиту в соответствии с действующим законодательством Российской Федерации и настоящим Соглашением.\n1.2. Персональные данные — это любая информация, относящаяся к прямо или косвенно определенному или определяемому физическому лицу (Пользователю).\n1.3. Обработка персональных данных включает сбор, запись, систематизацию, накопление, хранение, уточнение, извлечение, использование, передачу, обезличивание, блокирование, удаление и уничтожение данных.\n\n2. Цели обработки персональных данных\n2.1. Администрация обрабатывает персональные данные Пользователя для следующих целей:\nпредоставление доступа к функционалу Сервиса; улучшение качества работы Сервиса; отправка уведомлений, запросов и информации, связанной с использованием Сервиса; выполнение обязательств перед Пользователем; проведение статистических и аналитических исследований; соблюдение требований действующего законодательства.\n\n3. Состав персональных данных\n3.1. Администрация может запрашивать и обрабатывать следующие персональные данные:\nфамилия, имя, отчество; адрес электронной почты; номер телефона; данные о местоположении (если предоставлены Пользователем); иные данные, необходимые для выполнения целей, указанных в разделе 2 настоящего Соглашения.\n\n4. Условия обработки персональных данных\n4.1. Обработка персональных данных осуществляется с согласия Пользователя, которое выражается путем использования Сервиса.\n4.2. Администрация вправе передавать персональные данные третьим лицам только в следующих случаях:\nПользователь явно выразил согласие на такую передачу; передача необходима для выполнения обязательств перед Пользователем; передача предусмотрена действующим законодательством.\n4.3. Администрация принимает необходимые организационные и технические меры для защиты персональных данных от несанкционированного доступа, уничтожения, изменения или блокирования.\n\n5. Права Пользователя\n5.1. Пользователь имеет право:\nзапрашивать информацию о своих персональных данных, обрабатываемых Администрацией; требовать уточнения, блокирования или удаления своих персональных данных, если они являются неполными, устаревшими, недостоверными или обрабатываются с нарушением законодательства; отозвать согласие на обработку персональных данных, направив соответствующее уведомление Администрации.\n5.2. Для реализации своих прав Пользователь может обратиться к Администрации по контактным данным, указанным в разделе 7 настоящего Соглашения.\n\n6. Хранение и уничтожение данных\n6.1. Персональные данные Пользователя хранятся в течение срока, необходимого для достижения целей обработки, или до момента отзыва согласия Пользователем.\n6.2. После достижения целей обработки или отзыва согласия персональные данные подлежат уничтожению или обезличиванию.\n\n7. Контактная информация\n7.1. По всем вопросам, связанным с обработкой персональных данных, Пользователь может обратиться к Администрации по следующим контактным данным:\n- Электронная почта: [email@example.com].\n\n8. Заключительные положения\n8.1. Настоящее Соглашение может быть изменено Администрацией в одностороннем порядке. Новая редакция Соглашения вступает в силу с момента ее опубликования на Сайте, если иное не предусмотрено новой редакцией.\n8.2. Продолжение использования Сервиса после внесения изменений в Соглашение означает согласие Пользователя с новой редакцией.\n8.3. Если Пользователь не согласен с условиями настоящего Соглашения, он обязан прекратить использование Сервиса.', 
                                reply_markup=kb.privacy_keyboard_check_back)
    
@router.callback_query(F.data == 'check_privacy_back')
async def user_privacy_back(callback: CallbackQuery):
    global user_data
    await callback.answer('Вы закрыли пользовательское соглашение...')
    await bot.edit_message_text(chat_id=callback.message.chat.id, 
                                message_id=callback.message.message_id, 
                                text=f'Ваше ФИО: {user_data[callback.message.chat.id]['name']}\nВаш номер телефона: {user_data[callback.message.chat.id]['number']}\nВаш город: {user_data[callback.message.chat.id]['location']}\nПодтвердите регистрацию...\n(Нажав "Подтверждаю", вы принимаете пользовательское соглашение о обработке персональных данных)', 
                                reply_markup=kb.privacy_keyboard_check)



