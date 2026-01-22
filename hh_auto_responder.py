"""
Основной скрипт для автоматизации откликов на hh.ru
"""
import asyncio
import sys
from typing import Optional

from playwright.async_api import async_playwright

from src.config import get_config_from_env, Config
from src.browser_config import get_browser_options, get_browser_context_options
from src.auth import HHAuth
from src.navigation import HHNavigation
from src.vacancy_processor import VacancyProcessor
from src.application_sender import ApplicationSender
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
    
    # Получение опций браузера и контекста
    browser_options = get_browser_options(config)
    context_options = get_browser_context_options(config)
    
    async with async_playwright() as p:
        try:
            # Запуск браузера
            logger.info("Запуск браузера")
            browser = await p.chromium.launch(**browser_options)
            
            # Создание контекста браузера
            context = await browser.new_context(**context_options)
            
            # Создание новой страницы
            page = await context.new_page()
            
            # Инициализация модулей
            auth = HHAuth(config, logger)
            navigation = HHNavigation(config, logger)
            processor = VacancyProcessor(config, logger)
            sender = ApplicationSender(config, logger)
            error_handler = ErrorHandler(config, logger)
            
            try:
                # Авторизация
                logger.info("Начало процесса авторизации")
                await auth.perform_auth(page)
                logger.info("Авторизация завершена успешно")
                
                # Навигация к разделу рекомендаций
                logger.info("Начало процесса навигации к рекомендуемым вакансиям")
                await navigation.navigate_to_my_resumes(page)
                
                # Выбор резюме (предполагаем, что используется первое резюме)
                await navigation.select_first_resume(page)
                
                # Переход к рекомендуемым вакансиям
                # Здесь нужно получить ID резюме, пока используем заглушку
                await navigation.go_to_recommended_vacancies(page, "resume123")
                
                # Ожидание загрузки вакансий
                await navigation.wait_for_vacancies_loaded(page)
                logger.info("Страница с рекомендуемыми вакансиями загружена")
                
                # Поиск вакансий
                vacancy_count = await processor.find_vacancy_cards(page)
                logger.info(f"Найдено {vacancy_count} вакансий")
                
                # Создание локаторов для вакансий
                vacancy_locators = []
                for i in range(vacancy_count):
                    # Создаем локатор для каждой вакансии
                    vacancy_locator = page.locator(f"[data-qa='vacancy']").nth(i)
                    vacancy_locators.append(vacancy_locator)
                
                # Фильтрация вакансий по возможности отклика
                applicable_vacancies = await processor.filter_applicable_vacancies(vacancy_locators)
                logger.info(f"Найдено {len(applicable_vacancies)} вакансий, на которые можно откликнуться")
                
                # Отправка откликов на подходящие вакансии
                for i, vacancy in enumerate(applicable_vacancies):
                    logger.info(f"Отправка отклика на вакансию {i+1} из {len(applicable_vacancies)}")
                    try:
                        result = await sender.apply_to_vacancy(vacancy)
                        logger.info(f"Результат отклика: {result}")
                    except Exception as e:
                        logger.error(f"Ошибка при отправке отклика на вакансию {i+1}: {e}")
                        
                        # Обработка ошибки
                        await error_handler.handle_general_error(page, e)
                
                logger.info("Процесс отправки откликов завершен")
                
            except Exception as e:
                logger.error(f"Ошибка в процессе работы скрипта: {e}")
                
                # Обработка ошибки
                await error_handler.handle_general_error(page, e)
                
        except Exception as e:
            logger.error(f"Критическая ошибка: {e}")
            
            # В случае критической ошибки создаем скриншот и завершаем работу
            if 'page' in locals():
                screenshot_path = error_handler.create_error_screenshot_path()
                await page.screenshot(path=screenshot_path)
            
            sys.exit(1)
        finally:
            # Закрытие браузера
            logger.info("Закрытие браузера")
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())