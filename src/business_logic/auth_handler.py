"""
Обработчик авторизации на hh.ru
"""
from ..pages.auth_page import AuthPage
from ..decorators import async_log_info


class AuthHandler:
    """Класс для обработки авторизации на hh.ru"""

    def __init__(self, page, config, logger):
        """
        Инициализация обработчика авторизации

        :param page: Страница Playwright
        :param config: Объект конфигурации
        :param logger: Объект логгера
        """
        self.page = page
        self.config = config
        self.logger = logger
        self.auth_page = AuthPage(page, config, logger)

    @async_log_info()
    async def perform_auth(self) -> bool:
        """
        Выполнение авторизации на hh.ru

        :return: True, если авторизация прошла успешно
        """
        if self.logger:
            self.logger.info("Начало процесса авторизации")

        # Переход на страницу авторизации
        if not await self.auth_page.navigate_to_login_page():
            if self.logger:
                self.logger.error("Не удалось перейти на страницу авторизации")
            return False

        # Заполнение логина
        if not await self.auth_page.fill_login(self.config.HH_LOGIN):
            if self.logger:
                self.logger.error("Не удалось заполнить поле логина")
            return False

        # Заполнение пароля
        if not await self.auth_page.fill_password(self.config.HH_PASSWORD):
            if self.logger:
                self.logger.error("Не удалось заполнить поле пароля")
            return False

        # Проверка успешной авторизации
        if not await self.auth_page.is_logged_in():
            if self.logger:
                self.logger.error("Авторизация не удалась")
            return False

        if self.logger:
            self.logger.info("Авторизация прошла успешно")

        return True