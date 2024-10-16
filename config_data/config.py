""" Файл открывает файл с форматом env для загрузки Токен бота, списка админов"""
from os import getenv
from dataclasses import dataclass
from environs import Env  # установка - pip install environs

BOT_TOKEN = ("BOT_TOKEN")     # необходимо указать в переменных окружения
ADMIN_IDS = (1015119851, 1678398042)

@dataclass
class TgBot():
    token: str # токен для доступа к боту


@dataclass
class Config:
    tg_bot: TgBot # создаем класс бота


# создания экземпляра телеграмм бота с загрузкой токена, списка админов
def load_config() -> Config:
    return Config(
        tg_bot=TgBot(
            token=BOT_TOKEN)
    )

# Загрузка списка админов
def load_admin():
    ADMINS = list(ADMIN_IDS)
    return ADMINS