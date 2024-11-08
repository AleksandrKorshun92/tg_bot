""" Файл открывает файл с форматом env для загрузки Токен бота, списка админов"""
from os import getenv
from dataclasses import dataclass
from environs import Env  # установка - pip install environs

@dataclass
class TgBot():
    token: str # токен для доступа к боту
    admin_ids: list[int]


@dataclass
class Config:
    tg_bot: TgBot # создаем класс бота


# создания экземпляра телеграмм бота с загрузкой токена, списка админов
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path) # путь для файла env где хранится токен
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS'))) # возващае экземпляр класса конфиг - бота с токеном
        )
    )

# Загрузка списка админов
def load_admin(path: str | None = None):
    env = Env()
    env.read_env(path) # путь для файла env где хранится токен
    ADMINS = env.list('ADMIN_IDS')
    return ADMINS