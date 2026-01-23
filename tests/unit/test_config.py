"""
Тесты для модуля конфигурации
"""
import os
import pytest
from unittest.mock import patch, MagicMock

# Импортируем тестируемый модуль (после его создания)
from src.config import get_config_from_env, Config


class TestConfig:
    """Тесты для функций конфигурации"""

    def test_get_config_from_env_success(self):
        """Тест получения конфигурации из переменных окружения"""
        # Подготовка - мокируем load_dotenv_if_exists, чтобы она не загружала .env файл
        with patch('src.config.load_dotenv_if_exists'), \
             patch.dict(os.environ, {
                'HH_LOGIN': 'test@example.com',
                'HH_PASSWORD': 'password123',
                'HEADLESS': 'true'
            }, clear=True):
            # Выполнение
            config = get_config_from_env()

            # Проверка
            assert config.HH_LOGIN == 'test@example.com'
            assert config.HH_PASSWORD == 'password123'
            assert config.HEADLESS is True

    def test_get_config_from_env_missing_login_raises_error(self):
        """Тест выброса ошибки при отсутствии HH_LOGIN"""
        # Подготовка - мокируем load_dotenv_if_exists и используем пустой словарь для изоляции
        with patch('src.config.load_dotenv_if_exists'), \
             patch.dict(os.environ, {}, clear=True):
            # Выполнение и проверка
            with pytest.raises(ValueError, match="HH_LOGIN environment variable is required"):
                get_config_from_env()

    def test_get_config_from_env_missing_password_raises_error(self):
        """Тест выброса ошибки при отсутствии HH_PASSWORD"""
        # Подготовка - мокируем load_dotenv_if_exists, устанавливаем только HH_LOGIN
        with patch('src.config.load_dotenv_if_exists'), \
             patch.dict(os.environ, {'HH_LOGIN': 'test@example.com'}, clear=True):
            # Выполнение и проверка
            with pytest.raises(ValueError, match="HH_PASSWORD environment variable is required"):
                get_config_from_env()

    def test_headless_default_value(self):
        """Тест значения по умолчанию для HEADLESS"""
        # Подготовка - мокируем load_dotenv_if_exists, устанавливаем только необходимые переменные
        with patch('src.config.load_dotenv_if_exists'), \
             patch.dict(os.environ, {
                'HH_LOGIN': 'test@example.com',
                'HH_PASSWORD': 'password123'
                # HEADLESS не указан, должно использоваться значение по умолчанию
            }, clear=True):
            # Выполнение
            config = get_config_from_env()

            # Проверка
            assert config.HEADLESS is True  # По умолчанию должно быть True

    def test_headless_false_when_explicitly_set(self):
        """Тест установки HEADLESS в False при явном указании"""
        # Подготовка - мокируем load_dotenv_if_exists
        with patch('src.config.load_dotenv_if_exists'), \
             patch.dict(os.environ, {
                'HH_LOGIN': 'test@example.com',
                'HH_PASSWORD': 'password123',
                'HEADLESS': 'false'
            }, clear=True):
            # Выполнение
            config = get_config_from_env()

            # Проверка
            assert config.HEADLESS is False