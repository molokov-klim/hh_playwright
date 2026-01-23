"""
Обработчик вакансий на hh.ru
"""
from ..pages.vacancy_page import VacancyPage


class VacancyHandler:
    """Класс для обработки вакансий на hh.ru"""
    
    def __init__(self, page, config, logger):
        """
        Инициализация обработчика вакансий
        
        :param page: Страница Playwright
        :param config: Объект конфигурации
        :param logger: Объект логгера
        """
        self.page = page
        self.config = config
        self.logger = logger
        self.vacancy_page = VacancyPage(page, config, logger)
    
    async def get_vacancy_locators(self) -> list:
        """
        Получение локаторов всех вакансий на странице
        
        :return: Список локаторов вакансий
        """
        if self.logger:
            self.logger.debug("Получение локаторов вакансий")
        
        return await self.vacancy_page.get_vacancy_locators()
    
    async def is_apply_button_available(self, vacancy_locator) -> bool:
        """
        Проверка доступности кнопки отклика для вакансии
        
        :param vacancy_locator: Локатор вакансии
        :return: True, если кнопка отклика доступна
        """
        return await self.vacancy_page.is_apply_button_available(vacancy_locator)
    
    async def get_applicable_vacancies(self) -> list:
        """
        Получение списка вакансий, на которые можно откликнуться
        
        :return: Список локаторов вакансий, на которые можно откликнуться
        """
        if self.logger:
            self.logger.debug("Получение вакансий, на которые можно откликнуться")
        
        return await self.vacancy_page.get_applicable_vacancies()
    
    async def get_vacancy_info(self, vacancy_locator) -> tuple[str, str]:
        """
        Получение информации о вакансии (название, ID)
        
        :param vacancy_locator: Локатор вакансии
        :return: Кортеж с названием и ID вакансии
        """
        return await self.vacancy_page.get_vacancy_info(vacancy_locator)
    
    async def wait_for_vacancies_loaded(self, timeout: int = 30000) -> bool:
        """
        Ожидание загрузки вакансий
        
        :param timeout: Таймаут ожидания в миллисекундах
        :return: True, если вакансии загружены
        """
        if self.logger:
            self.logger.debug("Ожидание загрузки вакансий")
        
        return await self.vacancy_page.wait_for_vacancies_loaded(timeout)