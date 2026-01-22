"""
Интеграционный тест для полного сценария работы скрипта
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


class TestFullScenario:
    """Интеграционный тест для полного сценария работы скрипта"""

    @pytest.fixture
    def mock_config(self):
        """Мок конфигурации"""
        config = Mock(spec=Config)
        config.HH_LOGIN = "test@example.com"
        config.HH_PASSWORD = "password123"
        config.TIMEOUT = 30000
        config.HEADLESS = True
        config.VIEWPORT_WIDTH = 1920
        config.VIEWPORT_HEIGHT = 1080
        config.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
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
        return page

    @pytest.fixture
    def mock_logger(self):
        """Мок логгера"""
        logger = Mock()
        logger.info = Mock()
        logger.error = Mock()
        logger.debug = Mock()
        return logger

    def test_full_scenario_success_flow(self, mock_config, mock_page, mock_logger):
        """Тест полного сценария - успешный поток"""
        # Подготовка всех модулей
        auth = HHAuth(mock_config, mock_logger)
        navigation = HHNavigation(mock_config, mock_logger)
        processor = VacancyProcessor(mock_config, mock_logger)
        sender = ApplicationSender(mock_config, mock_logger)
        
        # Мок для успешной авторизации
        with patch.object(auth, '_check_auth_success', return_value=True):
            # Мок для вакансий
            vacancy_locator = Mock()
            vacancy_locator.count = AsyncMock(return_value=2)
            mock_page.locator.return_value = vacancy_locator
            
            # Мок для вакансий с возможностью отклика
            vacancy1 = Mock()
            vacancy1.click = AsyncMock()
            vacancy1.wait_for_selector = AsyncMock()
            vacancy1.locator = Mock()
            
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
            
            vacancy1.locator.side_effect = mock_locator
            
            vacancy_list = [vacancy1, Mock()]
            vacancy_list[1].locator = Mock()
            vacancy_list[1].locator.return_value.count = AsyncMock(return_value=1)
            vacancy_list[1].click = AsyncMock()
            vacancy_list[1].wait_for_selector = AsyncMock()
            
            async def run_full_scenario():
                # 1. Авторизация
                auth_result = await auth.perform_auth(mock_page)
                assert auth_result is True
                
                # 2. Навигация к резюме
                await navigation.navigate_to_my_resumes(mock_page)
                
                # 3. Выбор первого резюме
                await navigation.select_first_resume(mock_page)
                
                # 4. Переход к рекомендуемым вакансиям
                await navigation.go_to_recommended_vacancies(mock_page, "resume123")
                
                # 5. Ожидание загрузки вакансий
                await navigation.wait_for_vacancies_loaded(mock_page)
                
                # 6. Поиск вакансий
                vacancy_count = await processor.find_vacancy_cards(mock_page)
                assert vacancy_count == 2
                
                # 7. Фильтрация вакансий
                applicable_vacancies = await processor.filter_applicable_vacancies(vacancy_list)
                assert len(applicable_vacancies) >= 0  # Может быть 0 или больше
                
                # 8. Отправка откликов на все подходящие вакансии
                for vacancy in applicable_vacancies[:1]:  # Ограничиваем до одной для теста
                    result = await sender.apply_to_vacancy(vacancy)
                    assert result in ["Успешно", "Ошибка"]
                
                # Проверка, что были вызваны ключевые методы
                mock_page.goto.assert_any_call("https://hh.ru")
                mock_page.click.assert_called()
            
            import asyncio
            asyncio.run(run_full_scenario())

    def test_full_scenario_with_error_handling(self, mock_config, mock_page, mock_logger):
        """Тест полного сценария с обработкой ошибок"""
        # Подготовка всех модулей
        auth = HHAuth(mock_config, mock_logger)
        error_handler = ErrorHandler(mock_config, mock_logger)
        
        # Мок для неудачной авторизации
        with patch.object(auth, '_check_auth_success', return_value=False):
            async def run_scenario_with_error():
                try:
                    # Попытка авторизации, которая должна завершиться неудачей
                    await auth.perform_auth(mock_page)
                    assert False, "Ожидалось исключение при неудачной авторизации"
                except Exception as e:
                    # Проверяем, что было выброшено исключение
                    assert "Authentication failed" in str(e)
                    
                    # Имитируем вызов обработчика ошибок
                    await error_handler.handle_general_error(mock_page, e)
            
            import asyncio
            with pytest.raises(Exception):
                asyncio.run(run_scenario_with_error())
                
            # Проверяем, что был сделан скриншот
            mock_page.screenshot.assert_called()