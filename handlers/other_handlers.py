"""Хочу добавить чатGPT4 при общение с ботом 
Для этого надо разобраться и установить бесплатное API компаний, которые купили чат
репозиторий - https://github.com/xtekky/gpt4free?tab=readme-ov-file#text-generation
"""


from aiogram import Router
from aiogram.types import Message
from database.sqlite3 import update_message

r = Router()


# Этот хэндлер будет реагировать на любые сообщения пользователя, которые не были обработаны ранее
@r.message()
async def send_echo(message: Message):
    # тут происходит запись (обновление) в БД messange - записывается id пользователя и сообщение
    await update_message(message.text, message.from_user.id)
       
    await message.answer(f'Это эхо ... Я не придумал фразы, на которые можно настроить бота. Если есть предложения, просьба пишите))) ! {message.text}')