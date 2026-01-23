"""
Page Object для страницы вакансий hh.ru
"""
from playwright.async_api import Page, Locator
from .base_page import BasePage, PageProtocol


class VacancyPage(BasePage):
    """Page Object для страницы вакансий"""
    
    def __init__(self, page: PageProtocol, config=None, logger=None):
        """Инициализация страницы вакансий"""
        super().__init__(page, config, logger)
        
        # Селекторы для элементов страницы вакансий
        self.vacancy_cards_selectors = [
            "[data-qa='vacancy']",
            ".vacancy-serp-item",
            "[data-qa*='vacancy']",
            ".serp-item"
        ]
        
        self.apply_button_selectors = [
            "[data-qa='apply-button']",
            "text=Откликнуться",
            "button:has-text('Откликнуться')",
            "[data-qa*='response']",
            "[href*='response']"
        ]
        
        self.success_message_selectors = [
            "[data-qa='success-message']",
            "text=Отклик отправлен",
            "text=Ваш отклик",
            ".success-message",
            "[data-qa*='response-success']"
        ]
        
        self.vacancy_title_selectors = [
            "[data-qa='vacancy-title']",
            ".vacancy-title",
            "[data-qa*='title']",
            "h3, h2"
        ]
        
        self.vacancy_id_selectors = [
            "[data-qa='vacancy-id']",
            "[data-id]",
            "[data-qa*='vacancy']"
        ]
    
    async def get_vacancy_locators(self) -> list[Locator]:
        """Получение локаторов всех вакансий на странице"""
        for selector in self.vacancy_cards_selectors:
            try:
                locator = self.page.locator(selector)
                count = await locator.count()
                if count > 0:
                    locators = []
                    for i in range(count):
                        locators.append(locator.nth(i))
                    return locators
            except Exception:
                continue
        
        return []
    
    async def is_apply_button_available(self, vacancy_locator: Locator) -> bool:
        """Проверка доступности кнопки отклика для вакансии"""
        for selector in self.apply_button_selectors:
            try:
                button_locator = vacancy_locator.locator(selector)
                count = await button_locator.count()
                if count > 0:
                    return True
            except Exception:
                continue
        
        return False
    
    async def get_applicable_vacancies(self) -> list[Locator]:
        """Получение списка вакансий, на которые можно откликнуться"""
        all_vacancies = await self.get_vacancy_locators()
        applicable_vacancies = []
        
        for vacancy in all_vacancies:
            if await self.is_apply_button_available(vacancy):
                applicable_vacancies.append(vacancy)
        
        if self.logger:
            self.logger.info(f"Найдено {len(applicable_vacancies)} вакансий, на которые можно откликнуться")
        
        return applicable_vacancies
    
    async def get_vacancy_info(self, vacancy_locator: Locator) -> tuple[str, str]:
        """Получение информации о вакансии (название, ID)"""
        title = ""
        vacancy_id = ""
        
        # Получение названия вакансии
        for selector in self.vacancy_title_selectors:
            try:
                title_element = vacancy_locator.locator(selector)
                title = await title_element.inner_text()
                if title:
                    break
            except Exception:
                continue
        
        # Получение ID вакансии
        for selector in self.vacancy_id_selectors:
            try:
                id_element = vacancy_locator.locator(selector)
                vacancy_id = await id_element.get_attribute("data-id") or ""
                if vacancy_id:
                    break
            except Exception:
                continue
        
        return title.strip(), vacancy_id.strip()
    
    async def click_apply_button(self, vacancy_locator: Locator) -> bool:
        """Клик по кнопке отклика на вакансию"""
        for selector in self.apply_button_selectors:
            if await self.safe_click(selector):
                if self.logger:
                    self.logger.debug(f"Клик по кнопке отклика с селектором: {selector}")
                return True
        
        if self.logger:
            self.logger.error("Не удалось найти кнопку отклика")
        return False
    
    async def wait_for_application_result(self, timeout: int = 30000) -> str:
        """Ожидание результата отклика"""
        for selector in self.success_message_selectors:
            try:
                await self.page.wait_for_selector(selector, timeout=timeout)
                return "Успешно"
            except Exception:
                continue

        return "Ошибка"

    async def wait_for_vacancies_loaded(self, timeout: int = 30000) -> bool:
        """Ожидание загрузки вакансий"""
        for selector in self.vacancy_cards_selectors:
            try:
                await self.page.wait_for_selector(selector, timeout=timeout)
                return True
            except Exception:
                continue

        return False