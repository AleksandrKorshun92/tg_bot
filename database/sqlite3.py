""" 
Инициализируем базу данных (если файл есть с таким именем, то продолжаем, если нет - создаем новый)
Обновляем данные 
Выгружаем данные при необходимости

При вызове данных функций в других модулях надо всегда начинать c await
"""

import sqlite3 as sq
from datetime import date

# Запуск базы данных - данную функцию запускаем в файле main
async def db_start():
    
    global db, cur
    
    # создем экземпляр базы даных с названием файла, где она будет храниться
    db = sq.connect('db_bota.db')
    cur = db.cursor()
    
    # СОздаем базу данных пользователей, которые запустили бота + прошли регистрацию. 
    cur.execute('CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, fill_name TEXT, fill_age TEXT,'
               'fill_number TEXT, upload_photo TEXT, fill_education TEXT)')
    
    # Создаем базу данных по написанным боту сообщениям. 
    cur.execute('CREATE TABLE IF NOT EXISTS message_from_users(user_id TEXT, message TEXT)')
    
    # Создаем базу данных по записям на прием. 
    cur.execute('CREATE TABLE IF NOT EXISTS appointments(user_id TEXT, message TEXT, day TEXT)')
    
    # Создаем базу данных по произведенным оплатам. 
    cur.execute('CREATE TABLE IF NOT EXISTS pay(user_id TEXT, upload_photo TEXT, day TEXT)')
    
    print('GO')
    db.commit()


# Заполнение таблицы profile данными по id   
async def create_profile(user_id):
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id,)).fetchone()
    
    if not user:
        cur.execute("INSERT INTO profile VALUES(?, ?, ?, ?, ?, ?)",(user_id,'','','','',''))
        db.commit()

       
# Заполнение таблицы profile после регистрации пользвателя с сохранением его данных
async def edit_profile(state, user_id):
    cur.execute("UPDATE profile SET fill_name = '{}', fill_age = '{}', fill_number = '{}',"
                    "upload_photo = '{}', fill_education = '{}'"
                    "WHERE user_id == '{}' ".format(state['name'],state['age'],state['number'],state['photo_id'],state['education'], user_id))
    db.commit()

# Выгрузка данных пользователя
async def load_user_all(user_id):
    # выгружаем все данные пользователя по полученному id
    load_user_bd = cur.execute("SELECT * FROM profile WHERE user_id == '{}' ".format(user_id)).fetchall()
    
    # сохраняем все в список, после возвращем его 
    loads = []
    for i in load_user_bd:
        loads.append(i)
    db.commit()
    return loads
    
# Выгрузка id пользователя по его имени    
async def load_id_from_name(name):
    # выгрузка id по имени
    load_bd = cur.execute("SELECT user_id FROM profile WHERE fill_name == '{}' ".format(name)).fetchall()
    res = load_bd
    db.commit()
    
    # возвращает id пользователя
    return res[0][0]


# Заполнение таблицы message_from_users после отправки боту сообщения
async def update_message(message, user_id):
    cur.execute("INSERT INTO message_from_users VALUES('{}', '{}')".format(user_id, message))
    db.commit()


# Заполнение таблицы appointments после отправки боту сообщения для записи на прием
async def update_appointments(message, user_id):
    # создаем переменню и записываем дату записи
    today = date.today().strftime("%d.%m.%Y")
    cur.execute("INSERT INTO appointments VALUES('{}', '{}', '{}')".format(user_id, message, today))
    db.commit()


# Выгрузка данных по записям по дате
async def load_appointments(day):
    # выгружаем все данные по определенной дате
    load_appointments_bd = cur.execute("SELECT * FROM appointments WHERE day == '{}' ".format(day)).fetchall()
    
    # сохраняем все в список, после возвращем его 
    loads = []
    for i in load_appointments_bd:
        loads.append(i)
    db.commit()
    return loads


# Заполнение таблицы pay после отправки боту фото оплаты
async def update_pay(pay_photo, user_id):
    # создаем переменню и записываем дату записи
    today = date.today().strftime("%d.%m.%Y")
    cur.execute("INSERT INTO pay VALUES('{}', '{}', '{}')".format(user_id, pay_photo, today))
    db.commit()
    

# Выгрузка данных по оплатам по id
async def load_pay(user_id):
    # выгружаем все данные по определенной id
    load_appointments_bd = cur.execute("SELECT * FROM pay WHERE user_id == '{}' ".format(user_id)).fetchall()
    
    # сохраняем все в список, после возвращем его 
    loads = []
    for i in load_appointments_bd:
        loads.append(i)
    db.commit()
    return loads
