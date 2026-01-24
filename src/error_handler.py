"""
Модуль обработки ошибок
"""
import asyncio
from datetime import datetime
import os
from typing import Protocol, Optional
from .telegram_notifier import TelegramNotifier


class PageProtocol(Protocol):
    """Протокол для страницы Playwright"""
    async def screenshot(self, path: str) -> None: ...


class ErrorHandler:
    """Класс для обработки ошибок"""

    def __init__(self, config, logger):
        """
        Инициализация класса обработки ошибок

        :param config: Объект конфигурации
        :param logger: Объект логгера
        """
        self.config = config
        self.logger = logger
        self.telegram_notifier = None

        # Инициализация TelegramNotifier, если токен и chat_id заданы
        if config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHAT_ID:
            self.telegram_notifier = TelegramNotifier(
                bot_token=config.TELEGRAM_BOT_TOKEN,
                chat_id=config.TELEGRAM_CHAT_ID,
                logger=logger
            )
            # Запускаем polling для получения команд от пользователя
            self.telegram_notifier.start_polling()

    def create_error_screenshot_path(self) -> str:
        """
        Создание пути для скриншота ошибки с временной меткой

        :return: Путь к файлу скриншота
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"error_screenshot_{timestamp}.png"
        return filename

    async def take_screenshot_on_error(self, page: PageProtocol, screenshot_path: str) -> None:
        """
        Создание скриншота при ошибке

        :param page: Страница Playwright
        :param screenshot_path: Путь для сохранения скриншота
        """
        self.logger.debug(f"Создание скриншота ошибки: {screenshot_path}")
        await page.screenshot(path=screenshot_path)

    async def handle_captcha_detection(self, page: PageProtocol, error_message: str) -> None:
        """
        Обработка обнаружения капчи

        :param page: Страница Playwright
        :param error_message: Сообщение об ошибке
        """
        self.logger.error(error_message)

        # Создаем скриншот
        screenshot_path = self.create_error_screenshot_path()
        await self.take_screenshot_on_error(page, screenshot_path)

        # Подготовим контекст ошибки
        context = {
            "stage": "captcha_detection",
            "url": page.url if hasattr(page, 'url') else "unknown",
            "error_type": "captcha_detected"
        }

        # Отправляем отчет в Telegram, если настроено
        if self.telegram_notifier:
            self.telegram_notifier.send_error_report(
                error=Exception(error_message),
                context=context,
                screenshot_path=screenshot_path
            )

        # Вызываем исключение для остановки выполнения
        raise Exception(error_message)

    async def handle_unexpected_modal_window(self, page: PageProtocol, error_message: str) -> None:
        """
        Обработка неожиданного модального окна

        :param page: Страница Playwright
        :param error_message: Сообщение об ошибке
        """
        self.logger.error(error_message)

        # Создаем скриншот
        screenshot_path = self.create_error_screenshot_path()
        await self.take_screenshot_on_error(page, screenshot_path)

        # Подготовим контекст ошибки
        context = {
            "stage": "unexpected_modal",
            "url": page.url if hasattr(page, 'url') else "unknown",
            "error_type": "modal_window"
        }

        # Отправляем отчет в Telegram, если настроено
        if self.telegram_notifier:
            self.telegram_notifier.send_error_report(
                error=Exception(error_message),
                context=context,
                screenshot_path=screenshot_path
            )

        # Вызываем исключение для остановки выполнения
        raise Exception(error_message)

    async def handle_general_error(self, page: PageProtocol, error: Exception) -> None:
        """
        Обработка общей ошибки

        :param page: Страница Playwright
        :param error: Объект ошибки
        """
        error_message = f"Произошла непредвиденная ошибка: {error}"
        self.logger.error(error_message)

        # Создаем скриншот
        screenshot_path = self.create_error_screenshot_path()
        await self.take_screenshot_on_error(page, screenshot_path)

        # Подготовим контекст ошибки
        context = {
            "stage": "general_error",
            "url": page.url if hasattr(page, 'url') else "unknown",
            "error_type": "general_exception",
            "exception_class": type(error).__name__
        }

        # Отправляем отчет в Telegram, если настроено
        if self.telegram_notifier:
            self.telegram_notifier.send_error_report(
                error=error,
                context=context,
                screenshot_path=screenshot_path
            )

        # Вызываем исключение для остановки выполнения
        raise error

    async def send_startup_notification(self) -> None:
        """
        Отправка уведомления о запуске скрипта в Telegram
        """
        if self.telegram_notifier:
            self.telegram_notifier.send_startup_notification()

    async def send_shutdown_notification(self, success_count: int = 0, error_count: int = 0) -> None:
        """
        Отправка уведомления о завершении работы скрипта в Telegram

        :param success_count: Количество успешных откликов
        :param error_count: Количество ошибок
        """
        if self.telegram_notifier:
            self.telegram_notifier.send_shutdown_notification(success_count, error_count)

    def cleanup(self):
        """
        Очистка ресурсов при завершении работы
        """
        if self.telegram_notifier:
            self.telegram_notifier.stop_polling()