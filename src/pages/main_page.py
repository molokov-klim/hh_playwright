"""
Page Object для главной страницы hh.ru
"""
from playwright.async_api import Page
from .base_page import BasePage, PageProtocol


class MainPage(BasePage):
    """Page Object для главной страницы hh.ru"""
    
    def __init__(self, page: PageProtocol, config=None, logger=None):
        """Инициализация главной страницы"""
        super().__init__(page, config, logger)
        
        # Селекторы для элементов главной страницы
        self.my_resumes_link_selectors = [
            "[href='/applicant/resumes']",
            "[data-qa='main-skills-link']",
            "text=Мои резюме",
            "[href*='my-resumes']",
            "[href*='resume']"
        ]
        
        self.search_vacancies_input_selectors = [
            "[data-qa='vacancy-search-query-input']",
            "[name='text']",
            "[placeholder*='вакансии'], [placeholder*='работа']",
            "#search-input, #vacancy-search-input"
        ]
        
        self.search_button_selectors = [
            "[data-qa='search-button']",
            "[type='submit']",
            "button:has-text('Найти')",
            "button:has-text('Поиск')"
        ]
    
    async def navigate_to_my_resumes(self) -> bool:
        """Переход на страницу 'Мои резюме'"""
        for selector in self.my_resumes_link_selectors:
            if await self.safe_click(selector):
                if self.logger:
                    self.logger.debug(f"Переход на 'Мои резюме' с селектором: {selector}")
                return True
        
        if self.logger:
            self.logger.error("Не удалось найти ссылку на 'Мои резюме'")
        return False
    
    async def search_vacancies(self, query: str) -> bool:
        """Поиск вакансий по запросу"""
        # Заполнить поле поиска
        for selector in self.search_vacancies_input_selectors:
            if await self.safe_fill(selector, query):
                if self.logger:
                    self.logger.debug(f"Заполнено поле поиска с селектором: {selector}")
                break
        else:
            if self.logger:
                self.logger.error("Не удалось найти поле поиска вакансий")
            return False
        
        # Кликнуть кнопку поиска
        for selector in self.search_button_selectors:
            if await self.safe_click(selector):
                if self.logger:
                    self.logger.debug(f"Клик по кнопке поиска с селектором: {selector}")
                return True
        
        if self.logger:
            self.logger.error("Не удалось найти кнопку поиска")
        return False