import telebot
from telebot import types
import user_list

bot = telebot.TeleBot('7575636058:AAGYv7xtuCrY6hR2KS-uq4J5wI68AphgeEQ')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Присылайте мне фото!')

@bot.message_handler(content_types=['photo'])
def answer(message):
    markup = types.InlineKeyboardMarkup()
    btn_edit = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
    btn_del = types.InlineKeyboardButton('Удалить фото', callback_data='delete')
    btn_help = types.InlineKeyboardButton('Помощь', callback_data='help')
    markup.row(btn_edit, btn_del)
    markup.row(btn_help)
    bot.send_message(message.chat.id, 'ахуеть красиво', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    match callback.data:
        case 'delete':
            bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
        case 'edit':
            markup = answer.markup
            bot.edit_message_text('edited text', callback.message.chat.id, callback.message.message_id, reply_markup=markup)
        case 'help':
            markup = types.InlineKeyboardMarkup()
            btn_back = types.InlineKeyboardButton('Назад', callback_data='back')
            markup.row(btn_back)
            bot.edit_message_text('help not found', callback.message.chat.id, callback.message.message_id, reply_markup=markup)
        case 'back':
            bot.edit_message_text('back not found', callback.message.chat.id, callback.message.message_id)

bot.infinity_polling()