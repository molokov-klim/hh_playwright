"""
Тесты для модуля конфигурации
"""
import os
import pytest
from unittest.mock import patch, MagicMock

# Импортируем тестируемый модуль (после его создания)
from src.config import get_config_from_env


class TestConfig:
    """Тесты для функций конфигурации"""

    def test_get_config_from_env_success(self):
        """Тест получения конфигурации из переменных окружения"""
        # Подготовка
        with patch.dict(os.environ, {
            'HH_LOGIN': 'test@example.com',
            'HH_PASSWORD': 'password123',
            'HEADLESS': 'true'
        }):
            # Выполнение
            config = get_config_from_env()

            # Проверка
            assert config.HH_LOGIN == 'test@example.com'
            assert config.HH_PASSWORD == 'password123'
            assert config.HEADLESS is True

    def test_get_config_from_env_missing_login_raises_error(self):
        """Тест выброса ошибки при отсутствии HH_LOGIN"""
        # Подготовка
        with patch.dict(os.environ, {}, clear=True):
            # Выполнение и проверка
            with pytest.raises(ValueError, match="HH_LOGIN environment variable is required"):
                get_config_from_env()

    def test_get_config_from_env_missing_password_raises_error(self):
        """Тест выброса ошибки при отсутствии HH_PASSWORD"""
        # Подготовка
        with patch.dict(os.environ, {'HH_LOGIN': 'test@example.com'}, clear=True):
            # Выполнение и проверка
            with pytest.raises(ValueError, match="HH_PASSWORD environment variable is required"):
                get_config_from_env()

    def test_headless_default_value(self):
        """Тест значения по умолчанию для HEADLESS"""
        # Подготовка
        with patch.dict(os.environ, {
            'HH_LOGIN': 'test@example.com',
            'HH_PASSWORD': 'password123'
            # HEADLESS не указан
        }):
            # Выполнение
            config = get_config_from_env()

            # Проверка
            assert config.HEADLESS is True  # По умолчанию должно быть True

    def test_headless_false_when_explicitly_set(self):
        """Тест установки HEADLESS в False при явном указании"""
        # Подготовка
        with patch.dict(os.environ, {
            'HH_LOGIN': 'test@example.com',
            'HH_PASSWORD': 'password123',
            'HEADLESS': 'false'
        }):
            # Выполнение
            config = get_config_from_env()

            # Проверка
            assert config.HEADLESS is False