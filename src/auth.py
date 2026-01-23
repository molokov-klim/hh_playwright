"""
Модуль авторизации на hh.ru
"""
import asyncio
from typing import Protocol

from src.config import Config


class PageProtocol(Protocol):
    """Протокол для страницы Playwright"""
    async def goto(self, url: str) -> None: ...
    async def fill(self, selector: str, value: str) -> None: ...
    async def click(self, selector: str) -> None: ...
    async def wait_for_selector(self, selector: str, **kwargs) -> None: ...
    async def is_visible(self, selector: str) -> bool: ...
    def locator(self, selector: str): ...


class HHAuth:
    """Класс для авторизации на hh.ru"""

    def __init__(self, config: Config, logger):
        """
        Инициализация класса авторизации
        
        :param config: Объект конфигурации
        :param logger: Объект логгера
        """
        self.config = config
        self.logger = logger

    async def perform_auth(self, page: PageProtocol) -> bool:
        """
        Выполнение авторизации на hh.ru

        :param page: Страница Playwright
        :return: True, если авторизация прошла успешно
        """
        self.logger.info("Начало процесса авторизации")

        # Переход на главную страницу hh.ru
        await page.goto("https://hh.ru")

        # Клик по кнопке "Войти" - может быть несколько вариантов селектора
        try:
            # Пробуем разные возможные селекторы для кнопки входа
            selectors_to_try = [
                ".supernova-auth-header-switch__link",  # Современный интерфейс hh.ru (основной)
                "[data-qa='login']",  # Оригинальный селектор
                ".bloko-header-controls-item a[href*='login']",  # Ссылка в шапке
                "[href='/account/login']",  # Ссылка на страницу входа
                "text=Войти",  # Текстовая кнопка
                "button:has-text('Войти')",  # Кнопка с текстом "Войти"
                ".supernova-auth-header-switch__link sup[data-qa*='login']"  # Современный интерфейс
            ]

            login_clicked = False
            for selector in selectors_to_try:
                try:
                    await page.wait_for_selector(selector, timeout=5000)
                    await page.click(selector)
                    self.logger.debug(f"Клик по кнопке входа с селектором: {selector}")
                    login_clicked = True
                    break
                except:
                    continue

            if not login_clicked:
                # Если не удалось найти кнопку входа, возможно, мы уже на странице входа
                # или страница уже содержит поля ввода
                self.logger.warning("Не найдена кнопка входа, проверяем наличие полей ввода")

        except Exception as e:
            self.logger.warning(f"Не удалось кликнуть по кнопке входа: {e}")

        # Заполнение формы логина
        await self._fill_login_form(page)

        # Заполнение формы пароля
        await self._fill_password_form(page)

        # Проверка успешной авторизации
        auth_success = await self._check_auth_success(page)

        if not auth_success:
            raise Exception("Authentication failed")

        self.logger.info("Авторизация прошла успешно")
        return True

    async def _fill_login_form(self, page: PageProtocol) -> None:
        """Заполнение формы логина (email/телефон)"""
        self.logger.debug("Заполнение формы логина")

        # Ожидание появления поля ввода логина - пробуем разные возможные селекторы
        selectors_to_try = [
            "[name='username']",  # Обычное имя поля
            "[name='login']",  # Альтернативное имя
            "[name='email_or_phone']",  # Возможное имя для email или телефона
            "[type='email']",  # Поле email
            "[type='tel']",  # Поле телефона
            "[placeholder*='логин'], [placeholder*='email'], [placeholder*='телефон'], [placeholder*='почта']",  # Плейсхолдеры
            "#login, #username, #email, #phone",  # ID полей
            "[data-qa='login-input']",  # Оригинальный селектор
            "input:not([type='hidden']):not([disabled]):not([readonly]):first-child"  # Первое доступное поле ввода
        ]

        login_field_filled = False
        for selector in selectors_to_try:
            try:
                await page.wait_for_selector(selector, timeout=10000)
                await page.fill(selector, self.config.HH_LOGIN)
                self.logger.debug(f"Заполнено поле логина с селектором: {selector}")
                login_field_filled = True

                # После заполнения логина, пробуем найти и нажать кнопку "Продолжить"
                button_selectors = [
                    "text=Продолжить",  # Текст кнопки
                    "button:has-text('Продолжить')",  # Кнопка с текстом
                    "[data-qa='login-button-next']",  # Оригинальная кнопка
                    "button[type='submit']:not([data-qa*='password'])",  # Кнопка отправки формы
                    "button:has-text('Войти')",  # Альтернативная кнопка
                    "button[type='button']:first-of-type",  # Первая кнопка
                    "input[type='submit']"  # Кнопка отправки формы
                ]

                button_clicked = False
                for btn_selector in button_selectors:
                    try:
                        await page.wait_for_selector(btn_selector, timeout=5000)
                        await page.click(btn_selector)
                        self.logger.debug(f"Клик по кнопке с селектором: {btn_selector}")
                        button_clicked = True
                        break
                    except:
                        continue

                if not button_clicked:
                    self.logger.warning("Не найдена кнопка 'Продолжить', возможно, форма сразу перешла к паролю")

                break
            except:
                continue

        if not login_field_filled:
            raise Exception("Не удалось найти и заполнить поле логина")

    async def _fill_password_form(self, page: PageProtocol) -> None:
        """Заполнение формы пароля"""
        self.logger.debug("Заполнение формы пароля")

        # Ожидание появления поля ввода пароля - пробуем разные возможные селекторы
        selectors_to_try = [
            "[name='password']",  # Обычное имя поля
            "[type='password']",  # Поле пароля
            "[placeholder*='пароль'], [placeholder*='Password']",  # Плейсхолдер
            "#password",  # ID поля
            "[data-qa='password-input']",  # Оригинальный селектор
            "input[type='password']:not([disabled]):not([readonly])"  # Любое доступное поле пароля
        ]

        password_field_filled = False
        for selector in selectors_to_try:
            try:
                await page.wait_for_selector(selector, timeout=10000)
                await page.fill(selector, self.config.HH_PASSWORD)
                self.logger.debug(f"Заполнено поле пароля с селектором: {selector}")
                password_field_filled = True

                # После заполнения пароля, пробуем найти и нажать кнопку "Войти"
                button_selectors = [
                    "text=Войти",  # Текст кнопки
                    "button:has-text('Войти')",  # Кнопка с текстом
                    "[data-qa='login-button-submit']",  # Оригинальная кнопка
                    "button[type='submit']",  # Кнопка отправки формы
                    "[type='submit'][value], [role='button']",  # Альтернативные кнопки
                    "button:has-text('Отправить')"  # Альтернативная кнопка
                ]

                button_clicked = False
                for btn_selector in button_selectors:
                    try:
                        await page.wait_for_selector(btn_selector, timeout=5000)
                        await page.click(btn_selector)
                        self.logger.debug(f"Клик по кнопке входа с селектором: {btn_selector}")
                        button_clicked = True
                        break
                    except:
                        continue

                if not button_clicked:
                    self.logger.warning("Не найдена кнопка 'Войти', пробуем нажать Enter")
                    # Если кнопка не найдена, пробуем нажать Enter в поле пароля
                    await page.press(selector, "Enter")

                break
            except:
                continue

        if not password_field_filled:
            raise Exception("Не удалось найти и заполнить поле пароля")

    async def _check_auth_success(self, page: PageProtocol) -> bool:
        """
        Проверка успешной авторизации

        :param page: Страница Playwright
        :return: True, если авторизация успешна
        """
        self.logger.debug("Проверка успешной авторизации")

        # Ожидание появления элемента, характерного для авторизованного пользователя
        # Это может быть аватарка пользователя в шапке или ссылка "Мои резюме"

        # Пробуем разные возможные селекторы для проверки авторизации
        success_indicators = [
            ".supernova-user-info",  # Современный интерфейс hh.ru (основной)
            "[data-qa='header-menu-account']",  # Оригинальный селектор
            "[data-qa*='account'], [data-qa*='profile']",  # Элементы профиля
            ".bloko-header-controls-item .supernova-user-info",  # Современный интерфейс
            "[href='/applicant/resumes'], [href*='/my-resumes'], [href*='my']",  # Ссылка на резюме
            ".supernova-auth-header-switch__link sup:not([data-qa*='login'])",  # Не кнопка входа
            "text=Выйти",  # Текст "Выйти" обычно появляется после входа
            "[aria-label='Профиль'], [alt='Аватар'], [data-name='AccountMenu'], [data-qa*='user']",  # Альтернативные индикаторы
            ".bloko-header-controls-item a[href*='account'], .bloko-header-controls-item a[href*='profile']"  # Ссылки в шапке
        ]

        for selector in success_indicators:
            try:
                # Ждем появления элемента с определенным таймаутом
                await page.wait_for_selector(selector, timeout=10000)

                # Проверяем видимость элемента
                is_logged_in = await page.is_visible(selector)

                if is_logged_in:
                    self.logger.debug(f"Обнаружен элемент авторизации: {selector}")
                    return True
            except:
                continue

        # Если ни один из индикаторов не найден, значит пользователь не авторизован
        return False