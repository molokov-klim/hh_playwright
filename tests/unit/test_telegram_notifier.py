"""
Тесты для нового модуля TelegramNotifier
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Добавляем путь к src для импорта модулей
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.telegram_notifier import TelegramNotifier


@pytest.fixture
def mock_logger():
    """Мок логгера"""
    logger = Mock()
    logger.info = Mock()
    logger.error = Mock()
    logger.debug = Mock()
    return logger


def test_telegram_notifier_initialization():
    """Тест инициализации TelegramNotifier"""
    bot_token = "6209761567:AAG3QwLjuGqAoFVww4PqvmEcB-O-8qiXZFk"
    chat_id = "1353223764"
    
    notifier = TelegramNotifier(bot_token, chat_id)
    
    assert notifier.bot_token == bot_token
    assert notifier.chat_id == chat_id
    assert notifier.bot is not None


@patch('src.telegram_notifier.telebot.TeleBot')
def test_send_message_success(mock_telebot_class, mock_logger):
    """Тест успешной отправки сообщения"""
    bot_token = "6209761567:AAG3QwLjuGqAoFVww4PqvmEcB-O-8qiXZFk"
    chat_id = "1353223764"
    
    # Мокаем экземпляр бота
    mock_bot_instance = Mock()
    mock_telebot_class.return_value = mock_bot_instance
    
    notifier = TelegramNotifier(bot_token, chat_id, mock_logger)
    
    # Мокаем метод отправки сообщения
    mock_bot_instance.send_message.return_value = True
    
    message = "Тестовое сообщение"
    result = notifier.send_message(message)
    
    assert result is True
    mock_bot_instance.send_message.assert_called_once_with(
        chat_id, message, parse_mode='HTML'
    )


@patch('src.telegram_notifier.telebot.TeleBot')
def test_send_error_report(mock_telebot_class, mock_logger):
    """Тест отправки отчета об ошибке"""
    bot_token = "6209761567:AAG3QwLjuGqAoFVww4PqvmEcB-O-8qiXZFk"
    chat_id = "1353223764"
    
    # Мокаем экземпляр бота
    mock_bot_instance = Mock()
    mock_telebot_class.return_value = mock_bot_instance
    
    notifier = TelegramNotifier(bot_token, chat_id, mock_logger)
    
    # Мокаем метод отправки сообщения
    mock_bot_instance.send_message.return_value = True
    
    error = Exception("Тестовая ошибка")
    context = {
        "stage": "test_stage",
        "url": "https://example.com",
        "error_type": "test_error"
    }
    
    result = notifier.send_error_report(error, context)
    
    assert result is True
    mock_bot_instance.send_message.assert_called_once()
    
    # Проверяем, что в вызове содержится информация об ошибке
    call_args = mock_bot_instance.send_message.call_args
    sent_message = call_args[0][1]  # Второй аргумент - это сообщение
    
    assert "Тестовая ошибка" in sent_message
    assert "test_stage" in sent_message
    assert "https://example.com" in sent_message
    assert "test_error" in sent_message


@patch('src.telegram_notifier.telebot.TeleBot')
def test_send_startup_notification(mock_telebot_class, mock_logger):
    """Тест отправки уведомления о запуске"""
    bot_token = "6209761567:AAG3QwLjuGqAoFVww4PqvmEcB-O-8qiXZFk"
    chat_id = "1353223764"
    
    # Мокаем экземпляр бота
    mock_bot_instance = Mock()
    mock_telebot_class.return_value = mock_bot_instance
    
    notifier = TelegramNotifier(bot_token, chat_id, mock_logger)
    
    # Мокаем метод отправки сообщения
    mock_bot_instance.send_message.return_value = True
    
    result = notifier.send_startup_notification()
    
    assert result is True
    mock_bot_instance.send_message.assert_called_once()
    
    # Проверяем, что в вызове содержится упоминание запуска
    call_args = mock_bot_instance.send_message.call_args
    sent_message = call_args[0][1]  # Второй аргумент - это сообщение
    
    assert "запущен" in sent_message


@patch('src.telegram_notifier.telebot.TeleBot')
def test_send_shutdown_notification(mock_telebot_class, mock_logger):
    """Тест отправки уведомления о завершении"""
    bot_token = "6209761567:AAG3QwLjuGqAoFVww4PqvmEcB-O-8qiXZFk"
    chat_id = "1353223764"
    
    # Мокаем экземпляр бота
    mock_bot_instance = Mock()
    mock_telebot_class.return_value = mock_bot_instance
    
    notifier = TelegramNotifier(bot_token, chat_id, mock_logger)
    
    # Мокаем метод отправки сообщения
    mock_bot_instance.send_message.return_value = True
    
    result = notifier.send_shutdown_notification(success_count=5, error_count=1)
    
    assert result is True
    mock_bot_instance.send_message.assert_called_once()
    
    # Проверяем, что в вызове содержится упоминание завершения
    call_args = mock_bot_instance.send_message.call_args
    sent_message = call_args[0][1]  # Второй аргумент - это сообщение
    
    assert "завершен" in sent_message
    assert "5" in sent_message  # количество успешных откликов
    assert "1" in sent_message  # количество ошибок