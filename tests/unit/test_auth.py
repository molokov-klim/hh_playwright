"""
Тесты для модуля авторизации на hh.ru (устаревший)
"""
import pytest
import warnings
from unittest.mock import AsyncMock, Mock, patch, MagicMock
import asyncio

from src.auth import HHAuth


pytest_plugins = ["pytest_asyncio"]


class TestHHAuth:
    """Тесты для класса HHAuth (устаревший)"""

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
        # Проверяем, что генерируется предупреждение об устаревании
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # Выполнение
            auth = HHAuth(mock_config, mock_logger)

            # Проверка
            assert auth.config == mock_config
            assert auth.logger == mock_logger
            # Проверяем, что было сгенерировано предупреждение
            assert len(w) >= 1
            assert issubclass(w[-1].category, DeprecationWarning)

    @pytest.mark.asyncio
    async def test_perform_auth_success(self, mock_config, mock_page, mock_logger):
        """Тест успешной авторизации"""
        # Проверяем, что генерируется предупреждение об устаревании
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # Подготовка
            auth = HHAuth(mock_config, mock_logger)

            # Проверяем, что было сгенерировано предупреждение
            assert len(w) >= 1
            assert issubclass(w[-1].category, DeprecationWarning)

        # Мок для проверки успешной авторизации
        with patch('src.auth.AuthHandler') as mock_auth_handler_class:
            mock_auth_handler = Mock()
            mock_auth_handler.perform_auth = AsyncMock(return_value=True)
            mock_auth_handler_class.return_value = mock_auth_handler

            # Выполнение
            result = await auth.perform_auth(mock_page)

            # Проверка
            assert result is True
            # Проверяем, что был вызван новый обработчик
            mock_auth_handler.perform_auth.assert_called_once()

    @pytest.mark.asyncio
    async def test_perform_auth_failure(self, mock_config, mock_page, mock_logger):
        """Тест неудачной авторизации"""
        # Проверяем, что генерируется предупреждение об устаревании
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # Подготовка
            auth = HHAuth(mock_config, mock_logger)

            # Проверяем, что было сгенерировано предупреждение
            assert len(w) >= 1
            assert issubclass(w[-1].category, DeprecationWarning)

        # Мок для проверки неудачной авторизации
        with patch('src.auth.AuthHandler') as mock_auth_handler_class:
            mock_auth_handler = Mock()
            mock_auth_handler.perform_auth = AsyncMock(return_value=False)
            mock_auth_handler_class.return_value = mock_auth_handler

            # Выполнение
            result = await auth.perform_auth(mock_page)

            # Проверка
            assert result is False