"""
Модуль для отправки уведомлений в Telegram с использованием pytelegrambotapi
"""
import telebot
from telebot.types import Message
from typing import Optional
import threading
import time
import logging
from datetime import datetime


class TelegramNotifier:
    """Класс для отправки уведомлений в Telegram с использованием pytelegrambotapi"""

    def __init__(self, bot_token: str, chat_id: str, logger=None):
        """
        Инициализация TelegramNotifier

        :param bot_token: Токен Telegram бота
        :param chat_id: ID чата для отправки сообщений
        :param logger: Объект логгера
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.logger = logger or logging.getLogger(__name__)
        self.bot = telebot.TeleBot(bot_token)
        
        # Запускаем polling в отдельном потоке
        self.polling_thread = None
        self.is_polling = False
        
        # Регистрируем обработчики команд
        self._register_handlers()

    def _register_handlers(self):
        """Регистрация обработчиков команд бота"""
        
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message: Message):
            welcome_text = (
                "🤖 <b>HH Auto Responder Bot</b>\n\n"
                "Привет! Я бот для уведомлений системы автоматического отклика на hh.ru.\n\n"
                "<b>Доступные команды:</b>\n"
                "/status - получить статус системы\n"
                "/last_errors - последние ошибки\n"
                "/stats - статистика за сегодня"
            )
            self.bot.reply_to(message, welcome_text, parse_mode='HTML')

        @self.bot.message_handler(commands=['status'])
        def send_status(message: Message):
            status_text = (
                "📊 <b>Статус системы</b>\n\n"
                "✅ Система запущена и работает\n"
                f"🕐 Время последнего запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                "🔄 Режим работы: активный"
            )
            self.bot.reply_to(message, status_text, parse_mode='HTML')

    def start_polling(self):
        """Запуск polling в отдельном потоке"""
        if not self.is_polling:
            self.is_polling = True
            self.polling_thread = threading.Thread(target=self._polling_worker)
            self.polling_thread.daemon = True
            self.polling_thread.start()
            
            if self.logger:
                self.logger.info("Telegram polling запущен в фоновом режиме")

    def _polling_worker(self):
        """Рабочий метод для polling в отдельном потоке"""
        while self.is_polling:
            try:
                self.bot.polling(non_stop=True, timeout=60)
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Ошибка в polling: {e}")
                time.sleep(10)  # Пауза перед повторной попыткой

    def stop_polling(self):
        """Остановка polling"""
        if self.is_polling:
            self.is_polling = False
            self.bot.stop_polling()
            
            if self.polling_thread:
                self.polling_thread.join(timeout=5)
                
            if self.logger:
                self.logger.info("Telegram polling остановлен")

    def send_message(self, message: str) -> bool:
        """
        Отправка сообщения в Telegram

        :param message: Текст сообщения
        :return: True, если сообщение отправлено успешно
        """
        if not self.bot_token or not self.chat_id:
            if self.logger:
                self.logger.warning("Telegram bot token или chat ID не заданы, сообщение не отправлено")
            return False

        try:
            self.bot.send_message(self.chat_id, message, parse_mode='HTML')
            
            if self.logger:
                self.logger.info(f"Сообщение в Telegram успешно отправлено: {message[:50]}...")
            return True

        except Exception as e:
            if self.logger:
                self.logger.error(f"Исключение при отправке сообщения в Telegram: {e}")
            return False

    def send_error_report(self, error: Exception, context: Optional[dict] = None, screenshot_path: Optional[str] = None) -> bool:
        """
        Отправка детального отчета об ошибке в Telegram

        :param error: Объект ошибки
        :param context: Контекст ошибки (информация о состоянии системы)
        :param screenshot_path: Путь к скриншоту (опционально)
        :return: True, если отчет об ошибке отправлен успешно
        """
        # Формируем детальный отчет об ошибке
        error_details = self._format_error_report(error, context)
        
        # Отправляем текстовое сообщение с деталями ошибки
        success = self.send_message(error_details)
        
        # Если есть скриншот, отправляем его
        if screenshot_path and success:
            try:
                with open(screenshot_path, 'rb') as photo:
                    self.bot.send_photo(self.chat_id, photo, caption="📸 Скриншот ошибки")
                    
                if self.logger:
                    self.logger.info(f"Скриншот ошибки отправлен: {screenshot_path}")
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Ошибка при отправке скриншота: {e}")
        
        return success

    def _format_error_report(self, error: Exception, context: Optional[dict] = None) -> str:
        """
        Форматирование детального отчета об ошибке

        :param error: Объект ошибки
        :param context: Контекст ошибки
        :return: Отформатированный текст отчета
        """
        # Получаем время ошибки
        error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Формируем основной текст отчета
        report_parts = [
            "🚨 <b>ОШИБКА В hh_auto_responder</b> 🚨",
            "",
            f"<b>Тип ошибки:</b> {type(error).__name__}",
            f"<b>Сообщение:</b> {str(error)}",
            f"<b>Время ошибки:</b> {error_time}",
        ]
        
        # Добавляем контекст, если он предоставлен
        if context:
            report_parts.append("")
            report_parts.append("<b>Контекст ошибки:</b>")
            
            for key, value in context.items():
                report_parts.append(f"• <code>{key}</code>: {value}")
        
        # Добавляем информацию о системе
        report_parts.extend([
            "",
            "<b>Системная информация:</b>",
            f"• PID процесса: {__import__('os').getpid()}",
            f"• Версия Python: {__import__('sys').version}",
            f"• Версия Playwright: {__import__('playwright').__version__ if hasattr(__import__('playwright'), '__version__') else 'unknown'}",
        ])
        
        return "\n".join(report_parts)

    def send_startup_notification(self) -> bool:
        """
        Отправка уведомления о запуске скрипта

        :return: True, если уведомление отправлено успешно
        """
        startup_message = f"""
✅ <b>hh_auto_responder запущен</b> ✅

<b>Время запуска:</b> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
<b>Режим работы:</b> {"Тестовый (FAKE)" if __import__('os').environ.get('FAKE', '').lower() == 'true' else "Рабочий"}
        """

        return self.send_message(startup_message)

    def send_shutdown_notification(self, success_count: int = 0, error_count: int = 0) -> bool:
        """
        Отправка уведомления о завершении работы скрипта

        :param success_count: Количество успешных откликов
        :param error_count: Количество ошибок
        :return: True, если уведомление отправлено успешно
        """
        shutdown_message = f"""
⏹️ <b>hh_auto_responder завершен</b> ⏹️

<b>Время завершения:</b> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
<b>Успешных откликов:</b> {success_count}
<b>Ошибок:</b> {error_count}

{'🎉 Работа завершена успешно!' if error_count == 0 else '⚠️ Обнаружены ошибки во время работы.'}
        """

        return self.send_message(shutdown_message)

    def send_detailed_stats(self, stats_data: dict) -> bool:
        """
        Отправка детальной статистики работы

        :param stats_data: Словарь с данными статистики
        :return: True, если статистика отправлена успешно
        """
        stats_message = [
            "📈 <b>Детальная статистика работы</b> 📈",
            ""
        ]
        
        for key, value in stats_data.items():
            stats_message.append(f"<b>{key}:</b> {value}")
        
        return self.send_message("\n".join(stats_message))