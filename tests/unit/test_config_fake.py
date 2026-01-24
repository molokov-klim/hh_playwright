"""
Тесты для проверки новой переменной FAKE в конфигурации
"""
import os
import pytest
from src.config import get_config_from_env


def test_fake_variable_defaults_to_false():
    """Тест, что переменная FAKE по умолчанию равна False"""
    # Сохраняем оригинальные переменные окружения
    original_environ = dict(os.environ)
    
    # Очищаем все переменные окружения
    os.environ.clear()
    
    try:
        # Задаем только обязательные переменные
        os.environ['HH_LOGIN'] = 'test@example.com'
        os.environ['HH_PASSWORD'] = 'password123'
        
        # Получаем конфигурацию
        config = get_config_from_env()
        
        # Проверяем, что FAKE по умолчанию равен False
        assert config.FAKE is False
    finally:
        # Восстанавливаем оригинальные переменные окружения
        os.environ.clear()
        os.environ.update(original_environ)


def test_fake_variable_true_when_set():
    """Тест, что переменная FAKE равна True, когда установлена в true"""
    # Сохраняем оригинальные переменные окружения
    original_environ = dict(os.environ)
    
    # Очищаем все переменные окружения
    os.environ.clear()
    
    try:
        # Задаем переменные, включая FAKE
        os.environ['HH_LOGIN'] = 'test@example.com'
        os.environ['HH_PASSWORD'] = 'password123'
        os.environ['FAKE'] = 'true'
        
        # Получаем конфигурацию
        config = get_config_from_env()
        
        # Проверяем, что FAKE равен True
        assert config.FAKE is True
    finally:
        # Восстанавливаем оригинальные переменные окружения
        os.environ.clear()
        os.environ.update(original_environ)


def test_fake_variable_false_when_explicitly_set():
    """Тест, что переменная FAKE равна False, когда явно установлена в false"""
    # Сохраняем оригинальные переменные окружения
    original_environ = dict(os.environ)
    
    # Очищаем все переменные окружения
    os.environ.clear()
    
    try:
        # Задаем переменные, включая FAKE
        os.environ['HH_LOGIN'] = 'test@example.com'
        os.environ['HH_PASSWORD'] = 'password123'
        os.environ['FAKE'] = 'false'
        
        # Получаем конфигурацию
        config = get_config_from_env()
        
        # Проверяем, что FAKE равен False
        assert config.FAKE is False
    finally:
        # Восстанавливаем оригинальные переменные окружения
        os.environ.clear()
        os.environ.update(original_environ)


def test_fake_variable_various_true_values():
    """Тест, что переменная FAKE распознает различные значения, означающие True"""
    # Сохраняем оригинальные переменные окружения
    original_environ = dict(os.environ)
    
    for fake_value in ['true', 'True', '1', 'yes', 'on']:
        # Очищаем все переменные окружения
        os.environ.clear()
        
        try:
            # Задаем переменные, включая FAKE
            os.environ['HH_LOGIN'] = 'test@example.com'
            os.environ['HH_PASSWORD'] = 'password123'
            os.environ['FAKE'] = fake_value
            
            # Получаем конфигурацию
            config = get_config_from_env()
            
            # Проверяем, что FAKE равен True
            assert config.FAKE is True, f"FAKE should be True when set to '{fake_value}'"
        finally:
            # Восстанавливаем оригинальные переменные окружения
            os.environ.clear()
            os.environ.update(original_environ)


def test_fake_variable_various_false_values():
    """Тест, что переменная FAKE распознает различные значения, означающие False"""
    # Сохраняем оригинальные переменные окружения
    original_environ = dict(os.environ)
    
    for fake_value in ['false', 'False', '0', 'no', 'off', '']:
        # Очищаем все переменные окружения
        os.environ.clear()
        
        try:
            # Задаем переменные, включая FAKE
            os.environ['HH_LOGIN'] = 'test@example.com'
            os.environ['HH_PASSWORD'] = 'password123'
            os.environ['FAKE'] = fake_value
            
            # Получаем конфигурацию
            config = get_config_from_env()
            
            # Проверяем, что FAKE равен False
            assert config.FAKE is False, f"FAKE should be False when set to '{fake_value}'"
        finally:
            # Восстанавливаем оригинальные переменные окружения
            os.environ.clear()
            os.environ.update(original_environ)