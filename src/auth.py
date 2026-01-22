"""
Модуль авторизации на hh.ru
"""
import asyncio
from typing import Protocol

from src.config import Config


class PageProtocol(Protocol):
    """Протокол для страницы Playwright"""
    async def goto(self, url: str) -> None: ...
    async def fill(self, selector: str, value: str) -> None: ...
    async def click(self, selector: str) -> None: ...
    async def wait_for_selector(self, selector: str, **kwargs) -> None: ...
    async def is_visible(self, selector: str) -> bool: ...
    def locator(self, selector: str): ...


class HHAuth:
    """Класс для авторизации на hh.ru"""

    def __init__(self, config: Config, logger):
        """
        Инициализация класса авторизации
        
        :param config: Объект конфигурации
        :param logger: Объект логгера
        """
        self.config = config
        self.logger = logger

    async def perform_auth(self, page: PageProtocol) -> bool:
        """
        Выполнение авторизации на hh.ru
        
        :param page: Страница Playwright
        :return: True, если авторизация прошла успешно
        """
        self.logger.info("Начало процесса авторизации")
        
        # Переход на главную страницу hh.ru
        await page.goto("https://hh.ru")
        
        # Клик по кнопке "Войти"
        await page.click("[data-qa='login']")

        # Заполнение формы логина
        await self._fill_login_form(page)

        # Заполнение формы пароля
        await self._fill_password_form(page)

        # Проверка успешной авторизации
        auth_success = await self._check_auth_success(page)
        
        if not auth_success:
            raise Exception("Authentication failed")
            
        self.logger.info("Авторизация прошла успешно")
        return True

    async def _fill_login_form(self, page: PageProtocol) -> None:
        """Заполнение формы логина (email/телефон)"""
        self.logger.debug("Заполнение формы логина")
        
        # Ожидание появления поля ввода логина
        await page.wait_for_selector("[data-qa='login-input']")
        
        # Заполнение поля логина
        await page.fill("[data-qa='login-input']", self.config.HH_LOGIN)
        
        # Нажатие кнопки "Продолжить"
        await page.click("[data-qa='login-button-next']")

    async def _fill_password_form(self, page: PageProtocol) -> None:
        """Заполнение формы пароля"""
        self.logger.debug("Заполнение формы пароля")
        
        # Ожидание появления поля ввода пароля
        await page.wait_for_selector("[data-qa='password-input']")
        
        # Заполнение поля пароля
        await page.fill("[data-qa='password-input']", self.config.HH_PASSWORD)
        
        # Нажатие кнопки "Войти"
        await page.click("[data-qa='login-button-submit']")

    async def _check_auth_success(self, page: PageProtocol) -> bool:
        """
        Проверка успешной авторизации

        :param page: Страница Playwright
        :return: True, если авторизация успешна
        """
        self.logger.debug("Проверка успешной авторизации")

        # Ожидание появления элемента, характерного для авторизованного пользователя
        # Это может быть аватарка пользователя в шапке или ссылка "Мои резюме"
        try:
            # Ждем появления элемента с аватаркой пользователя или меню профиля
            await page.wait_for_selector("[data-qa='header-menu-account']", timeout=5000)

            # Проверяем видимость элемента
            is_logged_in = await page.is_visible("[data-qa='header-menu-account']")

            return is_logged_in
        except:
            # Если элемент не найден в течение времени ожидания, значит пользователь не авторизован
            return False