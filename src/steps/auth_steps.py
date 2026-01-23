"""
Шаги авторизации на hh.ru
"""
from ..business_logic.auth_handler import AuthHandler


class AuthSteps:
    """Класс для шагов авторизации на hh.ru"""
    
    def __init__(self, page, config, logger):
        """
        Инициализация шагов авторизации
        
        :param page: Страница Playwright
        :param config: Объект конфигурации
        :param logger: Объект логгера
        """
        self.page = page
        self.config = config
        self.logger = logger
        self.auth_handler = AuthHandler(page, config, logger)
    
    async def login_to_hh(self) -> bool:
        """
        Шаг: Авторизация на hh.ru
        
        :return: True, если авторизация прошла успешно
        """
        if self.logger:
            self.logger.info("Выполнение шага: Авторизация на hh.ru")
        
        return await self.auth_handler.perform_auth()