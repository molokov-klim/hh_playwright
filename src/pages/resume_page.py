"""
Page Object для страницы резюме hh.ru
"""
from playwright.async_api import Page
from .base_page import BasePage, PageProtocol


class ResumePage(BasePage):
    """Page Object для страницы резюме"""
    
    def __init__(self, page: PageProtocol, config=None, logger=None):
        """Инициализация страницы резюме"""
        super().__init__(page, config, logger)
        
        # Селекторы для элементов страницы резюме
        self.resume_list_item_selectors = [
            "[data-qa='resume-list-item']",
            ".resume-list-item",
            "[data-qa*='resume']",
            ".bloko-card"
        ]
        
        self.first_resume_selectors = [
            "[data-qa='resume-list-item']:first-child",
            ".resume-list-item:first-child",
            "[data-qa='resume-list-item']:nth-child(1)"
        ]
        
        self.recommended_vacancies_tab_selectors = [
            "[data-qa='recommended-vacancies-tab']",
            "text=Рекомендуемые вакансии",
            "[href*='recommended']",
            "a:has-text('Рекомендуемые вакансии')"
        ]
        
        self.vacancy_cards_selectors = [
            "[data-qa='vacancy']",
            ".vacancy-serp-item",
            "[data-qa*='vacancy']",
            ".serp-item"
        ]
    
    async def select_first_resume(self) -> bool:
        """Выбор первого резюме на странице"""
        for selector in self.first_resume_selectors:
            if await self.safe_click(selector):
                if self.logger:
                    self.logger.debug(f"Выбрано первое резюме с селектором: {selector}")
                return True
        
        if self.logger:
            self.logger.error("Не удалось найти и выбрать первое резюме")
        return False
    
    async def select_resume_by_index(self, index: int) -> bool:
        """Выбор резюме по индексу"""
        selector = f"[data-qa='resume-list-item']:nth-child({index+1})"
        if await self.safe_click(selector):
            if self.logger:
                self.logger.debug(f"Выбрано резюме с индексом {index} с селектором: {selector}")
            return True
        
        if self.logger:
            self.logger.error(f"Не удалось найти и выбрать резюме с индексом {index}")
        return False
    
    async def go_to_recommended_vacancies(self) -> bool:
        """Переход к рекомендуемым вакансиям"""
        for selector in self.recommended_vacancies_tab_selectors:
            if await self.safe_click(selector):
                if self.logger:
                    self.logger.debug(f"Переход к рекомендуемым вакансиям с селектором: {selector}")
                return True
        
        if self.logger:
            self.logger.error("Не удалось найти вкладку 'Рекомендуемые вакансии'")
        return False
    
    async def wait_for_vacancies_loaded(self, timeout: int = 30000) -> bool:
        """Ожидание загрузки вакансий"""
        for selector in self.vacancy_cards_selectors:
            if await self.wait_for_element(selector, timeout):
                if self.logger:
                    self.logger.debug(f"Вакансии загружены, найден селектор: {selector}")
                return True
        
        if self.logger:
            self.logger.error("Не удалось дождаться загрузки вакансий")
        return False
    
    async def get_vacancy_count(self) -> int:
        """Получение количества найденных вакансий"""
        for selector in self.vacancy_cards_selectors:
            try:
                locator = self.page.locator(selector)
                count = await locator.count()
                return count
            except Exception:
                continue
        
        return 0