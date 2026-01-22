"""
Тесты для функций настройки браузера
"""
import pytest
from unittest.mock import Mock
from src.config import Config
from src.browser_config import get_browser_options, get_browser_context_options


class TestBrowserConfig:
    """Тесты для функций настройки браузера"""

    def test_get_browser_options_headless_true(self):
        """Тест получения опций браузера с headless=True"""
        # Подготовка
        config = Mock(spec=Config)
        config.HEADLESS = True
        
        # Выполнение
        options = get_browser_options(config)
        
        # Проверка
        assert options["headless"] is True

    def test_get_browser_options_headless_false(self):
        """Тест получения опций браузера с headless=False"""
        # Подготовка
        config = Mock(spec=Config)
        config.HEADLESS = False
        
        # Выполнение
        options = get_browser_options(config)
        
        # Проверка
        assert options["headless"] is False

    def test_get_browser_context_options_with_config_values(self):
        """Тест получения опций контекста браузера с значениями из конфига"""
        # Подготовка
        config = Mock(spec=Config)
        config.VIEWPORT_WIDTH = 1280
        config.VIEWPORT_HEIGHT = 720
        config.USER_AGENT = "Custom User Agent"
        config.TIMEOUT = 45000
        
        # Выполнение
        context_options = get_browser_context_options(config)
        
        # Проверка
        assert context_options["viewport"]["width"] == 1280
        assert context_options["viewport"]["height"] == 720
        assert context_options["user_agent"] == "Custom User Agent"
        assert context_options["timeout"] == 45000

    def test_get_browser_context_options_default_viewport(self):
        """Тест получения опций контекста браузера с вьюпортом по умолчанию"""
        # Подготовка
        config = Mock(spec=Config)
        config.VIEWPORT_WIDTH = 1920
        config.VIEWPORT_HEIGHT = 1080
        
        # Выполнение
        context_options = get_browser_context_options(config)
        
        # Проверка
        assert context_options["viewport"]["width"] == 1920
        assert context_options["viewport"]["height"] == 1080

    def test_get_browser_context_options_extra_options(self):
        """Тест наличия дополнительных опций контекста для обхода анти-бот защиты"""
        # Подготовка
        config = Mock(spec=Config)
        config.VIEWPORT_WIDTH = 1920
        config.VIEWPORT_HEIGHT = 1080
        config.USER_AGENT = "Test Agent"
        config.TIMEOUT = 30000
        
        # Выполнение
        context_options = get_browser_context_options(config)
        
        # Проверка
        # Проверяем наличие опций, которые помогают обойти анти-бот защиты
        assert "java_script_enabled" in context_options
        assert context_options["java_script_enabled"] is True
        assert "ignore_https_errors" in context_options
        assert context_options["ignore_https_errors"] is True