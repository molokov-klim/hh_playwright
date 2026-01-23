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
        headless = True

        # Выполнение
        options = get_browser_options(headless)

        # Проверка
        assert options["headless"] is True

    def test_get_browser_options_headless_false(self):
        """Тест получения опций браузера с headless=False"""
        # Подготовка
        headless = False

        # Выполнение
        options = get_browser_options(headless)

        # Проверка
        assert options["headless"] is False

    def test_get_browser_context_options_with_config_values(self):
        """Тест получения опций контекста браузера с значениями из конфига"""
        # Подготовка
        viewport_width = 1280
        viewport_height = 720
        user_agent = "Custom User Agent"

        # Выполнение
        context_options = get_browser_context_options(viewport_width, viewport_height, user_agent)

        # Проверка
        assert context_options["viewport"]["width"] == 1280
        assert context_options["viewport"]["height"] == 720
        assert context_options["user_agent"] == "Custom User Agent"

    def test_get_browser_context_options_default_viewport(self):
        """Тест получения опций контекста браузера с вьюпортом по умолчанию"""
        # Подготовка
        viewport_width = 1920
        viewport_height = 1080
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

        # Выполнение
        context_options = get_browser_context_options(viewport_width, viewport_height, user_agent)

        # Проверка
        assert context_options["viewport"]["width"] == 1920
        assert context_options["viewport"]["height"] == 1080

    def test_get_browser_context_options_extra_options(self):
        """Тест наличия дополнительных опций контекста для обхода анти-бот защиты"""
        # Подготовка
        viewport_width = 1920
        viewport_height = 1080
        user_agent = "Test Agent"

        # Выполнение
        context_options = get_browser_context_options(viewport_width, viewport_height, user_agent)

        # Проверка
        # Проверяем наличие опций, которые помогают обойти анти-бот защиты
        assert "java_script_enabled" in context_options
        assert context_options["java_script_enabled"] is True
        assert "ignore_https_errors" in context_options
        assert context_options["ignore_https_errors"] is True