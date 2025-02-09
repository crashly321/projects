import telebot
import webbrowser

import users_list


'''
python3 /Users/cryashly/Documents/gitRepositories/Codein/projects/PY/BOT/testbot.py
'''

bot = telebot.TeleBot('7575636058:AAGYv7xtuCrY6hR2KS-uq4J5wI68AphgeEQ')
users = users_list.user_list

@bot.message_handler(content_types=['text'])
def start(message): # основная менюшка с командами
    match message.text:
        case '/start':
            bot.send_message(message.from_user.id, 'Можешь написать /help')
            bot.register_next_step_handler(message, start)
        case '/help':
            bot.send_message(message.from_user.id, 'Список команд:\n/start - начало\n/help - помощь\n/reg - регистрация пользователя\n/id - узнать свой айди')
            if message.from_user.id in users_list.admins:
                bot.send_message(message.from_user.id, 'Список команд для МОДЕРАТОРА!!!\n/list - список пользователей\n/user_del - удалить пользователя\n/add_admin - добавить пользователя в админ панель')
        case '/reg':
            bot.send_message(message.from_user.id, 'Регаем нового юзера, мне понадобится Имя, Фамилия и возраст!\nКак вас зовут?')
            bot.register_next_step_handler(message, name)
        case '/id':
            bot.send_message(message.from_user.id, f'ID - {message.from_user.id}')
            print(f'\nЗапросили айди {message.from_user.username}\n')
            if message.from_user.id in users_list.admins:
                bot.send_message(message.from_user.id, "You in admin's group!")
        case '/siteX':
            webbrowser.open('https://crucialexperiments.com/')

    if message.text == '/list' and message.from_user.id in users_list.admins:
        listing = 'Пользователи:\n'
        admin_list = 'МОДЕРАТОРЫ!\n'
        for user in users:
            listing += f'Пользователь @{user}:\nИмя: {users[user]['имя']}, Фамилия: {users[user]['фамилия']}, Возраст: {users[user]['возраст']}\n\n'
        for i in users_list.admins:
            admin_list += f'ID - {i}\n'
        bot.send_message(message.from_user.id, f'{listing}\n\n{admin_list}')
    elif message.text == '/add_admin' and message.from_user.id in users_list.admins:
        bot.send_message(message.from_user.id, 'Введите айди пользователя для добавления в список модерации:')
        bot.register_next_step_handler(message, add_admin)


def name(message): # метод получает имя
    global nameus
    nameus = message.text
    
    bot.send_message(message.from_user.id, 'Какая у вас фамилия?')
    bot.register_next_step_handler(message, sur_name)
def sur_name(message): # метод получает фамилию
    global users
    global sur_nameus
    sur_nameus = message.text
    
    bot.send_message(message.from_user.id, 'Сколько вам лет?')
    bot.register_next_step_handler(message, age)
def age(message): # метод получает возраст
    global ageus
    ageus = message.text

    bot.send_message(message.from_user.id, f'Отлично, ваши данные:\n\nИмя : {nameus}, Фамилия : {sur_nameus}, Возраст : {ageus}\n\nДля сохранения напишите - "Сохраняю", для отмены - "Отмена"')
    bot.register_next_step_handler(message, choice_save)
def choice_save(message): # метод выбирает сохранить или отменить регистрацию
    global choice
    message.from_user.username
    choice = message.text.lower()
    if choice in ['сохраняю']:
        users[f'{message.from_user.username}({message.from_user.id})'] = {'имя' : f'{nameus}', 'фамилия' : f'{sur_nameus}', 'возраст' : f'{ageus}'}
        bot.send_message(message.from_user.id, f'Сохранено...\nИмя: {nameus}, Фамилия: {sur_nameus}, Возраст: {ageus}')
        bot.register_next_step_handler(message, start)
    elif choice in ['отмена']:
        bot.send_message(message.from_user.id, 'Отменено...')
        bot.register_next_step_handler(message, start)
    elif choice not in ['сохраняю', 'отмена']:
        bot.send_message(message.from_user.id, 'Отменено...')
        bot.register_next_step_handler(message, start)

def add_admin(message): # добавление нового адмена
    new_admin = message.text
    users_list.admins.append(int(new_admin))
    bot.send_message(message.from_user.id, f'Новая ячейка привелигированного общества: {new_admin}')
    bot.register_next_step_handler(message, start)
    
bot.polling(none_stop=True)