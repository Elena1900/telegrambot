from datetime import datetime
from db import db, get_subscribed

from telegram.error import BadRequest


def send_updates(context):
    text = "Сейчас " + datetime.now().strftime("%D.%m.%Y %H:%M:%S")
    for user in get_subscribed(db):
        try:
            context.bot.send_message(chat_id=user['chat_id'], text=text)
        except BadRequest:
            print(f"Чат {user['chat_id']} не найден")


def alarm(context):
    context.bot.send_message(chat_id=context.job.context, text="Сработал будильник!")


def send_hello(context):
    context.bot.send_message(chat_id=1001192227, text='Привет!')
