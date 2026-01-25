from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from typing import Optional, AsyncGenerator
from contextlib import asynccontextmanager
from src.logger import logger


class HHSession:
    """
    Класс для управления сессией браузера и контекста для работы с hh.ru
    """

    def __init__(self):
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        logger.debug("HHSession инициализирован")

    @asynccontextmanager
    async def create_session(self, headless: bool = False) -> AsyncGenerator['HHSession', None]:
        """Создание сессии как асинхронного контекстного менеджера"""
        logger.info("Создание сессии браузера")
        try:
            self.playwright = await async_playwright().start()
            logger.debug("Playwright запущен")

            self.browser = await self.playwright.chromium.launch(headless=headless)
            logger.debug("Браузер запущен")

            self.context = await self.browser.new_context()
            logger.debug("Контекст создан")

            self.page = await self.context.new_page()
            logger.debug("Страница создана")

            logger.success("Сессия браузера успешно создана")
            yield self
        except Exception as e:
            logger.error(f"Ошибка при создании сессии: {e}")
            raise
        finally:
            await self.close()

    async def close(self):
        """Закрытие сессии"""
        logger.info("Закрытие сессии браузера")
        try:
            if self.browser:
                await self.browser.close()
                logger.debug("Браузер закрыт")
            if self.playwright:
                await self.playwright.stop()
                logger.debug("Playwright остановлен")
            logger.success("Сессия браузера успешно закрыта")
        except Exception as e:
            logger.error(f"Ошибка при закрытии сессии: {e}")
            raise

    def get_page(self) -> Optional[Page]:
        """Получение текущей страницы"""
        if self.page:
            logger.debug("Получена страница из сессии")
        else:
            logger.warning("Попытка получить страницу, но она не инициализирована")
        return self.page