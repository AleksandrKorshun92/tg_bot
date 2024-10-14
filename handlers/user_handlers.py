"""Файл с основными функциями, хэндлерами
- начинается с команды старт - /start. Если пользователь зарегестрирован, то у него одно меню,
если пользователь не регестрировалс, то заполняется в БД его id и предлогается пройти регистрацию
"""

from aiogram import F, Router, Bot
from aiogram.types import FSInputFile # отвечает за загрузку файлов с директории (фото и тд)
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from lexicon.lexicon import LEXICON
from config_data.config import load_admin
from keyboards.main_menu import main_menu_no_reg, main_menu_reg
from keyboards.keybords import menu_services, menu_reviews, menu_shedule
from database.sqlite3 import load_user_all
from function.open_f import open_file_json

r = Router()

# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@r.message(CommandStart())
async def process_start_command(message: Message):
    # выгружает данные пользователя из БД по id 
    user_sql = await load_user_all(message.from_user.id)
    # Если список возвращен из БД пустой (нет пользователя в БД), просим пройти регистрацию
    if not user_sql:
        # await create_profile(message.from_user.id)
        await message.answer(text= 'Привет, ' + message.from_user.first_name +
                             LEXICON['start_no_reg'], 
                             reply_markup=main_menu_no_reg())
        
    else:
       # Если пользователь зарегестрирован, то отправляем пользователю сообщение с картинкой и с клавиатурой
        await message.answer_photo(photo=FSInputFile('photo/femida.png', filename='femida'),
                               caption=f"Привет, {message.from_user.first_name}!\n Выбирайте из меню: ",
                               reply_markup=main_menu_reg())

# Этот хэндлер будет срабатывать если, пользователь передумал проходить регистрацию
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@r.callback_query(F.data.in_(['no_reg_button', 'start_menu']))
async def start_menu(callback: CallbackQuery):
    await callback.message.delete()
     # выгружает данные пользователя из БД по id 
    user_sql = await load_user_all(callback.from_user.id)
    # Если список возвращен из БД пустой (нет пользователя в БД), просим пройти регистрацию
    if not user_sql:
        await callback.message.answer(text= 'Привет, ' + callback.from_user.first_name +
                             LEXICON['start_no_reg'], 
                             reply_markup=main_menu_no_reg())
        
    else:
        await callback.message.answer_photo(photo=FSInputFile('photo/femida.png', filename='femida'),
                               caption=f"Привет, {callback.from_user.first_name}!\n Выбирайте из меню: ",
                               reply_markup=main_menu_reg())

# Этот хэндлер будет срабатывать если, пользователь нажал команду из меню /help
@r.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON['help'])

# Этот хэндлер будет срабатывать если, пользователь нажал команду из меню /services (услуги)
@r.message(Command(commands='services'))
async def services_answer_command(message:Message):
    await message.delete()
    await message.answer(text='Услуги:', reply_markup=menu_services())

# Этот хэндлер будет срабатывать если, пользователь нажал кнопку из меню услуги
@r.callback_query(F.data.in_(['services']))
async def services_answer(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(text='Услуги:', reply_markup=menu_services())

    
# Этот хэндлер будет срабатывать если, пользователь нажал один из видов услуг
@r.callback_query(F.data.in_(["button_1",'button_2','button_3','button_4','button_5','button_6',
                              'button_7']))
async def handle_button_services(callback: CallbackQuery, bot_tg:Bot):
    # выгружаем из БД виды и стоимость услуг
    file = open_file_json("database/services.json")
    # пишет пользователю сообщение, какая выбрана услуга
    await callback.answer(text=f"{callback.from_user.username} Вы выбрали услугу {file[callback.data]}. \n"
                          f"Если вы зарегестрировались, то я Вам перезвоню, после судебного заседания", show_alert=True)
    # выгружаем id админа
    admins = load_admin() 
    # выгружаем данные пользователя, который написал сообщение о записи для отправки админу
    user_sql = await load_user_all(callback.from_user.id)
    # отправляем сообщения админу, что поступило обращение по услуги + передает данные пользователя, если он прошел регистрацию
    await bot_tg.send_message(chat_id=int(admins[0]), text=f"Сообщение от {callback.from_user.username} : {file[callback.data]}. \n\n"
                              f"Данные пользователя - имя по анкете {user_sql[0][1]}, телефон {user_sql[0][2]}")
    await bot_tg.send_message(chat_id=int(admins[1]), text=f"Сообщение от {callback.from_user.username} : {file[callback.data]}. \n\n"
                              f"Данные пользователя - имя по анкете {user_sql[0][1]}, телефон {user_sql[0][2]}")
    
    
# Этот хэндлер будет срабатывать если, пользователь нажал на кнопку, посмотреть отзывы
@r.callback_query(F.data == 'reviewsent')
async def handle_button_click(callback: CallbackQuery):
    # будет окошко, что нажали на кнопку отзывов - show_alert=True
    await callback.answer(text='вы нажали на кнопку отзывов', show_alert=True)
    # кнопка для перехода на сайт !!! тут важно посмотреть параметы, идет особенность!!!
    
    await callback.message.answer(text='Отзывы находятся на сайте яндекс. Для перехода, нажмите на кнопку',
                                  reply_markup=menu_reviews())
   

# Перехватывает кнопку расписание и выводит судей списком
@r.callback_query(F.data.in_(['shedule']))
async def shedule_judge(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(text=LEXICON['sgedule_judge'], 
                                  reply_markup=menu_shedule())

    
