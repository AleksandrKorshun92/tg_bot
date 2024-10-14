"""Файл с основными кнопками calback
функции возвращают Inline кнопки
"""

from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)
from function.open_f import open_file_json

# кнопка возврата в основное меню
def menu_start():
# Создаем объекты инлайн-кнопок
    no_reg_button = InlineKeyboardButton(
        text='Вернуться в меню',
        callback_data='start_menu'
    )
    # Добавляем кнопки в клавиатуру 
    keyboard: list[list[InlineKeyboardButton]] = [[no_reg_button]]
    # Создаем объект инлайн-клавиатуры
    menu_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return menu_markup

# кнопки для регистрации пользователя
def menu_reg_start():
    start_button = InlineKeyboardButton(
        text='✅ Начать регистрацию',
        callback_data='start_reg'   
    )
    
    no_reg_button = InlineKeyboardButton(
        text='❌ Нет, вернуться в меню',
        callback_data='no_reg_button'
    )
    # Добавляем кнопки в клавиатуру 
    keyboard: list[list[InlineKeyboardButton]] = [
        [start_button],
        [no_reg_button]
    ]
    # Создаем объект инлайн-клавиатуры
    menu_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return menu_markup


# кнопки выбора образования при регистрации пользователя
def menu_education():
  # Создаем объекты инлайн-кнопок
    secondary_button = InlineKeyboardButton(
        text='Среднее',
        callback_data='Среднее'
    )
    higher_button = InlineKeyboardButton(
        text='Высшее',
        callback_data='Высшее'
    )
    no_edu_button = InlineKeyboardButton(
        text='🤷 Нету',
        callback_data='Нету образование'
    )
    # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
    keyboard: list[list[InlineKeyboardButton]] = [
        [secondary_button, higher_button],
        [no_edu_button]
    ]
    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup

# кнопки выбора просмотра анкеты
def menu_reg():
# Создаем объекты инлайн-кнопок
    showdata_button = InlineKeyboardButton(
        text='Посмотреть анкету',
        callback_data='showdata'  
    )
    
    edit_profile_button = InlineKeyboardButton(
        text='Изменить данные',
        callback_data='edit_profile'  
    )
    
    no_reg_button = InlineKeyboardButton(
        text='Вернуться в меню',
        callback_data='start_menu'
    )
    # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
    keyboard: list[list[InlineKeyboardButton]] = [
        [showdata_button],
        [edit_profile_button],
        [no_reg_button]
    ]
    # Создаем объект инлайн-клавиатуры
    menu_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return menu_markup

# кнопки выбора внесения изменений в анкету профиля
def menu_edit_profile():
# Создаем объекты инлайн-кнопок
    new_registracion_button = InlineKeyboardButton(
        text='Заполнить анкету сначала',
        callback_data='start_reg'  
    )
    
    showdata_button = InlineKeyboardButton(
        text='Посмотреть анкету',
        callback_data='showdata'  
    )
    
    no_reg_button = InlineKeyboardButton(
        text='Вернуться в меню',
        callback_data='start_menu'
    )
    # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
    keyboard: list[list[InlineKeyboardButton]] = [
        [new_registracion_button],
        [showdata_button],
        [no_reg_button]
    ]
    # Создаем объект инлайн-клавиатуры
    menu_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return menu_markup

# кнопки возврата в меню или изменения данных пользователя
def menu_back():
# Создаем объекты инлайн-кнопок
    no_reg_button = InlineKeyboardButton(
        text='Вернуться в меню',
        callback_data='start_menu'
    )
    
    edit_profile_button = InlineKeyboardButton(
        text='Изменить данные',
        callback_data='edit_profile'  
    )
    # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
    keyboard: list[list[InlineKeyboardButton]] = [
        [edit_profile_button],
        [no_reg_button]
    ]
    # Создаем объект инлайн-клавиатуры
    menu_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return menu_markup

# кнопки выбора услуг 
def menu_services():
# Создаем объекты инлайн-кнопок
    file = open_file_json("database/services.json")
    """________________________
    ТУТ надо подумать, как сделать, чтобы список был из количества Не получается - [[]] * len(file.keys())"""
    keyboard: list[list[InlineKeyboardButton]] = [[], [], [], [], [], [], [], []]
    count = 0 
    for k in file:
        k = InlineKeyboardButton(
        text=file[k],
        callback_data=k
        )    
        keyboard[count].append(k)
        count+=1
    menu_buton = InlineKeyboardButton(
        text='Вернуться в меню',
        callback_data='start_menu'
    )
    keyboard[7].append(menu_buton)
    # Создаем объект инлайн-клавиатуры
    menu_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return menu_markup


# кнопки выбора кабинета (зала) расписаний 
def menu_shedule():
# Создаем объекты инлайн-кнопок
    file = open_file_json("database/shedule.json")
    """________________________
    ТУТ надо подумать, как сделать, чтобы список был из количества Не получается - [[]] * len(file.keys())"""
    keyboard: list[list[InlineKeyboardButton]] = [[], [], [], [], [], [], [], [], [], [], [], [],[]]
    count = 0 
    for k in file:
        k = InlineKeyboardButton(
        text=file[k],
        url='https://schedule.arbitr.ru/Schedule/Operator/?courtTag=SPB&cabinetName='+k
        )    
        keyboard[count].append(k)
        count+=1
    menu_buton = InlineKeyboardButton(
        text='Вернуться в меню',
        callback_data='start_menu'
    )
    keyboard[12].append(menu_buton)
    # Создаем объект инлайн-клавиатуры
    menu_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return menu_markup

# кнопки вперехода на сайт отзывов 
def menu_reviews():
# Создаем объекты инлайн-кнопок
    reviews_button = InlineKeyboardButton(
        text='Переход на сайт отзывов',
        url='https://uslugi.yandex.ru/profile/EvgenijChekan-2594577'
    )
    menu_buton = InlineKeyboardButton(
        text='Вернуться в меню',
        callback_data='start_menu'
    )
    # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
    keyboard: list[list[InlineKeyboardButton]] = [
        [reviews_button], [menu_buton]
    ]
    # Создаем объект инлайн-клавиатуры
    menu_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return menu_markup