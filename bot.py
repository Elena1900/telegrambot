import logging
from emoji import emojize
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from glob import glob
from random import randint, choice
import settings

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']    

def greet_user(update, context):
    text = 'Вызван /start'
    logging.info(text)
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Здравствуй, пользователь {context.user_data['emoji']}!")

def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    user_text = "Привет {}! Ты написал: {}".format(update.message.chat.first_name, update.message.text)
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                update.message.chat.id, update.message.text)
    update.message.reply_text(f"{user_text} {context.user_data['emoji']}")
    

def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f"Ваше число {user_number}, моё {bot_number}, вы выйграли"
    elif user_number == bot_number   :
        message = f"Ваше число {user_number}, моё {bot_number}, ничья" 
    else:
        message = f"Ваше число {user_number}, моё {bot_number}, вы проиграли"   
    return message

def send_cat_picture(update, context):
    cat_photos_list = glob('images/*cat.jpg')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))  

def guess_number(update, context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except(TypeError, ValueError):
            message = "Введите целое число"   
    else:
        message = "Введите целое число"

    update.message.reply_text(message)             


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('cat', send_cat_picture))
    dp.add_handler(CommandHandler('guess', guess_number))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()

if __name__ =="__main__":
    main()  