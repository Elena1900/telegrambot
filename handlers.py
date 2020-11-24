from glob import glob
import logging
import os
from random import choice

from db import db, get_or_create_user, subscribe_user, unsubscribe_user, save_cat_image_vote, user_voted, get_image_rating
from utils import is_cat, play_random_numbers, main_keyboard, cat_rating_inline_keyboard
from jobs import alarm


def greet_user(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    text = 'Вызван /start'
    logging.info(text)
    update.message.reply_text(
        f"Здравствуй, пользователь {user['emoji']}!",
        reply_markup=main_keyboard()
        )


def talk_to_me(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    user_text = "Привет {}! Ты написал: {}".format(update.message.chat.first_name, update.message.text)
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                 update.message.chat.id, update.message.text)
    update.message.reply_text(f"{user_text} {user['emoji']}", reply_markup=main_keyboard())   


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

    update.message.reply_text(message, reply_markup=main_keyboard())


def send_cat_picture(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    cat_photos_list = glob('images/*cat.jpg')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    if user_voted(db, cat_pic_filename, user["user_id"]):
        rating = get_image_rating(db, cat_pic_filename)
        keyboard = None
        caption = f"Рейтинг картинки {rating}"
    else:
        keyboard = cat_rating_inline_keyboard(cat_pic_filename)
        caption = None 
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'),
                           reply_markup=keyboard, caption=caption)


def user_coordinates(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {user['emoji']}!",
        reply_markup=main_keyboard()
    )


def check_user_photo(update, context):
    update.message.reply_text("Обрабатываем фотографии")
    os.makedirs("downloads", exist_ok=True)
    user_photo = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join("downloads", f"{user_photo.file_id}.jpg")
    user_photo.download(file_name)
    if is_cat(file_name):
        update.message.reply_text("Обнаружен котик, добавляю в библиотеку.")
        new_filename = os.path.join("images", f"{user_photo.file_id}_cat.jpg")
        os.rename(file_name, new_filename)
    else:
        os.remove(file_name)
        update.message.reply_text("Котик не обнаружен!")


def subscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    subscribe_user(db, user)
    update.message.reply_text("Вы успешно подписались")


def unsubscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    unsubscribe_user(db, user)
    update.message.reply_text("Вы успешно отписались")


def set_alarm(update, context):
    try:
        alarm_seconds = abs(int(context.args[0]))
        context.job_queue.run_once(alarm, alarm_seconds, context=update.message.chat.id)
        update.message.reply_text(f"Уведомление через {alarm_seconds} секунд")
    except(ValueError, TypeError):
        update.message.reply_text("Введите целое число секунд после команды")


def cat_picture_rating(update, context):
    update.callback_query.answer()
    callback_type, image_name, vote = update.callback_query.data.split("|")
    vote = int(vote)
    user = get_or_create_user(db, update.effective_user, update.effective_chat.id)
    save_cat_image_vote(db, user, image_name, vote)
    rating = get_image_rating(db, image_name)
    update.callback_query.edit_message_caption(caption=f"Рейтинг картинки {rating}")
