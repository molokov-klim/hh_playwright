"""
Тесты для обработчика авторизации
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch
from src.business_logic.auth_handler import AuthHandler
from src.config import Config


@pytest.mark.asyncio
class TestAuthHandler:
    """Тесты для AuthHandler"""
    
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
    def auth_handler(self, mock_page, mock_config, mock_logger):
        """Создание экземпляра AuthHandler для тестов"""
        return AuthHandler(mock_page, mock_config, mock_logger)
    
    async def test_perform_auth_success(self, auth_handler, mock_page):
        """Тест успешной авторизации"""
        # Мок для успешной авторизации
        with patch.object(auth_handler.auth_page, 'navigate_to_login_page', return_value=True), \
             patch.object(auth_handler.auth_page, 'fill_login', return_value=True), \
             patch.object(auth_handler.auth_page, 'fill_password', return_value=True), \
             patch.object(auth_handler.auth_page, 'is_logged_in', return_value=True):
            
            result = await auth_handler.perform_auth()
            
            assert result is True
    
    async def test_perform_auth_failure_on_navigate(self, auth_handler):
        """Тест неудачной авторизации из-за ошибки перехода"""
        # Мок для неудачной авторизации
        with patch.object(auth_handler.auth_page, 'navigate_to_login_page', return_value=False):
            
            result = await auth_handler.perform_auth()
            
            assert result is False
    
    async def test_perform_auth_failure_on_login_fill(self, auth_handler):
        """Тест неудачной авторизации из-за ошибки заполнения логина"""
        # Мок для неудачной авторизации
        with patch.object(auth_handler.auth_page, 'navigate_to_login_page', return_value=True), \
             patch.object(auth_handler.auth_page, 'fill_login', return_value=False):
            
            result = await auth_handler.perform_auth()
            
            assert result is False
    
    async def test_perform_auth_failure_on_password_fill(self, auth_handler):
        """Тест неудачной авторизации из-за ошибки заполнения пароля"""
        # Мок для неудачной авторизации
        with patch.object(auth_handler.auth_page, 'navigate_to_login_page', return_value=True), \
             patch.object(auth_handler.auth_page, 'fill_login', return_value=True), \
             patch.object(auth_handler.auth_page, 'fill_password', return_value=False):
            
            result = await auth_handler.perform_auth()
            
            assert result is False
    
    async def test_perform_auth_failure_on_check_login(self, auth_handler):
        """Тест неудачной авторизации из-за ошибки проверки статуса входа"""
        # Мок для неудачной авторизации
        with patch.object(auth_handler.auth_page, 'navigate_to_login_page', return_value=True), \
             patch.object(auth_handler.auth_page, 'fill_login', return_value=True), \
             patch.object(auth_handler.auth_page, 'fill_password', return_value=True), \
             patch.object(auth_handler.auth_page, 'is_logged_in', return_value=False):
            
            result = await auth_handler.perform_auth()
            
            assert result is False