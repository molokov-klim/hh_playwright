"""
Простой тест для проверки новой архитектуры
"""
import asyncio
import pytest
from unittest.mock import Mock, AsyncMock, patch


@pytest.mark.asyncio
async def test_new_architecture_basic_functionality():
    """Тест основной функциональности новой архитектуры"""
    # Импорты новых модулей
    from src.pages.base_page import BasePage
    from src.pages.auth_page import AuthPage
    from src.business_logic.auth_handler import AuthHandler
    from src.steps.auth_steps import AuthSteps
    from src.business_logic.session_manager import SessionManager
    from src.steps.main_workflow import MainWorkflow
    from src.config import Config
    
    # Создаем моки
    mock_page = Mock()
    mock_page.wait_for_selector = AsyncMock(return_value=True)
    mock_page.click = AsyncMock()
    mock_page.fill = AsyncMock()
    mock_page.is_visible = AsyncMock(return_value=True)
    mock_page.locator = Mock()
    mock_page.goto = AsyncMock()
    mock_page.press = AsyncMock()
    
    mock_config = Mock(spec=Config)
    mock_config.HH_LOGIN = "test@example.com"
    mock_config.HH_PASSWORD = "password123"
    mock_config.TIMEOUT = 30000
    mock_config.HEADLESS = True
    mock_config.VIEWPORT_WIDTH = 1920
    mock_config.VIEWPORT_HEIGHT = 1080
    mock_config.USER_AGENT = "test-agent"
    
    mock_logger = Mock()
    mock_logger.info = Mock()
    mock_logger.error = Mock()
    mock_logger.debug = Mock()
    
    # Тестируем Page Object
    auth_page = AuthPage(mock_page, mock_config, mock_logger)
    assert auth_page is not None
    
    # Тестируем Business Logic
    auth_handler = AuthHandler(mock_page, mock_config, mock_logger)
    assert auth_handler is not None
    
    # Тестируем Steps
    auth_steps = AuthSteps(mock_page, mock_config, mock_logger)
    assert auth_steps is not None
    
    # Тестируем Main Workflow
    main_workflow = MainWorkflow(mock_page, mock_config, mock_logger)
    assert main_workflow is not None
    
    # Тестируем Session Manager
    session_manager = SessionManager(mock_config, mock_logger)
    assert session_manager is not None
    
    print("Все компоненты новой архитектуры успешно инициализированы!")


if __name__ == "__main__":
    asyncio.run(test_new_architecture_basic_functionality())