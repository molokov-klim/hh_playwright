"""
Моки для компонентов приложения
"""
from unittest.mock import Mock, MagicMock, AsyncMock
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в путь Python
sys.path.insert(0, str(Path(__file__).parent.parent))

def create_mock_config():
    """Создание мока конфигурации приложения"""
    config = Mock()
    config.HH_LOGIN = "test@example.com"
    config.HH_PASSWORD = "secure_password"
    config.HEADLESS = True
    config.VIEWPORT_WIDTH = 1920
    config.VIEWPORT_HEIGHT = 1080
    config.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    config.TIMEOUT = 30000
    return config


def create_mock_browser_instance():
    """Создание мока экземпляра браузера"""
    browser = Mock()
    browser.context = Mock()
    browser.page = Mock()
    
    # Мок для асинхронного контекста
    browser.__aenter__ = AsyncMock(return_value=browser)
    browser.__aexit__ = AsyncMock(return_value=None)
    
    return browser


def create_mock_logger():
    """Создание мока логгера"""
    logger = Mock()
    logger.info = Mock()
    logger.warning = Mock()
    logger.error = Mock()
    logger.debug = Mock()
    return logger


def create_mock_hh_service():
    """Создание мока сервиса для работы с hh.ru"""
    service = Mock()
    service.browser = create_mock_browser_instance()
    service.logger = create_mock_logger()
    service.config = create_mock_config()
    
    # Моки для основных методов
    service.login = Mock()
    service.navigate_to_my_resumes = Mock()
    service.select_resume = Mock()
    service.go_to_recommended_vacancies = Mock()
    service.process_vacancies = Mock()
    service.apply_to_vacancy = Mock()
    
    return service