from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from typing import Optional, AsyncGenerator
from contextlib import asynccontextmanager


class HHSession:
    """
    Класс для управления сессией браузера и контекста для работы с hh.ru
    """

    def __init__(self):
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    @asynccontextmanager
    async def create_session(self, headless: bool = False) -> AsyncGenerator['HHSession', None]:
        """Создание сессии как асинхронного контекстного менеджера"""
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=headless)
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()
            yield self
        finally:
            await self.close()

    async def close(self):
        """Закрытие сессии"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    def get_page(self) -> Optional[Page]:
        """Получение текущей страницы"""
        return self.page