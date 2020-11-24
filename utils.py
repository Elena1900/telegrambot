from clarifai.rest import ClarifaiApp
from random import randint

from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

import settings


def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f"Ваше число {user_number}, моё {bot_number}, вы выйграли"
    elif user_number == bot_number   :
        message = f"Ваше число {user_number}, моё {bot_number}, ничья" 
    else:
        message = f"Ваше число {user_number}, моё {bot_number}, вы проиграли"   
    return message


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Прислать котика', KeyboardButton('Мои координаты', request_location=True), 'Заполнить анкету']
        ])


def is_cat(file_name):
    image_has_cat = False
    app = ClarifaiApp(api_key=settings.CLARIFAI_API_KEY)
    model = app.public_models.general_model
    response = model.predict_by_filename(file_name, max_concepts=5)
    if response['status']['code'] == 10000:
        for concept in response['outputs'][0]['data']['concepts']:
            if concept['name'] == 'cat':
                image_has_cat = True
    return image_has_cat


def cat_rating_inline_keyboard(image_name):
    callback_text = f"rate|{image_name}|"
    keyboard = [
        [
            InlineKeyboardButton('нравится', callback_data=callback_text + "1"),
            InlineKeyboardButton('не нравится', callback_data=callback_text + "-1")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


if __name__ == "__main__":
    print(is_cat('images/big_cat.jpg'))

