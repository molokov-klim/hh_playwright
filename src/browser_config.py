"""
Модуль настройки браузера
"""
from typing import Dict, Any
from src.config import Config


def get_browser_options(config: Config) -> Dict[str, Any]:
    """
    Получение опций браузера на основе конфигурации
    
    :param config: Объект конфигурации
    :return: Словарь с опциями браузера
    """
    options = {
        "headless": config.HEADLESS,
        "args": [
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage",
            "--no-sandbox",
            "--disable-setuid-sandbox"
        ]
    }
    
    return options


def get_browser_context_options(config: Config) -> Dict[str, Any]:
    """
    Получение опций контекста браузера на основе конфигурации
    
    :param config: Объект конфигурации
    :return: Словарь с опциями контекста браузера
    """
    context_options = {
        "viewport": {
            "width": config.VIEWPORT_WIDTH,
            "height": config.VIEWPORT_HEIGHT
        },
        "user_agent": config.USER_AGENT,
        "timeout": config.TIMEOUT,
        "java_script_enabled": True,
        "ignore_https_errors": True,
        "extra_http_headers": {
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
        }
    }
    
    return context_options