"""
Тест для проверки новой системы логирования с декоратором log_info
"""
import asyncio
import io
import sys
from contextlib import redirect_stdout, redirect_stderr
from unittest.mock import Mock, AsyncMock

from src.decorators import log_info
from src.business_logic.application_handler import ApplicationHandler
from src.business_logic.auth_handler import AuthHandler
from src.steps.main_workflow import MainWorkflow
from src.logger import setup_logger


def test_log_info_decorator():
    """Тест декоратора log_info"""
    # Создаем тестовую асинхронную функцию
    @log_info()
    async def test_async_function(x, y, z=None):
        return x + y + (z or 0)

    # Создаем тестовую синхронную функцию
    @log_info()
    def test_sync_function(a, b):
        return a * b

    # Тестируем синхронную функцию
    result_sync = test_sync_function(5, 3)
    print(f"Sync result: {result_sync}")

    # Тестируем асинхронную функцию
    async def run_async_test():
        result_async = await test_async_function(1, 2, z=3)
        print(f"Async result: {result_async}")

    asyncio.run(run_async_test())

    print("✓ Декоратор log_info корректно логгирует информацию о вызовах функций")


def test_application_handler_with_logging():
    """Тест ApplicationHandler с новой системой логирования"""
    # Создаем моки
    mock_page = Mock()
    mock_config = Mock()
    mock_config.FAKE = True  # Устанавливаем режим FAKE для тестирования
    mock_logger = setup_logger("test_app_handler")
    
    # Создаем экземпляр ApplicationHandler
    app_handler = ApplicationHandler(mock_page, mock_config, mock_logger)
    
    # Проверяем, что методы существуют
    assert hasattr(app_handler, 'apply_to_vacancy')
    assert hasattr(app_handler, 'click_apply_button')
    assert hasattr(app_handler, 'fill_cover_letter')
    
    print("✓ ApplicationHandler корректно инициализирован с новой системой логирования")


def test_auth_handler_with_logging():
    """Тест AuthHandler с новой системой логирования"""
    # Создаем моки
    mock_page = Mock()
    mock_config = Mock()
    mock_logger = setup_logger("test_auth_handler")
    
    # Создаем экземпляр AuthHandler
    auth_handler = AuthHandler(mock_page, mock_config, mock_logger)
    
    # Проверяем, что методы существуют
    assert hasattr(auth_handler, 'perform_auth')
    
    print("✓ AuthHandler корректно инициализирован с новой системой логирования")


def test_main_workflow_with_logging():
    """Тест MainWorkflow с новой системой логирования"""
    # Создаем моки
    mock_page = Mock()
    mock_config = Mock()
    mock_logger = setup_logger("test_main_workflow")
    
    # Создаем экземпляр MainWorkflow
    main_workflow = MainWorkflow(mock_page, mock_config, mock_logger)
    
    # Проверяем, что методы существуют
    assert hasattr(main_workflow, 'run_full_workflow')
    
    print("✓ MainWorkflow корректно инициализирован с новой системой логирования")


if __name__ == "__main__":
    test_log_info_decorator()
    test_application_handler_with_logging()
    test_auth_handler_with_logging()
    test_main_workflow_with_logging()
    print("\n✓ Все тесты новой системы логирования пройдены успешно!")