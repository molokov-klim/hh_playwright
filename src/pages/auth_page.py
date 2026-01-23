"""
Page Object для страницы авторизации на hh.ru
"""
from playwright.async_api import Page
from .base_page import BasePage, PageProtocol


class AuthPage(BasePage):
    """Page Object для страницы авторизации"""
    
    def __init__(self, page: PageProtocol, config=None, logger=None):
        """Инициализация страницы авторизации"""
        super().__init__(page, config, logger)
        
        # Селекторы для страницы авторизации
        self.login_input_selectors = [
            "[name='username']",
            "[name='login']",
            "[name='email_or_phone']",
            "[type='email']",
            "[type='tel']",
            "[placeholder*='логин'], [placeholder*='email'], [placeholder*='телефон'], [placeholder*='почта']",
            "#login, #username, #email, #phone",
            "[data-qa='login-input']",
            "input:not([type='hidden']):not([disabled]):not([readonly']):first-child"
        ]
        
        self.password_input_selectors = [
            "[name='password']",
            "[type='password']",
            "[placeholder*='пароль'], [placeholder*='Password']",
            "#password",
            "[data-qa='password-input']",
            "input[type='password']:not([disabled]):not([readonly])"
        ]
        
        self.login_button_selectors = [
            "text=Продолжить",
            "button:has-text('Продолжить')",
            "[data-qa='login-button-next']",
            "button[type='submit']:not([data-qa*='password'])",
            "button:has-text('Войти')",
            "button[type='button']:first-of-type",
            "input[type='submit']"
        ]
        
        self.submit_button_selectors = [
            "text=Войти",
            "button:has-text('Войти')",
            "[data-qa='login-button-submit']",
            "button[type='submit']",
            "[type='submit'][value], [role='button']",
            "button:has-text('Отправить')"
        ]
        
        self.auth_indicators = [
            ".supernova-user-info",
            "[data-qa='header-menu-account']",
            "[data-qa*='account'], [data-qa*='profile']",
            ".bloko-header-controls-item .supernova-user-info",
            "[href='/applicant/resumes'], [href*='/my-resumes'], [href*='my']",
            ".supernova-auth-header-switch__link sup:not([data-qa*='login'])",
            "text=Выйти",
            "[aria-label='Профиль'], [alt='Аватар'], [data-name='AccountMenu'], [data-qa*='user']",
            ".bloko-header-controls-item a[href*='account'], .bloko-header-controls-item a[href*='profile']"
        ]
        
        self.login_link_selectors = [
            ".supernova-auth-header-switch__link",
            "[data-qa='login']",
            ".bloko-header-controls-item a[href*='login']",
            "[href='/account/login']",
            "text=Войти",
            "button:has-text('Войти')",
            ".supernova-auth-header-switch__link sup[data-qa*='login']"
        ]
    
    async def navigate_to_login_page(self) -> bool:
        """Переход на страницу авторизации"""
        try:
            await self.page.goto("https://hh.ru")
            
            # Попробовать кликнуть по кнопке входа
            for selector in self.login_link_selectors:
                if await self.safe_click(selector, timeout=5000):
                    if self.logger:
                        self.logger.debug(f"Клик по кнопке входа с селектором: {selector}")
                    break
            
            return True
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Не удалось перейти на страницу авторизации: {e}")
            return False
    
    async def fill_login(self, login: str) -> bool:
        """Заполнение поля логина"""
        for selector in self.login_input_selectors:
            if await self.safe_fill(selector, login, timeout=10000):
                if self.logger:
                    self.logger.debug(f"Заполнено поле логина с селектором: {selector}")
                
                # Попробовать кликнуть кнопку "Продолжить"
                for btn_selector in self.login_button_selectors:
                    if await self.safe_click(btn_selector, timeout=5000):
                        if self.logger:
                            self.logger.debug(f"Клик по кнопке с селектором: {btn_selector}")
                        break
                
                return True
        
        if self.logger:
            self.logger.error("Не удалось найти и заполнить поле логина")
        return False
    
    async def fill_password(self, password: str) -> bool:
        """Заполнение поля пароля"""
        for selector in self.password_input_selectors:
            if await self.safe_fill(selector, password, timeout=10000):
                if self.logger:
                    self.logger.debug(f"Заполнено поле пароля с селектором: {selector}")
                
                # Попробовать кликнуть кнопку "Войти"
                for btn_selector in self.submit_button_selectors:
                    if await self.safe_click(btn_selector, timeout=5000):
                        if self.logger:
                            self.logger.debug(f"Клик по кнопке входа с селектором: {btn_selector}")
                        break
                    else:
                        # Если кнопка не найдена, пробуем нажать Enter в поле пароля
                        try:
                            await self.page.press(selector, "Enter")
                        except Exception:
                            pass
                
                return True
        
        if self.logger:
            self.logger.error("Не удалось найти и заполнить поле пароля")
        return False
    
    async def is_logged_in(self) -> bool:
        """Проверка, авторизован ли пользователь"""
        for selector in self.auth_indicators:
            try:
                if await self.wait_for_element(selector, timeout=10000):
                    is_visible = await self.is_element_visible(selector)
                    if is_visible:
                        if self.logger:
                            self.logger.debug(f"Обнаружен элемент авторизации: {selector}")
                        return True
            except Exception:
                continue
        
        return False