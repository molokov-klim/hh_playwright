"""
Тест для проверки детального разбора ошибок с контекстом
"""
import asyncio
from src.telegram_notifier import TelegramNotifier
from unittest.mock import Mock


def test_detailed_error_formatting():
    """Тест форматирования детального отчета об ошибке"""
    # Создаем мок логгера
    mock_logger = Mock()
    
    # Создаем TelegramNotifier
    notifier = TelegramNotifier(
        bot_token="6209761567:AAG3QwLjuGqAoFVww4PqvmEcB-O-8qiXZFk",
        chat_id="1353223764",
        logger=mock_logger
    )
    
    # Создаем тестовую ошибку
    test_error = Exception("Тестовая ошибка при обработке вакансии")
    
    # Подготовим контекст ошибки
    context = {
        "stage": "processing_vacancy",
        "vacancy_id": "12345",
        "vacancy_title": "Python Developer",
        "url": "https://hh.ru/vacancy/12345",
        "resume_used": "main_resume",
        "timestamp": "2026-01-24 13:00:00"
    }
    
    # Форматируем отчет об ошибке
    formatted_report = notifier._format_error_report(test_error, context)
    
    print("Сформированный отчет об ошибке:")
    print(formatted_report)
    
    # Проверяем, что в отчете содержатся необходимые элементы
    assert "Тестовая ошибка при обработке вакансии" in formatted_report
    assert "processing_vacancy" in formatted_report
    assert "12345" in formatted_report
    assert "Python Developer" in formatted_report
    assert "https://hh.ru/vacancy/12345" in formatted_report
    assert "main_resume" in formatted_report
    
    print("\n✓ Все элементы контекста присутствуют в отчете об ошибке")


if __name__ == "__main__":
    test_detailed_error_formatting()