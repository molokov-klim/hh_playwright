"""
Page Object для страницы отправки откликов hh.ru
"""
from playwright.async_api import Page
from .base_page import BasePage, PageProtocol


class ApplicationPage(BasePage):
    """Page Object для страницы отправки откликов"""
    
    def __init__(self, page: PageProtocol, config=None, logger=None):
        """Инициализация страницы отправки откликов"""
        super().__init__(page, config, logger)
        
        # Селекторы для элементов страницы отправки откликов
        self.response_form_selectors = [
            "[data-qa='response-form']",
            ".response-form",
            "[data-qa*='response']",
            ".vacancy-response-form"
        ]
        
        self.cover_letter_textarea_selectors = [
            "[data-qa='response-cover-letter']",
            "textarea[name='message']",
            "[placeholder*='сопроводительное'], [placeholder*='cover letter']",
            "#cover-letter, #message"
        ]
        
        self.send_response_button_selectors = [
            "[data-qa='send-response-button']",
            "text=Отправить отклик",
            "button:has-text('Отправить отклик')",
            "[type='submit']",
            "button:has-text('Отправить')"
        ]
        
        self.success_response_selectors = [
            "[data-qa='response-success']",
            "text=Отклик отправлен",
            "text=Ваш отклик",
            ".success-response",
            "[data-qa*='success']"
        ]
        
        self.error_response_selectors = [
            "[data-qa='response-error']",
            "text=Ошибка",
            ".error-response",
            "[data-qa*='error']"
        ]
    
    async def fill_cover_letter(self, cover_letter: str) -> bool:
        """Заполнение сопроводительного письма"""
        for selector in self.cover_letter_textarea_selectors:
            if await self.safe_fill(selector, cover_letter):
                if self.logger:
                    self.logger.debug(f"Заполнено сопроводительное письмо с селектором: {selector}")
                return True
        
        if self.logger:
            self.logger.error("Не удалось найти поле для сопроводительного письма")
        return False
    
    async def click_send_response(self) -> bool:
        """Клик по кнопке отправки отклика"""
        for selector in self.send_response_button_selectors:
            if await self.safe_click(selector):
                if self.logger:
                    self.logger.debug(f"Клик по кнопке отправки отклика с селектором: {selector}")
                return True
        
        if self.logger:
            self.logger.error("Не удалось найти кнопку отправки отклика")
        return False
    
    async def wait_for_response_result(self, timeout: int = 30000) -> str:
        """Ожидание результата отправки отклика"""
        # Проверка на успех
        for selector in self.success_response_selectors:
            try:
                await self.page.wait_for_selector(selector, timeout=5000)
                if self.logger:
                    self.logger.debug(f"Обнаружен успех отклика: {selector}")
                return "Успешно"
            except Exception:
                continue
        
        # Проверка на ошибку
        for selector in self.error_response_selectors:
            try:
                await self.page.wait_for_selector(selector, timeout=5000)
                if self.logger:
                    self.logger.debug(f"Обнаружена ошибка отклика: {selector}")
                return "Ошибка"
            except Exception:
                continue
        
        # Если за указанный таймаут ничего не произошло
        try:
            await self.page.wait_for_timeout(timeout)
            return "Таймаут"
        except Exception:
            return "Ошибка"