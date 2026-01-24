"""
Тестовый скрипт для проверки новой функциональности Telegram-уведомлений
"""
import asyncio
import os
from src.config import get_config_from_env, Config
from src.error_handler import ErrorHandler
from src.logger import setup_logger


async def test_telegram_notifications():
    """Тестирование новой функциональности Telegram-уведомлений"""
    logger = setup_logger("test_telegram_notifications")
    
    # Создаем конфигурацию с тестовыми значениями
    os.environ['HH_LOGIN'] = 'test@example.com'
    os.environ['HH_PASSWORD'] = 'password123'
    os.environ['TELEGRAM_BOT_TOKEN'] = '6209761567:AAG3QwLjuGqAoFVww4PqvmEcB-O-8qiXZFk'
    os.environ['TELEGRAM_CHAT_ID'] = '1353223764'
    
    config = get_config_from_env()
    
    # Создаем обработчик ошибок
    error_handler = ErrorHandler(config, logger)
    
    print("Тестируем отправку уведомлений в Telegram...")
    
    # Отправляем уведомление о запуске
    await error_handler.send_startup_notification()
    print("✓ Уведомление о запуске отправлено")
    
    # Имитируем ошибку для тестирования отправки отчета об ошибке
    try:
        # Создаем фейковую страницу для тестирования
        class FakePage:
            url = "https://hh.ru/some-page"
            
            async def screenshot(self, path: str):
                print(f"Скриншот сохранен в {path}")
        
        fake_page = FakePage()
        
        # Вызываем обработку ошибки
        await error_handler.handle_general_error(fake_page, Exception("Тестовая ошибка"))
        
    except Exception as e:
        print(f"✓ Обработка ошибки выполнена: {e}")
    
    # Отправляем уведомление о завершении
    await error_handler.send_shutdown_notification(success_count=0, error_count=1)
    print("✓ Уведомление о завершении отправлено")
    
    # Очищаем ресурсы
    error_handler.cleanup()
    print("✓ Ресурсы очищены")


if __name__ == "__main__":
    asyncio.run(test_telegram_notifications())