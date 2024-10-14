"""Файл с машинным состоянием FSM, которые принимает некоторые хэндлеры (заполнение профиля, оплата)
"""

from aiogram import Bot, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, Message, PhotoSize)
from lexicon.lexicon import LEXICON
from keyboards.keybords import menu_reg, menu_back, menu_start, menu_reg_start, menu_education, menu_edit_profile
from config_data.config import load_admin
from database.sqlite3 import create_profile, edit_profile, load_user_all, update_appointments, update_pay
import json

# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage = MemoryStorage()

# Создаем объекты роутера
r = Router()

# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    fill_name = State()        # Состояние ожидания ввода имени
    fill_age = State()         # Состояние ожидания ввода возраста
    fill_number = State()      # Состояние ожидания ввода телефона
    upload_photo = State()     # Состояние ожидания загрузки фото
    fill_education = State()   # Состояние ожидания выбора образования
    pay_photo = State()        # Состояние ожидания загрузки фото оплаты
    make_appointment = State() # Состояние ожидания данных для записи на прием (звонка)


# Этот хэндлер будет срабатывать на команду /registracio вне состояний и предлагать перейти к заполнению анкеты
@r.callback_query(F.data.in_(['registracio']), StateFilter(default_state))
async def process_start_registracio(callback: CallbackQuery):
    # удаляем предыдущие сообщения
    await callback.message.delete()

    # Отправляем пользователю сообщение с клавиатурой
    await callback.message.answer(
        text=LEXICON['questionnaire'],
        reply_markup=menu_reg_start()
    )
        

# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@r.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text=LEXICON['cancel']
    )


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@r.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text=LEXICON['cancel']
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на кнопку начать регистрацию
# и переводить бота в состояние ожидания ввода имени пользователя
@r.callback_query(F.data.in_(['start_reg', ]), StateFilter(default_state))
async def process_fillform_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        text=LEXICON['input_name']
    )   
    # после ввода имени переходит FSN стостояние в заполнение имени, для проверки корректности ввода
    await state.set_state(FSMFillForm.fill_name)


# Этот хэндлер будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода возраста
@r.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(name=message.text)
    await message.answer(text=LEXICON['input_age'])
    
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.fill_age)


# Этот хэндлер будет срабатывать, если во время ввода имени
# будет введено что-то некорректное
@r.message(StateFilter(FSMFillForm.fill_name))
async def warning_not_name(message: Message):
    await message.answer(
        text= LEXICON['error_name']
    )


# Этот хэндлер будет срабатывать, если введен корректный возраст
# и переводить в состояние набора номера телефона (проверяет, чтобы возвратст был не менее 4 и не более 120 цифр)
@r.message(StateFilter(FSMFillForm.fill_age),
            lambda x: x.text.isdigit() and 4 <= int(x.text) <= 120)
async def process_age_sent(message: Message, state: FSMContext):
    # Cохраняем возраст в хранилище по ключу "age"
    await state.update_data(age=message.text)
   
    await message.answer(text=LEXICON['input_number_phone'])
   
    # Устанавливаем состояние ожидания набора номера телефона
    await state.set_state(FSMFillForm.fill_number)


# Этот хэндлер будет срабатывать, если во время ввода возраста
# будет введено что-то некорректное
@r.message(StateFilter(FSMFillForm.fill_age))
async def warning_not_age(message: Message):
    await message.answer(
        text=LEXICON['error_age']
    )


# Этот хэндлер будет срабатывать после корректного ввода номера телефона
# переводить в состояние отправки фото (проверяет, что телефон начинается с 7)
@r.message(StateFilter(FSMFillForm.fill_number),
                   F.text.isdigit() and F.text.startswith('7'))
async def process_number(message:Message, state: FSMContext):
    # Cохраняем номер телефона в хранилище по ключу "number"
    await state.update_data(number=message.text)
    await message.delete()
    await message.answer(
        text=LEXICON['input_photo_user']
    )
    # Устанавливаем состояние ожидания загрузки фото
    await state.set_state(FSMFillForm.upload_photo)


# Этот хэндлер будет срабатывать, если во время набора номера телефона будет
# будет введено/отправлено что-то некорректное
@r.message(StateFilter(FSMFillForm.fill_number))
async def warning_not_gender(message: Message):
    await message.answer(
        text=LEXICON['error_number']
    )

# Этот хэндлер будет срабатывать, если отправлено фото
# и переводить в состояние выбора образования
@r.message(StateFilter(FSMFillForm.upload_photo),
            F.photo[-1].as_('largest_photo'))
async def process_photo_sent(message: Message,
                             state: FSMContext,
                             largest_photo: PhotoSize):
    # Cохраняем данные фото (file_unique_id и file_id) в хранилище
    # по ключам "photo_unique_id" и "photo_id"
    await state.update_data(
        photo_unique_id=largest_photo.file_unique_id,
        photo_id=largest_photo.file_id
    )
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(
        text=LEXICON['input_edication'],
        reply_markup=menu_education()
    )
    # Устанавливаем состояние ожидания выбора образования
    await state.set_state(FSMFillForm.fill_education)


# Этот хэндлер будет срабатывать, если во время отправки фото
# будет введено/отправлено что-то некорректное
@r.message(StateFilter(FSMFillForm.upload_photo))
async def warning_not_photo(message: Message):
    await message.answer(
        text=LEXICON['error_photo']
    )

# Этот хэндлер будет срабатывать, если выбрано образование, записывать в БД и прекращать FSM
@r.callback_query(StateFilter(FSMFillForm.fill_education),
                   F.data.in_(['Среднее', 'Высшее', 'Нету образование']))
async def process_education_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем данные об образовании по ключу "education"
    await state.update_data(education=callback.data)
    # в БД создается запись с id пользователя
    await create_profile(callback.from_user.id)
    """!!! ТУТ БАЗА ДАННЫХ ЮЗЕРА """ 
    # user_dict[callback.from_user.id] = await state.get_data()
    # users_db[callback.from_user.id] = callback.from_user.first_name
   
    """!!! Идет сохранение даннанкеты пользователя в базу данных""" 
    await edit_profile(await state.get_data(), user_id= callback.from_user.id)
        
    # Завершаем машину состояний FSM
    await state.clear()
    # Отправляем в чат сообщение о выходе из машины состояний
    await callback.message.edit_text(
        text=LEXICON['cancel_input_profile']
    )
  
    await callback.message.answer(
        text='Можете посмотреть свои данные: ',
        reply_markup=menu_reg()
    )
        
 

# Этот хэндлер будет срабатывать, если во время выбора образования
# будет введено/отправлено что-то некорректное
@r.message(StateFilter(FSMFillForm.fill_education))
async def warning_not_education(message: Message):
    await message.answer(
        text=LEXICON['error_education']
    )

      
# Этот хэндлер будет срабатывать на нажатие кнопки - showdata
# и отправлять в чат данные анкеты, либо сообщение об отсутствии данных
@r.callback_query(F.data.in_(['showdata']), StateFilter(default_state))
async def process_showdata_command(callback: CallbackQuery):
    await callback.message.delete()
    
    # выгружаю БД в переменную 
    user_sql = await load_user_all(callback.from_user.id)
    # Отправляем пользователю анкету, если она есть в БД
    if callback.from_user.id == int(user_sql[0][0]):
        await callback.message.answer_photo(
            photo=user_sql[0][4],
            caption=f'Имя: {user_sql[0][1]}\n'
                    f'Возраст: {user_sql[0][2]}\n'
                    f'Телефон: +{user_sql[0][3]}\n'
                    f'Образование: {user_sql[0][5]}\n',
            reply_markup=menu_back()
        )
 
    else:
        # Если анкеты пользователя в базе нет - предлагаем заполнить
        await callback.message.answer(
            text='Вы еще не заполняли анкету!'
        )


# Переход для изменения профиля (анкеты)
@r.callback_query(F.data=='edit_profile')
async def edit_profiless(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        text=LEXICON['edit_profile'], reply_markup=menu_edit_profile()
    )


#Будет переведен в состояние ожидание ввода фото оплаты, пока нет фото не выйдет из FSM
@r.callback_query(F.data.in_(['pay','/pay']), StateFilter(default_state))
async def process_pay(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer(text='Вы нажали на кнопку оплатить', show_alert=True)
    await callback.message.answer(
        text=LEXICON['pay_user'], reply_markup=menu_start()
    )
    # Устанавливаем состояние ожидания фото от пользователя
    await state.set_state(FSMFillForm.pay_photo)

#Отправляет сообщение администратору, что произведена оплата (загружет экзмепляр бота через роутер - диспетчер)
@r.message(StateFilter(FSMFillForm.pay_photo), F.photo[-1].as_('largest_photo'))
async def confirmation_pay(message:Message, bot_tg:Bot, state: FSMContext, largest_photo: PhotoSize):
    # Отвечаем пользователю, что получили фото оплаты. 
    await message.answer(
        text="Получил фото оплаты, спасибо "+message.from_user.first_name +'!', reply_markup=menu_start()
    )
    # сохраняем фото в FSM
    await state.update_data(
        photo_unique_id=largest_photo.file_unique_id,
        photo_id=largest_photo.file_id
    )
    # загружает фото оплаты в БД pay
    await update_pay(largest_photo.file_id, message.from_user.id)

    """ !!!! ТУТ сделать, чтобы сообщения отправлялись Жени!! """
    admins = load_admin()
    await bot_tg.send_photo(chat_id=int(admins[0]), photo=largest_photo.file_id, 
                            caption= f"Сообщение от {message.from_user.username}. Он произвел оплату \n"
                              f"фото чека оплаты")
    await bot_tg.send_photo(chat_id=int(admins[1]), photo=largest_photo.file_id, 
                            caption= f"Сообщение от {message.from_user.username}. Он произвел оплату \n"
                              f"фото чека оплаты")
    # Завершаем машину состояний FSM
    await state.clear()


# Этот хэндлер будет срабатывать, если во время отправки фото
# будет введено/отправлено что-то некорректное
@r.message(StateFilter(FSMFillForm.pay_photo))
async def warning_not_photo_pay(message: Message):
    await message.answer(
        text=LEXICON['error_photo_pay']
    )

#Будет переведен в состояние ожидание ввода данных для записи на прием
@r.callback_query(F.data.in_(['make_appointment']), StateFilter(default_state))
async def make_appointment(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text=LEXICON['make_appointment'])
    # Устанавливаем состояние ожидания написания текста записи на прием / консультацию
    await state.set_state(FSMFillForm.make_appointment)


# Отправляет сообщение администратору, что произведена запись на прием /консультацию
@r.message(StateFilter(FSMFillForm.make_appointment))
async def process_make_appointment(message:Message, bot_tg:Bot, state: FSMContext):
    await message.answer(
        text="Получил данные, спасибо "+message.from_user.first_name +'!', reply_markup=menu_start()
    )
    # загружает сообщение от пользователя по записи на прием в БД
    await update_appointments(message.text, message.from_user.id)
    
    # выгружаем id админа
    admins = load_admin()
    # выгружаем данные пользователя, который написал сообщение о записи для отправки админу
    user_sql = await load_user_all(message.from_user.id)
    await bot_tg.send_message(chat_id=int(admins[0]), text=f"Сообщение от {message.from_user.username} : {message.text}. \n\n "
                              f"Данные пользователя - имя по анкете {user_sql[0][1]}, телефон {user_sql[0][3]}")
    await bot_tg.send_message(chat_id=int(admins[1]), text=f"Сообщение от {message.from_user.username} : {message.text}. \n\n "
                              f"Данные пользователя - имя по анкете {user_sql[0][1]}, телефон {user_sql[0][3]}")
     # Завершаем машину состояний FSM
    await state.clear()
