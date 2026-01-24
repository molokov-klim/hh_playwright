"""
Модуль настройки браузера
"""
from typing import Dict, Any


def get_browser_options(headless: bool) -> Dict[str, Any]:
    """
    Получение опций браузера на основе конфигурации

    :param headless: Режим без GUI
    :return: Словарь с опциями браузера
    """
    options = {
        "headless": headless,
        "args": [
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage",
            "--no-sandbox",
            "--disable-setuid-sandbox"
        ]
    }

    # В headed режиме добавляем дополнительные аргументы для корректного отображения
    if not headless:
        options["args"].extend([
            "--start-maximized",
            "--disable-extensions",
            "--disable-plugins",
            "--disable-images",  # Ускоряет загрузку страниц
        ])

    return options


def get_browser_context_options(viewport_width: int, viewport_height: int, user_agent: str) -> Dict[str, Any]:
    """
    Получение опций контекста браузера на основе конфигурации

    :param viewport_width: Ширина окна браузера
    :param viewport_height: Высота окна браузера
    :param user_agent: User agent строка
    :return: Словарь с опциями контекста браузера
    """
    context_options = {
        "viewport": {
            "width": viewport_width,
            "height": viewport_height
        },
        "user_agent": user_agent,
        "java_script_enabled": True,
        "ignore_https_errors": True,
        "extra_http_headers": {
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
        }
    }

    return context_options