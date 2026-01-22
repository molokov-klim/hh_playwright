"""
Модуль обработки ошибок
"""
import asyncio
from datetime import datetime
import os
from typing import Protocol


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
        
        # Вызываем исключение для остановки выполнения
        raise error