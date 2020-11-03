from glob import glob
import logging
import os
from random import choice

from utils import get_smile, is_cat, play_random_numbers, main_keyboard


def greet_user(update, context):
    text = 'Вызван /start'
    logging.info(text)
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(
        f"Здравствуй, пользователь {context.user_data['emoji']}!",
        reply_markup=main_keyboard()
        )


def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    user_text = "Привет {}! Ты написал: {}".format(update.message.chat.first_name, update.message.text)
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                update.message.chat.id, update.message.text)
    update.message.reply_text(f"{user_text} {context.user_data['emoji']}", reply_markup=main_keyboard())        


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
    cat_photos_list = glob('images/*cat.jpg')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'), reply_markup=main_keyboard())  


def user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {context.user_data['emoji']}!",
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

