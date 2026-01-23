"""
Основной скрипт для автоматизации откликов на hh.ru
"""
import asyncio
import sys

from playwright.async_api import async_playwright

from src.config import get_config_from_env, Config
from src.browser_config import get_browser_options, get_browser_context_options
from src.business_logic.session_manager import SessionManager
from src.steps.main_workflow import MainWorkflow
from src.error_handler import ErrorHandler
from src.logger import setup_logger


async def main():
    """Основная функция для запуска скрипта"""
    logger = setup_logger("hh_auto_responder")

    try:
        # Загрузка конфигурации
        config = get_config_from_env()
        logger.info("Конфигурация успешно загружена")
    except ValueError as e:
        logger.error(f"Ошибка загрузки конфигурации: {e}")
        sys.exit(1)

    # Создание менеджера сессии
    session_manager = SessionManager(config, logger)

    try:
        # Запуск сессии
        await session_manager.start_session()
        logger.info("Сессия браузера запущена")

        # Получение страницы
        page = session_manager.get_page()

        # Инициализация обработчика ошибок
        error_handler = ErrorHandler(config, logger)

        # Инициализация основного сценария
        main_workflow = MainWorkflow(page, config, logger)

        try:
            # Запуск основного сценария
            logger.info("Начало выполнения основного сценария")
            success = await main_workflow.run_full_workflow()
            
            if success:
                logger.info("Основной сценарий успешно завершен")
            else:
                logger.error("Ошибка при выполнении основного сценария")

        except Exception as e:
            logger.error(f"Ошибка в процессе работы скрипта: {e}")

            # Обработка ошибки
            await error_handler.handle_general_error(page, e)

    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")

        # В случае критической ошибки создаем скриншот и завершаем работу
        page = session_manager.get_page() if hasattr(session_manager, 'get_page') else None
        if page:
            screenshot_path = error_handler.create_error_screenshot_path()
            await page.screenshot(path=screenshot_path)

        sys.exit(1)
    finally:
        # Завершение сессии
        await session_manager.end_session()
        logger.info("Сессия браузера завершена")


if __name__ == "__main__":
    asyncio.run(main())