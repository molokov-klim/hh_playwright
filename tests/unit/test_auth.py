"""
Тесты для модуля авторизации на hh.ru
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch, MagicMock
import asyncio

from src.auth import HHAuth


pytest_plugins = ["pytest_asyncio"]


class TestHHAuth:
    """Тесты для класса HHAuth"""

    @pytest.fixture
    def mock_config(self):
        """Мок конфигурации"""
        config = Mock()
        config.HH_LOGIN = "test@example.com"
        config.HH_PASSWORD = "password123"
        return config

    @pytest.fixture
    def mock_page(self):
        """Мок страницы Playwright"""
        page = Mock()
        page.goto = AsyncMock()
        page.fill = AsyncMock()
        page.click = AsyncMock()
        page.wait_for_selector = AsyncMock()
        page.is_visible = AsyncMock(return_value=True)
        page.locator = Mock()
        return page

    @pytest.fixture
    def mock_logger(self):
        """Мок логгера"""
        logger = Mock()
        logger.info = Mock()
        logger.error = Mock()
        logger.debug = Mock()
        return logger

    def test_init_creates_correct_instance(self, mock_config, mock_logger):
        """Тест инициализации класса HHAuth"""
        # Выполнение
        auth = HHAuth(mock_config, mock_logger)

        # Проверка
        assert auth.config == mock_config
        assert auth.logger == mock_logger

    @pytest.mark.asyncio
    async def test_perform_auth_success(self, mock_config, mock_page, mock_logger):
        """Тест успешной авторизации"""
        # Подготовка
        auth = HHAuth(mock_config, mock_logger)
        
        # Мок для проверки успешной авторизации
        with patch.object(auth, '_check_auth_success', return_value=True):
            # Выполнение
            result = await auth.perform_auth(mock_page)

            # Проверка
            assert result is True
            # Проверяем, что были вызваны нужные методы
            mock_page.goto.assert_called_once()
            mock_page.fill.assert_any_call("[data-qa='login-input']", "test@example.com")
            mock_page.click.assert_called()

    @pytest.mark.asyncio
    async def test_perform_auth_failure(self, mock_config, mock_page, mock_logger):
        """Тест неудачной авторизации"""
        # Подготовка
        auth = HHAuth(mock_config, mock_logger)
        
        # Мок для проверки неудачной авторизации
        with patch.object(auth, '_check_auth_success', return_value=False):
            # Выполнение и проверка
            with pytest.raises(Exception, match="Authentication failed"):
                await auth.perform_auth(mock_page)

    @pytest.mark.asyncio
    async def test_fill_login_form(self, mock_config, mock_page, mock_logger):
        """Тест заполнения формы логина"""
        # Подготовка
        auth = HHAuth(mock_config, mock_logger)

        # Выполнение
        await auth._fill_login_form(mock_page)

        # Проверка
        mock_page.fill.assert_any_call("[data-qa='login-input']", "test@example.com")
        mock_page.click.assert_called_with("[data-qa='login-button-next']")

    @pytest.mark.asyncio
    async def test_fill_password_form(self, mock_config, mock_page, mock_logger):
        """Тест заполнения формы пароля"""
        # Подготовка
        auth = HHAuth(mock_config, mock_logger)

        # Выполнение
        await auth._fill_password_form(mock_page)

        # Проверка
        mock_page.fill.assert_any_call("[data-qa='password-input']", "password123")
        mock_page.click.assert_called_with("[data-qa='login-button-submit']")

    @pytest.mark.asyncio
    async def test_check_auth_success_returns_true_when_logged_in(self, mock_config, mock_page, mock_logger):
        """Тест проверки успешной авторизации - пользователь залогинен"""
        # Подготовка
        auth = HHAuth(mock_config, mock_logger)
        
        # Мок для проверки видимости элемента авторизованного пользователя
        mock_page.locator.return_value.is_visible = AsyncMock(return_value=True)

        # Выполнение
        result = await auth._check_auth_success(mock_page)

        # Проверка
        assert result is True

    @pytest.mark.asyncio
    async def test_check_auth_success_returns_false_when_not_logged_in(self, mock_config, mock_page, mock_logger):
        """Тест проверки успешной авторизации - пользователь не залогинен"""
        # Подготовка
        auth = HHAuth(mock_config, mock_logger)

        # Мок для проверки отсутствия элемента авторизованного пользователя
        # В данном случае, мы мокаем wait_for_selector, чтобы он выбросил исключение
        mock_page.wait_for_selector = AsyncMock(side_effect=Exception("Timeout"))

        # Выполнение
        result = await auth._check_auth_success(mock_page)

        # Проверка
        assert result is False