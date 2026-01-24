"""
Модуль конфигурации приложения
"""
import os
from dataclasses import dataclass


@dataclass
class Config:
    """Класс для хранения конфигурации приложения"""
    HH_LOGIN: str
    HH_PASSWORD: str
    HEADLESS: bool = True
    VIEWPORT_WIDTH: int = 1920
    VIEWPORT_HEIGHT: int = 1080
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    TIMEOUT: int = 30000
    RESUME_ID: str = ""  # Может быть пустым, будет определен автоматически
    FAKE: bool = True  # Если True, реальные отклики не отправляются
    TELEGRAM_BOT_TOKEN: str = ""  # Токен для Telegram бота
    TELEGRAM_CHAT_ID: str = ""  # ID чата для отправки отчетов


def load_dotenv_if_exists():
    """
    Загружает переменные из .env файла, если он существует
    """
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')

    if os.path.exists(dotenv_path):
        try:
            with open(dotenv_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()

                        # Удаляем кавычки из значения, если они есть
                        if (value.startswith('"') and value.endswith('"')) or \
                           (value.startswith("'") and value.endswith("'")):
                            value = value[1:-1]

                        if key not in os.environ:  # Не перезаписываем существующие переменные
                            os.environ[key] = value
        except Exception as e:
            print(f"Ошибка при загрузке .env файла: {e}")


def get_config_from_env() -> Config:
    """
    Получение конфигурации из переменных окружения

    :return: Объект Config с настройками
    :raises ValueError: Если обязательные переменные окружения отсутствуют
    """
    # Загружаем .env файл, если он существует
    load_dotenv_if_exists()

    login = os.getenv('HH_LOGIN')
    password = os.getenv('HH_PASSWORD')

    if not login:
        raise ValueError("HH_LOGIN environment variable is required")

    if not password:
        raise ValueError("HH_PASSWORD environment variable is required")

    # Преобразование строки в булево значение для HEADLESS
    headless_str = os.getenv('HEADLESS', 'true').lower()
    headless = headless_str not in ('false', '0', 'no', 'off')

    # Преобразование строки в булево значение для FAKE
    fake_str = os.getenv('FAKE', 'false').lower()
    fake = fake_str in ('true', '1', 'yes', 'on')

    viewport_width = int(os.getenv('VIEWPORT_WIDTH', '1920'))
    viewport_height = int(os.getenv('VIEWPORT_HEIGHT', '1080'))
    user_agent = os.getenv('USER_AGENT', "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    timeout = int(os.getenv('TIMEOUT', '30000'))
    resume_id = os.getenv('RESUME_ID', '')
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID', '')

    return Config(
        HH_LOGIN=login,
        HH_PASSWORD=password,
        HEADLESS=headless,
        VIEWPORT_WIDTH=viewport_width,
        VIEWPORT_HEIGHT=viewport_height,
        USER_AGENT=user_agent,
        TIMEOUT=timeout,
        RESUME_ID=resume_id,
        FAKE=fake,
        TELEGRAM_BOT_TOKEN=telegram_bot_token,
        TELEGRAM_CHAT_ID=telegram_chat_id
    )