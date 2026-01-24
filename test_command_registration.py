"""
Тест для проверки обработки команд от Telegram-бота
"""
import asyncio
from src.telegram_notifier import TelegramNotifier
from unittest.mock import Mock


def test_command_registration():
    """Тест регистрации команд бота"""
    # Создаем мок логгера
    mock_logger = Mock()
    
    # Создаем TelegramNotifier
    notifier = TelegramNotifier(
        bot_token="6209761567:AAG3QwLjuGqAoFVww4PqvmEcB-O-8qiXZFk",
        chat_id="1353223764",
        logger=mock_logger
    )
    
    # Проверяем, что обработчики команд зарегистрированы
    handlers = notifier.bot.message_handlers
    
    # Найдем обработчики для нужных команд
    start_handler = None
    status_handler = None
    
    for handler in handlers:
        if '/start' in str(handler['filters']):
            start_handler = handler
        elif '/status' in str(handler['filters']):
            status_handler = handler
    
    assert start_handler is not None, "Обработчик команды /start не найден"
    assert status_handler is not None, "Обработчик команды /status не найден"
    
    print("✓ Обработчики команд зарегистрированы корректно")
    print(f"✓ Команда /start зарегистрирована: {start_handler is not None}")
    print(f"✓ Команда /status зарегистрирована: {status_handler is not None}")


if __name__ == "__main__":
    test_command_registration()