from datetime import datetime
from db import db, get_subscribed

from telegram.error import BadRequest


def send_updates(context):
    text = "Сейчас " + datetime.now().strftime('%d.%m.%Y %H:%M:%s')
    for user in get_subscribed(db):
        try:
            context.bot.send_message(chat_id=user['chat_id'], text=text)
        except BadRequest:
            print(f"Чат {user['chat_id']} не найден")


def alarm(context):
    context.bot.send_message(chat_id=context.job.context, text="Сработал будильник!")
