"""
Тесты для Page Object авторизации
"""
import pytest
from unittest.mock import AsyncMock, Mock
from src.pages.auth_page import AuthPage
from src.config import Config


@pytest.mark.asyncio
class TestAuthPage:
    """Тесты для AuthPage"""
    
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
        page.press = AsyncMock()
        return page
    
    @pytest.fixture
    def mock_config(self):
        """Мок конфигурации"""
        config = Mock(spec=Config)
        config.HH_LOGIN = "test@example.com"
        config.HH_PASSWORD = "password123"
        return config
    
    @pytest.fixture
    def mock_logger(self):
        """Мок логгера"""
        logger = Mock()
        logger.info = Mock()
        logger.error = Mock()
        logger.debug = Mock()
        return logger
    
    @pytest.fixture
    def auth_page(self, mock_page, mock_config, mock_logger):
        """Создание экземпляра AuthPage для тестов"""
        return AuthPage(mock_page, mock_config, mock_logger)
    
    async def test_navigate_to_login_page_success(self, auth_page, mock_page):
        """Тест успешного перехода на страницу авторизации"""
        result = await auth_page.navigate_to_login_page()
        
        assert result is True
        mock_page.goto.assert_called_once_with("https://hh.ru")
    
    async def test_fill_login_success(self, auth_page, mock_page, mock_config):
        """Тест успешного заполнения логина"""
        result = await auth_page.fill_login(mock_config.HH_LOGIN)
        
        assert result is True
        mock_page.fill.assert_called()
    
    async def test_fill_password_success(self, auth_page, mock_page, mock_config):
        """Тест успешного заполнения пароля"""
        result = await auth_page.fill_password(mock_config.HH_PASSWORD)
        
        assert result is True
        mock_page.fill.assert_called()
    
    async def test_is_logged_in_success(self, auth_page, mock_page):
        """Тест проверки статуса авторизации"""
        # Мок для успешной авторизации
        mock_page.wait_for_selector = AsyncMock(return_value=True)
        mock_page.is_visible = AsyncMock(return_value=True)
        
        result = await auth_page.is_logged_in()
        
        assert result is True