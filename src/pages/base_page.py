"""
Базовый класс для Page Objects
"""
from typing import Protocol, Union, Dict, Any
from playwright.async_api import Page, Locator


class PageProtocol(Protocol):
    """Протокол для страницы Playwright"""
    async def goto(self, url: str) -> None: ...
    async def fill(self, selector: str, value: str) -> None: ...
    async def click(self, selector: str) -> None: ...
    async def wait_for_selector(self, selector: str, **kwargs) -> None: ...
    async def wait_for_url(self, url: str, **kwargs) -> None: ...
    async def is_visible(self, selector: str) -> bool: ...
    def locator(self, selector: str) -> Locator: ...
    async def press(self, selector: str, key: str) -> None: ...
    async def screenshot(self, **kwargs) -> bytes: ...


class BasePage:
    """Базовый класс для всех Page Objects"""
    
    def __init__(self, page: PageProtocol, config=None, logger=None):
        """
        Инициализация базовой страницы
        
        :param page: Страница Playwright
        :param config: Объект конфигурации
        :param logger: Объект логгера
        """
        self.page = page
        self.config = config
        self.logger = logger
    
    async def wait_for_element(self, selector: str, timeout: int = 30000) -> bool:
        """
        Ожидание появления элемента
        
        :param selector: Селектор элемента
        :param timeout: Таймаут ожидания в миллисекундах
        :return: True, если элемент появился
        """
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            return True
        except Exception:
            return False
    
    async def is_element_visible(self, selector: str) -> bool:
        """
        Проверка видимости элемента
        
        :param selector: Селектор элемента
        :return: True, если элемент видим
        """
        try:
            return await self.page.is_visible(selector)
        except Exception:
            return False
    
    async def safe_click(self, selector: str, timeout: int = 30000) -> bool:
        """
        Безопасный клик по элементу
        
        :param selector: Селектор элемента
        :param timeout: Таймаут ожидания в миллисекундах
        :return: True, если клик выполнен успешно
        """
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            await self.page.click(selector)
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Ошибка при клике на элемент {selector}: {e}")
            return False
    
    async def safe_fill(self, selector: str, value: str, timeout: int = 30000) -> bool:
        """
        Безопасное заполнение поля
        
        :param selector: Селектор поля
        :param value: Значение для заполнения
        :param timeout: Таймаут ожидания в миллисекундах
        :return: True, если поле заполнено успешно
        """
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            await self.page.fill(selector, value)
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Ошибка при заполнении поля {selector}: {e}")
            return False