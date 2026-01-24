"""
Менеджер сессии для hh_auto_responder
"""
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from ..browser_config import get_browser_options, get_browser_context_options


class SessionManager:
    """Класс для управления сессией браузера"""
    
    def __init__(self, config, logger):
        """
        Инициализация менеджера сессии
        
        :param config: Объект конфигурации
        :param logger: Объект логгера
        """
        self.config = config
        self.logger = logger
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
    
    async def start_session(self):
        """Запуск сессии браузера"""
        if self.logger:
            self.logger.info("Запуск сессии браузера")

        self.playwright = await async_playwright().start()

        # Получение опций браузера и контекста
        browser_options = get_browser_options(self.config.HEADLESS)

        # Логгирование опций браузера
        if self.logger:
            self.logger.info(f"Опции браузера: {browser_options}")

        context_options = get_browser_context_options(
            self.config.VIEWPORT_WIDTH,
            self.config.VIEWPORT_HEIGHT,
            self.config.USER_AGENT
        )

        # Логгирование опций контекста
        if self.logger:
            self.logger.info(f"Опции контекста: {context_options}")

        # Запуск браузера
        self.browser = await self.playwright.chromium.launch(**browser_options)

        # Создание контекста браузера
        self.context = await self.browser.new_context(**context_options)

        # Создание новой страницы
        self.page = await self.context.new_page()

        if self.logger:
            self.logger.info("Сессия браузера успешно запущена")
    
    async def end_session(self):
        """Завершение сессии браузера"""
        if self.logger:
            self.logger.info("Завершение сессии браузера")
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        if self.logger:
            self.logger.info("Сессия браузера успешно завершена")
    
    def get_page(self) -> Page:
        """
        Получение текущей страницы
        
        :return: Объект страницы Playwright
        """
        return self.page
    
    def get_context(self) -> BrowserContext:
        """
        Получение текущего контекста
        
        :return: Объект контекста браузера
        """
        return self.context
    
    def get_browser(self) -> Browser:
        """
        Получение текущего браузера
        
        :return: Объект браузера
        """
        return self.browser