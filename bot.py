import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from anketa import anketa_start, anketa_name, anketa_rating, anketa_skip, anketa_comment, anketa_dontknow
from handlers import greet_user, guess_number, check_user_photo, send_cat_picture, talk_to_me, user_coordinates
import settings

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )



def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    logging.info('Бот стартовал')
    dp = mybot.dispatcher

    anketa = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Заполнить анкету)$'), anketa_start)
        ],
        states={
            "name": [MessageHandler(Filters.text, anketa_name)],
            "rating": [MessageHandler(Filters.regex('^(1|2|3|4|5)$'), anketa_rating)],
            "comment":[
                CommandHandler('skip', anketa_skip),
                MessageHandler(
                                Filters.text | Filters.video | Filters.photo | Filters.document | Filters.location,
                                anketa_dontknow
                 )
            ]
        },
        fallbacks=[
            MessageHandler(Filters.text, anketa_dontknow)
        ]
    )

    dp.add_handler(anketa)
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_cat_picture))
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать котика)$'), send_cat_picture))
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()

if __name__ =="__main__":
    main()  