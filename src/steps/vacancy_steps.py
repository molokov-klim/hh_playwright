"""
Шаги работы с вакансиями на hh.ru
"""
from ..business_logic.vacancy_handler import VacancyHandler


class VacancySteps:
    """Класс для шагов работы с вакансиями на hh.ru"""
    
    def __init__(self, page, config, logger):
        """
        Инициализация шагов работы с вакансиями
        
        :param page: Страница Playwright
        :param config: Объект конфигурации
        :param logger: Объект логгера
        """
        self.page = page
        self.config = config
        self.logger = logger
        self.vacancy_handler = VacancyHandler(page, config, logger)
    
    async def get_vacancy_locators(self) -> list:
        """
        Шаг: Получение локаторов вакансий
        
        :return: Список локаторов вакансий
        """
        if self.logger:
            self.logger.info("Выполнение шага: Получение локаторов вакансий")
        
        return await self.vacancy_handler.get_vacancy_locators()
    
    async def get_applicable_vacancies(self) -> list:
        """
        Шаг: Получение вакансий, на которые можно откликнуться
        
        :return: Список локаторов вакансий, на которые можно откликнуться
        """
        if self.logger:
            self.logger.info("Выполнение шага: Получение вакансий, на которые можно откликнуться")
        
        return await self.vacancy_handler.get_applicable_vacancies()
    
    async def wait_for_vacancies_loaded(self, timeout: int = 30000) -> bool:
        """
        Шаг: Ожидание загрузки вакансий
        
        :param timeout: Таймаут ожидания в миллисекундах
        :return: True, если вакансии загружены
        """
        if self.logger:
            self.logger.info("Выполнение шага: Ожидание загрузки вакансий")
        
        return await self.vacancy_handler.wait_for_vacancies_loaded(timeout)