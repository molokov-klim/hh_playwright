"""
Модуль навигации по hh.ru
"""
import warnings
from typing import Protocol

from src.pages.main_page import MainPage
from src.pages.resume_page import ResumePage
from src.business_logic.resume_handler import ResumeHandler
from src.steps.resume_steps import ResumeSteps


# Предупреждение об устаревшем модуле
warnings.warn(
    "Модуль src.navigation устарел. Используйте src.steps.resume_steps.ResumeSteps или "
    "src.business_logic.resume_handler.ResumeHandler вместо этого модуля.",
    DeprecationWarning,
    stacklevel=2
)


class PageProtocol(Protocol):
    """Протокол для страницы Playwright"""
    async def goto(self, url: str) -> None: ...
    async def click(self, selector: str) -> None: ...
    async def wait_for_selector(self, selector: str, **kwargs) -> None: ...
    async def wait_for_url(self, url: str, **kwargs) -> None: ...
    def locator(self, selector: str): ...


class HHNavigation:
    """Класс для навигации по hh.ru (устаревший)"""

    def __init__(self, config, logger):
        """
        Инициализация класса навигации

        :param config: Объект конфигурации
        :param logger: Объект логгера
        """
        warnings.warn(
            "HHNavigation устарел. Используйте ResumeHandler или ResumeSteps вместо этого класса.",
            DeprecationWarning,
            stacklevel=2
        )
        self.config = config
        self.logger = logger

    async def navigate_to_my_resumes(self, page: PageProtocol) -> None:
        """
        Переход на страницу 'Мои резюме'

        :param page: Страница Playwright
        """
        warnings.warn(
            "navigate_to_my_resumes устарел. Используйте ResumeHandler.navigate_to_my_resumes "
            "или ResumeSteps.navigate_to_my_resumes вместо этого метода.",
            DeprecationWarning,
            stacklevel=2
        )
        # Используем новый подход
        resume_handler = ResumeHandler(page, self.config, self.logger)
        await resume_handler.navigate_to_my_resumes()

    async def select_resume(self, page: PageProtocol, resume_id: str) -> None:
        """
        Выбор резюме по ID

        :param page: Страница Playwright
        :param resume_id: ID резюме
        """
        warnings.warn(
            "select_resume устарел.",
            DeprecationWarning,
            stacklevel=2
        )
        # В новой архитектуре выбор резюме по ID не реализован напрямую, 
        # но можно использовать индексный подход

    async def select_first_resume(self, page: PageProtocol) -> None:
        """
        Выбор первого резюме на странице

        :param page: Страница Playwright
        """
        warnings.warn(
            "select_first_resume устарел. Используйте ResumeHandler.select_first_resume "
            "или ResumeSteps.select_first_resume вместо этого метода.",
            DeprecationWarning,
            stacklevel=2
        )
        # Используем новый подход
        resume_handler = ResumeHandler(page, self.config, self.logger)
        await resume_handler.select_first_resume()

    async def go_to_recommended_vacancies(self, page: PageProtocol, resume_id: str) -> None:
        """
        Переход к рекомендуемым вакансиям для указанного резюме

        :param page: Страница Playwright
        :param resume_id: ID резюме
        """
        warnings.warn(
            "go_to_recommended_vacancies устарел. Используйте ResumeHandler.go_to_recommended_vacancies "
            "или ResumeSteps.go_to_recommended_vacancies вместо этого метода.",
            DeprecationWarning,
            stacklevel=2
        )
        # Используем новый подход
        resume_handler = ResumeHandler(page, self.config, self.logger)
        await resume_handler.go_to_recommended_vacancies()

    async def wait_for_vacancies_loaded(self, page: PageProtocol) -> None:
        """
        Ожидание загрузки вакансий на странице

        :param page: Страница Playwright
        """
        warnings.warn(
            "wait_for_vacancies_loaded устарел. Используйте ResumeHandler.wait_for_vacancies_loaded "
            "или ResumeSteps.wait_for_vacancies_loaded вместо этого метода.",
            DeprecationWarning,
            stacklevel=2
        )
        # Используем новый подход
        resume_handler = ResumeHandler(page, self.config, self.logger)
        await resume_handler.wait_for_vacancies_loaded()