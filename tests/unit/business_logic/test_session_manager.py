"""
Тесты для менеджера сессии
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch, MagicMock
from src.business_logic.session_manager import SessionManager
from src.config import Config


@pytest.mark.asyncio
class TestSessionManager:
    """Тесты для SessionManager"""
    
    @pytest.fixture
    def mock_config(self):
        """Мок конфигурации"""
        config = Mock(spec=Config)
        config.HEADLESS = True
        config.VIEWPORT_WIDTH = 1920
        config.VIEWPORT_HEIGHT = 1080
        config.USER_AGENT = "test-agent"
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
    def session_manager(self, mock_config, mock_logger):
        """Создание экземпляра SessionManager для тестов"""
        return SessionManager(mock_config, mock_logger)
    
    async def test_start_session(self, session_manager, mock_config):
        """Тест запуска сессии"""
        # Создаем моки для playwright компонентов
        mock_playwright = AsyncMock()
        mock_browser = AsyncMock()
        mock_context = AsyncMock()
        mock_page = AsyncMock()
        
        # Мокаем async_playwright
        with patch('src.business_logic.session_manager.async_playwright') as mock_async_playwright_func:
            mock_pw_instance = AsyncMock()
            mock_pw_instance.chromium.launch = AsyncMock(return_value=mock_browser)
            mock_async_playwright_func.return_value.start = AsyncMock(return_value=mock_pw_instance)
            
            with patch('src.business_logic.session_manager.get_browser_context_options') as mock_get_context_opts, \
                 patch('src.business_logic.session_manager.get_browser_options') as mock_get_browser_opts:
                
                mock_get_browser_opts.return_value = {"headless": True}
                mock_get_context_opts.return_value = {
                    "viewport": {"width": 1920, "height": 1080},
                    "user_agent": "test-agent"
                }
                
                # Мокаем методы браузера
                mock_browser.new_context = AsyncMock(return_value=mock_context)
                mock_context.new_page = AsyncMock(return_value=mock_page)
                
                await session_manager.start_session()
                
                # Проверяем, что все компоненты были установлены
                assert session_manager.playwright is not None
                assert session_manager.browser is not None
                assert session_manager.context is not None
                assert session_manager.page is not None
    
    async def test_end_session(self, session_manager):
        """Тест завершения сессии"""
        # Создаем моки для компонентов сессии
        session_manager.browser = Mock()
        session_manager.browser.close = AsyncMock()
        session_manager.playwright = Mock()
        session_manager.playwright.stop = AsyncMock()
        
        await session_manager.end_session()
        
        # Проверяем, что методы были вызваны
        session_manager.browser.close.assert_called_once()
        session_manager.playwright.stop.assert_called_once()
    
    async def test_get_page(self, session_manager):
        """Тест получения страницы"""
        mock_page = Mock()
        session_manager.page = mock_page
        
        page = session_manager.get_page()
        
        assert page == mock_page
    
    async def test_get_context(self, session_manager):
        """Тест получения контекста"""
        mock_context = Mock()
        session_manager.context = mock_context
        
        context = session_manager.get_context()
        
        assert context == mock_context
    
    async def test_get_browser(self, session_manager):
        """Тест получения браузера"""
        mock_browser = Mock()
        session_manager.browser = mock_browser
        
        browser = session_manager.get_browser()
        
        assert browser == mock_browser