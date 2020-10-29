import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from handlers import greet_user, guess_number, send_cat_picture, talk_to_me, user_coordinates
import settings

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )



def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    logging.info('Бот стартовал')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_cat_picture))
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать котика)$'), send_cat_picture))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()

if __name__ =="__main__":
    main()  