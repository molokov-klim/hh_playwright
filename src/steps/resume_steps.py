"""
Шаги работы с резюме на hh.ru
"""
from ..business_logic.resume_handler import ResumeHandler


class ResumeSteps:
    """Класс для шагов работы с резюме на hh.ru"""
    
    def __init__(self, page, config, logger):
        """
        Инициализация шагов работы с резюме
        
        :param page: Страница Playwright
        :param config: Объект конфигурации
        :param logger: Объект логгера
        """
        self.page = page
        self.config = config
        self.logger = logger
        self.resume_handler = ResumeHandler(page, config, logger)
    
    async def navigate_to_my_resumes(self) -> bool:
        """
        Шаг: Переход на страницу 'Мои резюме'
        
        :return: True, если переход выполнен успешно
        """
        if self.logger:
            self.logger.info("Выполнение шага: Переход на страницу 'Мои резюме'")
        
        return await self.resume_handler.navigate_to_my_resumes()
    
    async def select_first_resume(self) -> bool:
        """
        Шаг: Выбор первого резюме
        
        :return: True, если выбор выполнен успешно
        """
        if self.logger:
            self.logger.info("Выполнение шага: Выбор первого резюме")
        
        return await self.resume_handler.select_first_resume()
    
    async def select_resume_by_index(self, index: int) -> bool:
        """
        Шаг: Выбор резюме по индексу
        
        :param index: Индекс резюме (начиная с 0)
        :return: True, если выбор выполнен успешно
        """
        if self.logger:
            self.logger.info(f"Выполнение шага: Выбор резюме с индексом {index}")
        
        return await self.resume_handler.select_resume_by_index(index)
    
    async def go_to_recommended_vacancies(self) -> bool:
        """
        Шаг: Переход к рекомендуемым вакансиям
        
        :return: True, если переход выполнен успешно
        """
        if self.logger:
            self.logger.info("Выполнение шага: Переход к рекомендуемым вакансиям")
        
        return await self.resume_handler.go_to_recommended_vacancies()
    
    async def wait_for_vacancies_loaded(self, timeout: int = 30000) -> bool:
        """
        Шаг: Ожидание загрузки вакансий
        
        :param timeout: Таймаут ожидания в миллисекундах
        :return: True, если вакансии загружены
        """
        if self.logger:
            self.logger.info("Выполнение шага: Ожидание загрузки вакансий")
        
        return await self.resume_handler.wait_for_vacancies_loaded(timeout)