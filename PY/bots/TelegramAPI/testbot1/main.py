import logging
import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler, CallbackQueryHandler, CallbackContext

import users_list




# если что-то ломается - эта функция пишет что и где
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# эта функция отвечает за действия команды start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            telegram.InlineKeyboardButton("Регистрация", callback_data="registration"),
            telegram.InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [
            telegram.InlineKeyboardButton("Option 3", callback_data="3")
        ],
    ]
    start_markup = telegram.InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text="Я одинокий ботик которого написали на новой библиотеке\n(старой просто более функциональной)", reply_markup=start_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    application = ApplicationBuilder().token('7575636058:AAGYv7xtuCrY6hR2KS-uq4J5wI68AphgeEQ').build()
    query = update.callback_query

    await query.answer()
    print(f'\n\n\nКнопка - {query.data}\n\n\n')

    if query.data == 'registration':
        await query.edit_message_text(text=f"Окей, регаемся. Напиши для начала свое имя, я жду!")
        await application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reg_name(update, context)))
        print(update)

    elif query.data == '2':
        print(f'\n\n{update}\n\n')

def reg_name(update: Update, context:CallbackContext):
    
    print(f'\n\n\nreg_name\n\n\n')
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Хорошо твое имя - {update.effective_chat.first_name}\nТеперь напиши свой номер!'
    )


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text=' '.join(context.args).upper())

# функция на случай не найденой команды
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text="Ниче не пон(")

# тут мы объявляем токен бота и указываем функции присвоенные к командам
def main():
    application = ApplicationBuilder().token('7575636058:AAGYv7xtuCrY6hR2KS-uq4J5wI68AphgeEQ').build()

    start_handler = CommandHandler('start', start)
    caps_handler = CommandHandler('caps', caps)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(caps_handler)

    application.add_handler(unknown_handler) # кусок включающийся в случае если команда не найдена(обязательно в конце так как должен проверяться последним)
    
    application.run_polling()

if __name__ == '__main__':
    main()
    