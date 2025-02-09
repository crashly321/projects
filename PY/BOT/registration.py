import telebot
import users_list

bot = telebot.TeleBot('7575636058:AAGYv7xtuCrY6hR2KS-uq4J5wI68AphgeEQ')
users = users_list.user_list


@bot.message_handler(content_types=['text'])
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

def choice_save(message): # метод выбирает сохранить или отменить
    global choice
    message.from_user.username
    choice = message.text.lower()
    if choice in ['сохраняю']:
        users[f'{message.from_user.username}({message.from_user.id})'] = {'имя' : f'{nameus}', 'фамилия' : f'{sur_nameus}', 'возраст' : f'{ageus}'}
        bot.send_message(message.from_user.id, f'Сохранено...\nИмя: {nameus}, Фамилия: {sur_nameus}, Возраст: {ageus}')
    elif choice in ['отмена']: bot.send_message(message.from_user.id, 'Отменено...')
    elif choice not in ['сохраняю', 'отмена']: bot.send_message(message.from_user.id, 'Отменено...')


bot.infinity_polling()