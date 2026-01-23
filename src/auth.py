"""
Модуль авторизации на hh.ru
"""
import warnings
from typing import Protocol

from src.business_logic.auth_handler import AuthHandler
from src.config import Config
from src.pages.auth_page import AuthPage

# Предупреждение об устаревшем модуле
warnings.warn(
    "Модуль src.auth устарел. Используйте src.steps.auth_steps.AuthSteps или "
    "src.business_logic.auth_handler.AuthHandler вместо этого модуля.",
    DeprecationWarning,
    stacklevel=2
)


class PageProtocol(Protocol):
    """Протокол для страницы Playwright"""

    async def goto(self, url: str) -> None: ...
    async def fill(self, selector: str, value: str) -> None: ...
    async def click(self, selector: str) -> None: ...
    async def wait_for_selector(self, selector: str, **kwargs) -> None: ...
    async def is_visible(self, selector: str) -> bool: ...
    def locator(self, selector: str): ...


class HHAuth:
    """Класс для авторизации на hh.ru (устаревший)"""

    def __init__(self, config: Config, logger):
        """
        Инициализация класса авторизации

        :param config: Объект конфигурации
        :param logger: Объект логгера
        """
        warnings.warn(
            "HHAuth устарел. Используйте AuthHandler или AuthSteps вместо этого класса.",
            DeprecationWarning,
            stacklevel=2
        )
        self.config = config
        self.logger = logger

    async def perform_auth(self, page: PageProtocol) -> bool:
        """
        Выполнение авторизации на hh.ru

        :param page: Страница Playwright
        :return: True, если авторизация прошла успешно
        """
        warnings.warn(
            "perform_auth устарел. Используйте AuthHandler.perform_auth или AuthSteps.login_to_hh вместо этого метода.",
            DeprecationWarning,
            stacklevel=2
        )
        # Используем новый подход
        auth_handler = AuthHandler(page, self.config, self.logger)
        return await auth_handler.perform_auth()

    async def _fill_login_form(self, page: PageProtocol) -> None:
        """Заполнение формы логина (устаревший метод)"""
        warnings.warn(
            "_fill_login_form устарел.",
            DeprecationWarning,
            stacklevel=2
        )
        # Этот метод больше не используется в новой архитектуре

    async def _fill_password_form(self, page: PageProtocol) -> None:
        """Заполнение формы пароля (устаревший метод)"""
        warnings.warn(
            "_fill_password_form устарел.",
            DeprecationWarning,
            stacklevel=2
        )
        # Этот метод больше не используется в новой архитектуре

    async def _check_auth_success(self, page: PageProtocol) -> bool:
        """
        Проверка успешной авторизации (устаревший метод)

        :param page: Страница Playwright
        :return: True, если авторизация успешна
        """
        warnings.warn(
            "_check_auth_success устарел.",
            DeprecationWarning,
            stacklevel=2
        )
        # Этот метод больше не используется в новой архитектуре
        auth_page = AuthPage(page, self.config, self.logger)
        return await auth_page.is_logged_in()
