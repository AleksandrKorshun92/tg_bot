""" 
В этом блоке настроены функции для админа
- сделаны фильтры, которые сравнивают от кого сообщение поступает (от админа или нет), если от админа
то возвращают словари со значениями, которые используются в дальнейших хэндлерах.
"""

from aiogram import F, Router, Bot
from aiogram.filters import BaseFilter
from aiogram.types import Message
from config_data.config import load_admin
from database.sqlite3 import load_user_all, load_id_from_name, load_appointments
from keyboards.keybords import menu_start
from datetime import date

r = Router()

# загружаем список админов
admin_id_load = load_admin()
admin_id_list = [int(x) for x in admin_id_load]

# Фильтр парсит из базы данных по имени id пользователя и текст сообщения
# 1 вариант Сообщение формата "Сообщение отправить - ИМЯ следующего содержания : ТЕКС СООБЩЕНИЯ"
# 2 вариант Сообщение формата "посмотреть анкету - ИМЯ"
class DefinitionIDUserFilter(BaseFilter):
    # создает аргумент id админов
    def __init__(self, admi_id) -> None:
        self.admin_id = admi_id
   
    # Call чтобы можно было вызывать () данный класс
    async def __call__(self, message:Message) -> bool | dict[str, str]:
        # проверяет от кого пришло сообщение, если от админа - то выполянется код
        if message.from_user.id in self.admin_id:
            print(message.from_user.id)
            res_dict = {}
            
            # разбивает сообщение на список строк
            list_message = message.text.split()
            print(list_message)
            for word in list_message:
                if word == '-':
                    res_dict["name"] = list_message[list_message.index(word)+1]
                    # находит в базе данных id пользователя по имени
                    res_dict["id_other"] = await load_id_from_name(res_dict["name"])
                if word == ':':
                    # записывает в словарь текст сообщения, который нужно отрпавить пользователю
                    res_dict["mes_text"] = ' '.join(list_message[list_message.index(word)+1:])
            # Возвращает словарь с ключами, которые передаются в хэндлер
            return res_dict
        else:
            return False 


# Фильтр парсит дату и возвращает дату
# 1 вариант Сообщение формата "посмотреть записи - ДАТА ФОРМАТА ДД.ММ.ГГГГ или написать сегодня"
class AppointmentsFilter(BaseFilter):
    def __init__(self, admi_id) -> None:
        self.admin_id = admi_id
    
    # Call чтобы можно было вызывать () данный класс
    async def __call__(self, message:Message) -> bool | dict[str, str]:
        # проверяет от кого пришло сообщение, если от админа - то выполянется код
        if message.from_user.id in self.admin_id:
            res_dict = {}
            list_message = message.text.split()
            today = 'сегодня'
            # Если в сообение написано сегодня, то определяет дату сегодня 
            if today in list_message:
                res_dict['day'] = date.today().strftime("%d.%m.%Y")
            # Определяет дату 
            elif today not in list_message:
                for word in list_message:
                    if word == '-':
                        res_dict["day"] = list_message[list_message.index(word)+1]
            # Возвращает словарь с ключами, которые передаются в хэндлер
            return res_dict
        else:
            return False 


# проверяет сообщение, если есть в нем фраза "сообщение отправить" то запускает фильтр
# если все проходит, отправляет сообщение пользователю от имени бота + отправляет уведомление админу, что все прошло успешно
# на вход принимает функция собщение, объект бота (для  отправки от имени бота), ключи из словаря от фильтра - DefinitionIDUserFilter
@r.message(F.text.lower().startswith('сообщение отправить'), DefinitionIDUserFilter(admin_id_list))
async def send_message_from_user(message:Message, bot_tg:Bot, id_other:str, name:str, mes_text:str):
    await message.answer(text=f"Собщение для {name} отправлено успешно следующего содержания: {mes_text}")
    await bot_tg.send_message(chat_id=int(id_other), text=f"{mes_text}")

# проверяет сообщение, если есть в нем фраза "посмотреть анкету" то запускает фильтр
# если все проходит, отправляет админу анкету пользователя 
# на вход принимает функция собщение, ключи из словаря от фильтра - DefinitionIDUserFilter
@r.message(F.text.lower().startswith('посмотреть анкету'), DefinitionIDUserFilter(admin_id_list))
async def show_user_profile(message:Message, id_other:str):
    # Загружаем из базы данных по id все данные (возвращает список кортежей)
    user_sql = await load_user_all(id_other)    
    # Отправляем админу анкету пользователя
    await message.answer_photo(
        photo=user_sql[0][4],
        caption=f'Имя: {user_sql[0][1]}\n'
                    f'Возраст: {user_sql[0][2]}\n'
                    f'Телефон: +{user_sql[0][3]}\n'
                    f'Образование: {user_sql[0][5]}\n',
            reply_markup=menu_start()
        )
    
# проверяет сообщение, если есть в нем фраза "посмотреть записи" то запускает фильтр
# если все проходит, отправляет админу записей на консультацию / звонки
# на вход принимает функция собщение, ключи из словаря от фильтра - AppointmentsFilter
@r.message(F.text.lower().startswith('посмотреть записи'), AppointmentsFilter(admin_id_list))
async def number_search(message:Message, day:str):
    # Загружаем из базы данных по дате список запесей на консультации
    user_sql = await load_appointments(day)
    # если записей в данный день нет, то вернет пустой список и при проверки будет сообщение, что нет записей
    if not user_sql:
        await message.reply(text=f'{message.from_user.first_name} у вас нет записей в этот день')
    # Отправляем админу записи на прием из БД
    for i in user_sql:
        text_list = []
        for j in i:
            text_list.append(j)
        user = await load_user_all(text_list[0])
        await message.answer(
            text = f'Хотят на прием попасть к тебе {text_list[2]} пользователь\n'
            f'Имя: {user[0][1]}\n'
            f'Телефон: +{user[0][3]}\n'
            f'С сообщением которое оставил пользователь следующего содержания: {text_list[1]}'
            
        )



