"""
Шаги отправки откликов на hh.ru
"""
from ..business_logic.application_handler import ApplicationHandler


class ApplicationSteps:
    """Класс для шагов отправки откликов на hh.ru"""
    
    def __init__(self, page, config, logger):
        """
        Инициализация шагов отправки откликов
        
        :param page: Страница Playwright
        :param config: Объект конфигурации
        :param logger: Объект логгера
        """
        self.page = page
        self.config = config
        self.logger = logger
        self.application_handler = ApplicationHandler(page, config, logger)
    
    async def apply_to_vacancy(self, vacancy_locator, cover_letter: str = "") -> str:
        """
        Шаг: Отправка отклика на вакансию
        
        :param vacancy_locator: Локатор вакансии
        :param cover_letter: Текст сопроводительного письма (опционально)
        :return: Результат отклика
        """
        if self.logger:
            self.logger.info("Выполнение шага: Отправка отклика на вакансию")
        
        return await self.application_handler.apply_to_vacancy(vacancy_locator, cover_letter)