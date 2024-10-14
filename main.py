""" Основной файл для запуска ТГ бота
- СОздаем логирование
- СОздаем функцию для запуска бота, в которую загружаем из файла config экзмепляр
 - регистрация роутеров + делаем через Диспетчер ссылку на экземпляр созданного бота, с целью 
 обращения к нему в других файлах 
 - запускаем базу данных SQL3
 """


import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import Config, load_config
from handlers import fsm, user_handlers, other_handlers, admin_handlers
from keyboards.main_menu import set_main_menu
from database.sqlite3 import db_start

logger = logging.getLogger(__name__)

bots = Bot

    
"""Функция запуска бота """
async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info(f'start run bot')
    
         
        
    # Загружаем конфиг в переменную config
    config: Config = load_config()
    
    # создаем экзмепляр Бота 
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher()
    dp['bot_tg'] = bot # передаем экземпляр бота, для получения его из роутеров в других модулях
    
    # Настраиваем главное меню бота
    await set_main_menu(bot)
   
    # Загружаем базу данных и запускаем ее
    await db_start()
    logger.info(f'db activet')
  
    # Регистриуем роутеры в диспетчере !!!ВАЖНО!!! как идет регистрация роутеров, так и идет обработка апдейтов т.е если есть эхо, то его в последную очередь
    dp.include_router(fsm.r)
    dp.include_router(user_handlers.r)
    dp.include_router(admin_handlers.r)
    dp.include_router(other_handlers.r)

    
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, )

    
if __name__ == "__main__":
    asyncio.run(main())
    
    