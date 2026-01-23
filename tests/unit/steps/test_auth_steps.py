"""
Тесты для шагов авторизации
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch
from src.steps.auth_steps import AuthSteps
from src.config import Config


@pytest.mark.asyncio
class TestAuthSteps:
    """Тесты для AuthSteps"""
    
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
    def auth_steps(self, mock_page, mock_config, mock_logger):
        """Создание экземпляра AuthSteps для тестов"""
        return AuthSteps(mock_page, mock_config, mock_logger)
    
    async def test_login_to_hh_success(self, auth_steps):
        """Тест успешной авторизации через шаги"""
        # Мок для успешной авторизации
        with patch.object(auth_steps.auth_handler, 'perform_auth', return_value=True):
            
            result = await auth_steps.login_to_hh()
            
            assert result is True
    
    async def test_login_to_hh_failure(self, auth_steps):
        """Тест неудачной авторизации через шаги"""
        # Мок для неудачной авторизации
        with patch.object(auth_steps.auth_handler, 'perform_auth', return_value=False):
            
            result = await auth_steps.login_to_hh()
            
            assert result is False