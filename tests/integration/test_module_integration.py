"""
Интеграционные тесты для проверки взаимодействия модулей
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch, MagicMock
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в путь Python
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.config import Config, get_config_from_env
from src.auth import HHAuth
from src.navigation import HHNavigation
from src.vacancy_processor import VacancyProcessor
from src.application_sender import ApplicationSender
from src.error_handler import ErrorHandler
from src.logger import setup_logger


class TestModuleIntegration:
    """Интеграционные тесты для проверки взаимодействия модулей"""

    @pytest.fixture
    def mock_config(self):
        """Мок конфигурации"""
        config = Mock(spec=Config)
        config.HH_LOGIN = "test@example.com"
        config.HH_PASSWORD = "password123"
        config.TIMEOUT = 30000
        config.HEADLESS = True
        return config

    @pytest.fixture
    def mock_page(self):
        """Мок страницы Playwright"""
        page = Mock()
        page.goto = AsyncMock()
        page.fill = AsyncMock()
        page.click = AsyncMock()
        page.wait_for_selector = AsyncMock()
        page.wait_for_url = AsyncMock()
        page.is_visible = AsyncMock(return_value=True)
        page.screenshot = AsyncMock()
        page.locator = Mock()
        return page

    def test_auth_and_navigation_integration(self, mock_config, mock_page):
        """Тест интеграции модулей авторизации и навигации"""
        # Подготовка
        logger = setup_logger("test_auth_nav_integration")
        
        auth = HHAuth(mock_config, logger)
        navigation = HHNavigation(mock_config, logger)
        
        # Мок для успешной авторизации
        with patch.object(auth, '_check_auth_success', return_value=True):
            # Выполнение - сначала авторизация, потом навигация
            import asyncio
            
            async def run_test():
                # Авторизация
                auth_result = await auth.perform_auth(mock_page)
                assert auth_result is True
                
                # Навигация после авторизации
                await navigation.navigate_to_my_resumes(mock_page)
                
                # Проверка, что были вызваны методы обоих модулей
                mock_page.goto.assert_called()
                mock_page.click.assert_called()
            
            asyncio.run(run_test())

    def test_navigation_and_vacancy_processor_integration(self, mock_config, mock_page):
        """Тест интеграции модулей навигации и обработки вакансий"""
        # Подготовка
        logger = setup_logger("test_nav_vac_proc_integration")
        
        navigation = HHNavigation(mock_config, logger)
        processor = VacancyProcessor(mock_config, logger)
        
        # Мок для вакансий
        vacancy_locator = Mock()
        vacancy_locator.count = AsyncMock(return_value=3)
        mock_page.locator.return_value = vacancy_locator
        
        # Мок для возвращения вакансий с возможностью отклика
        vacancy1 = Mock()
        vacancy1.locator.return_value.count = AsyncMock(return_value=1)
        
        async def run_test():
            # Навигация к рекомендуемым вакансиям
            await navigation.go_to_recommended_vacancies(mock_page, "resume123")
            
            # Поиск вакансий
            vacancy_count = await processor.find_vacancy_cards(mock_page)
            assert vacancy_count == 3
            
            # Проверка, что были вызваны методы обоих модулей
            mock_page.locator.assert_called()
            vacancy_locator.count.assert_called()
        
        import asyncio
        asyncio.run(run_test())

    def test_vacancy_processor_and_application_sender_integration(self, mock_config, mock_page):
        """Тест интеграции модулей обработки вакансий и отправки откликов"""
        # Подготовка
        logger = setup_logger("test_vac_proc_app_sender_integration")
        
        processor = VacancyProcessor(mock_config, logger)
        sender = ApplicationSender(mock_config, logger)
        
        # Мок для вакансии
        vacancy = Mock()
        vacancy.click = AsyncMock()
        vacancy.wait_for_selector = AsyncMock()
        vacancy.locator = Mock()
        
        # Мок для элементов вакансии
        title_element = Mock()
        title_element.inner_text = AsyncMock(return_value="Python Developer")
        id_element = Mock()
        id_element.get_attribute = AsyncMock(return_value="vac123")
        
        def mock_locator(selector):
            if selector == "[data-qa='vacancy-title']":
                return title_element
            elif selector == "[data-qa='vacancy-id']":
                return id_element
            else:
                apply_button_locator = Mock()
                apply_button_locator.count = AsyncMock(return_value=1)
                return apply_button_locator
        
        vacancy.locator.side_effect = mock_locator
        
        async def run_test():
            # Проверка, что вакансия доступна для отклика
            is_available = await processor.is_apply_button_available(vacancy)
            assert is_available is True
            
            # Отправка отклика на вакансию
            result = await sender.apply_to_vacancy(vacancy)
            assert result in ["Успешно", "Ошибка"]
            
            # Проверка, что были вызваны методы обоих модулей
            vacancy.click.assert_called()
            vacancy.wait_for_selector.assert_called()
        
        import asyncio
        asyncio.run(run_test())

    def test_error_handler_integration_with_other_modules(self, mock_config, mock_page):
        """Тест интеграции модуля обработки ошибок с другими модулями"""
        # Подготовка
        logger = setup_logger("test_error_handler_integration")
        
        error_handler = ErrorHandler(mock_config, logger)
        auth = HHAuth(mock_config, logger)
        
        async def run_test():
            # Тест обработки ошибки в контексте другого модуля
            try:
                await error_handler.handle_captcha_detection(mock_page, "Обнаружена капча")
            except Exception as e:
                assert "Обнаружена капча" in str(e)
            
            # Проверка, что скриншот был сделан
            mock_page.screenshot.assert_called()
        
        import asyncio
        asyncio.run(run_test())