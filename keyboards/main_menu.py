"""Файл с основными кнопками основного меню
функции возвращают Inline кнопки
"""

from aiogram import Bot
from aiogram.types import BotCommand
from lexicon.lexicon import LEXICON_COMMANDS, LEXICON
from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)


# Функция для настройки кнопки Menu бота (комманды)
async def set_main_menu(bot: Bot):
    main_menu_commands = [BotCommand(
        command=command,
        description=description
    ) for command,
        description in LEXICON_COMMANDS.items()]
    await bot.set_my_commands(main_menu_commands)

#Функция для создания кнопок основного меню, после регистрации пользователя
def main_menu_reg():
    services_button = InlineKeyboardButton(
        text=LEXICON['services'],
        callback_data='services'   
    )
    
    make_appointment_button = InlineKeyboardButton(
        text=LEXICON['Make an appointment'],
        callback_data='make_appointment'
    )
    reviews_button = InlineKeyboardButton(
        text=LEXICON['Reviews'],
        callback_data='reviewsent'
    )
    pay_button = InlineKeyboardButton(
        text=LEXICON['Pay'],
        callback_data='pay'
    )
    showdata_button = InlineKeyboardButton(
        text=LEXICON['show_profile'],
        callback_data='showdata'   
    )
    
    shedule_button = InlineKeyboardButton(
        text=LEXICON['shedule'],
        callback_data='shedule'   
    )
    # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
    keyboard: list[list[InlineKeyboardButton]] = [
        [services_button, make_appointment_button],
        [reviews_button,pay_button],
        [showdata_button],
        [shedule_button]
    ]
    # Создаем объект инлайн-клавиатуры
    menu_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return menu_markup
    
#Функция для создания кнопок основного меню, до  регистрации пользователя
def main_menu_no_reg():
    registracio_button = InlineKeyboardButton(
        text=LEXICON["registracio"],
        callback_data='registracio'   
    )
    
    services_button = InlineKeyboardButton(
        text=LEXICON['services'],
        callback_data='services'
    )
    reviews_button = InlineKeyboardButton(
        text=LEXICON['Reviews'],
        callback_data='reviewsent'
    )

    # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
    keyboard: list[list[InlineKeyboardButton]] = [
        [registracio_button],
        [services_button, reviews_button]

    ]
    # Создаем объект инлайн-клавиатуры
    menu_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return menu_markup