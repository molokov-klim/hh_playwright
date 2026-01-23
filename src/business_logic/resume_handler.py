"""
Обработчик резюме на hh.ru
"""
from ..pages.resume_page import ResumePage


class ResumeHandler:
    """Класс для обработки резюме на hh.ru"""
    
    def __init__(self, page, config, logger):
        """
        Инициализация обработчика резюме
        
        :param page: Страница Playwright
        :param config: Объект конфигурации
        :param logger: Объект логгера
        """
        self.page = page
        self.config = config
        self.logger = logger
        self.resume_page = ResumePage(page, config, logger)
    
    async def navigate_to_my_resumes(self) -> bool:
        """
        Переход на страницу 'Мои резюме'

        :return: True, если переход выполнен успешно
        """
        if self.logger:
            self.logger.info("Переход на страницу 'Мои резюме'")

        # Переходим напрямую на страницу моих резюме
        try:
            await self.page.goto("https://hh.ru/applicant/resumes")
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Ошибка при переходе на страницу 'Мои резюме': {e}")
            return False
    
    async def select_first_resume(self) -> bool:
        """
        Выбор первого резюме на странице
        
        :return: True, если выбор выполнен успешно
        """
        if self.logger:
            self.logger.info("Выбор первого резюме")
        
        return await self.resume_page.select_first_resume()
    
    async def select_resume_by_index(self, index: int) -> bool:
        """
        Выбор резюме по индексу
        
        :param index: Индекс резюме (начиная с 0)
        :return: True, если выбор выполнен успешно
        """
        if self.logger:
            self.logger.info(f"Выбор резюме с индексом {index}")
        
        return await self.resume_page.select_resume_by_index(index)
    
    async def go_to_recommended_vacancies(self) -> bool:
        """
        Переход к рекомендуемым вакансиям
        
        :return: True, если переход выполнен успешно
        """
        if self.logger:
            self.logger.info("Переход к рекомендуемым вакансиям")
        
        return await self.resume_page.go_to_recommended_vacancies()
    
    async def wait_for_vacancies_loaded(self, timeout: int = 30000) -> bool:
        """
        Ожидание загрузки вакансий
        
        :param timeout: Таймаут ожидания в миллисекундах
        :return: True, если вакансии загружены
        """
        if self.logger:
            self.logger.debug("Ожидание загрузки вакансий")
        
        return await self.resume_page.wait_for_vacancies_loaded(timeout)
    
    async def get_vacancy_count(self) -> int:
        """
        Получение количества найденных вакансий
        
        :return: Количество вакансий
        """
        return await self.resume_page.get_vacancy_count()