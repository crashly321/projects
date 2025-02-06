import telebot
# python3 /Users/cryashly/Documents/gitRepositories/Codein/projects/PY/BOT/testbot.py
bot = telebot.TeleBot('7575636058:AAGYv7xtuCrY6hR2KS-uq4J5wI68AphgeEQ')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text in ['Привет', 'привет']:
        bot.send_message(message.from_user.id, 'Прив, можешь написать /help')
    elif message.text in ['/help']:
        bot.send_message(message.from_user.id, 'Пока что разраб(уебан) разрешил мне отвечать только на приветы')
    else:
        bot.send_message(message.from_user.id, 'Хз че тебе сказать, отвечаю ток на привет')

bot.polling(none_stop=True, interval=0)