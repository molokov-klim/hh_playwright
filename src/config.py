"""
Модуль конфигурации приложения
"""
import os
from typing import NamedTuple


class Config(NamedTuple):
    """Класс для хранения конфигурации приложения"""
    HH_LOGIN: str
    HH_PASSWORD: str
    HEADLESS: bool = True
    VIEWPORT_WIDTH: int = 1920
    VIEWPORT_HEIGHT: int = 1080
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    TIMEOUT: int = 30000
    RESUME_ID: str = ""  # Может быть пустым, будет определен автоматически


def get_config_from_env() -> Config:
    """
    Получение конфигурации из переменных окружения
    
    :return: Объект Config с настройками
    :raises ValueError: Если обязательные переменные окружения отсутствуют
    """
    login = os.getenv('HH_LOGIN')
    password = os.getenv('HH_PASSWORD')
    
    if not login:
        raise ValueError("HH_LOGIN environment variable is required")
    
    if not password:
        raise ValueError("HH_PASSWORD environment variable is required")
    
    # Преобразование строки в булево значение для HEADLESS
    headless_str = os.getenv('HEADLESS', 'true').lower()
    headless = headless_str not in ('false', '0', 'no', 'off')
    
    viewport_width = int(os.getenv('VIEWPORT_WIDTH', '1920'))
    viewport_height = int(os.getenv('VIEWPORT_HEIGHT', '1080'))
    user_agent = os.getenv('USER_AGENT', Config.USER_AGENT)
    timeout = int(os.getenv('TIMEOUT', '30000'))
    resume_id = os.getenv('RESUME_ID', '')
    
    return Config(
        HH_LOGIN=login,
        HH_PASSWORD=password,
        HEADLESS=headless,
        VIEWPORT_WIDTH=viewport_width,
        VIEWPORT_HEIGHT=viewport_height,
        USER_AGENT=user_agent,
        TIMEOUT=timeout,
        RESUME_ID=resume_id
    )