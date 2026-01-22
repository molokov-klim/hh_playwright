"""
Модуль навигации по hh.ru
"""
from typing import Protocol


class PageProtocol(Protocol):
    """Протокол для страницы Playwright"""
    async def goto(self, url: str) -> None: ...
    async def click(self, selector: str) -> None: ...
    async def wait_for_selector(self, selector: str, **kwargs) -> None: ...
    async def wait_for_url(self, url: str, **kwargs) -> None: ...
    def locator(self, selector: str): ...


class HHNavigation:
    """Класс для навигации по hh.ru"""

    def __init__(self, config, logger):
        """
        Инициализация класса навигации
        
        :param config: Объект конфигурации
        :param logger: Объект логгера
        """
        self.config = config
        self.logger = logger

    async def navigate_to_my_resumes(self, page: PageProtocol) -> None:
        """
        Переход на страницу 'Мои резюме'
        
        :param page: Страница Playwright
        """
        self.logger.info("Переход на страницу 'Мои резюме'")
        await page.goto("https://hh.ru/applicant/resumes")

    async def select_resume(self, page: PageProtocol, resume_id: str) -> None:
        """
        Выбор резюме по ID
        
        :param page: Страница Playwright
        :param resume_id: ID резюме
        """
        self.logger.info(f"Выбор резюме с ID: {resume_id}")
        await page.click(f"[data-qa='resume-list-item-{resume_id}']")

    async def select_first_resume(self, page: PageProtocol) -> None:
        """
        Выбор первого резюме на странице
        
        :param page: Страница Playwright
        """
        self.logger.info("Выбор первого резюме")
        await page.click("[data-qa='resume-list-item']:first-child")

    async def go_to_recommended_vacancies(self, page: PageProtocol, resume_id: str) -> None:
        """
        Переход к рекомендуемым вакансиям для указанного резюме
        
        :param page: Страница Playwright
        :param resume_id: ID резюме
        """
        self.logger.info(f"Переход к рекомендуемым вакансиям для резюме {resume_id}")
        # Клик по вкладке/ссылке "Рекомендуемые вакансии"
        await page.click("[data-qa='recommended-vacancies-tab']")

    async def wait_for_vacancies_loaded(self, page: PageProtocol) -> None:
        """
        Ожидание загрузки вакансий на странице
        
        :param page: Страница Playwright
        """
        self.logger.debug("Ожидание загрузки вакансий")
        await page.wait_for_selector("[data-qa='vacancy']", timeout=self.config.TIMEOUT)