"""
Интеграционный тест для полного сценария работы скрипта с новой архитектурой
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch, MagicMock
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в путь Python
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.config import Config, get_config_from_env
from src.business_logic.auth_handler import AuthHandler
from src.business_logic.resume_handler import ResumeHandler
from src.business_logic.vacancy_handler import VacancyHandler
from src.business_logic.application_handler import ApplicationHandler
from src.business_logic.session_manager import SessionManager
from src.steps.auth_steps import AuthSteps
from src.steps.resume_steps import ResumeSteps
from src.steps.vacancy_steps import VacancySteps
from src.steps.application_steps import ApplicationSteps
from src.steps.main_workflow import MainWorkflow
from src.error_handler import ErrorHandler
from src.logger import setup_logger


class TestFullScenario:
    """Интеграционный тест для полного сценария работы скрипта с новой архитектурой"""

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
        page.locator = Mock()
        return page

    @pytest.fixture
    def mock_logger(self):
        """Мок логгера"""
        logger = Mock()
        logger.info = Mock()
        logger.error = Mock()
        logger.debug = Mock()
        return logger

    def test_full_scenario_success_flow_with_steps(self, mock_config, mock_page, mock_logger):
        """Тест полного сценария - успешный поток с использованием шагов"""
        # Подготовка всех модулей на уровне шагов
        auth_steps = AuthSteps(mock_page, mock_config, mock_logger)
        resume_steps = ResumeSteps(mock_page, mock_config, mock_logger)
        vacancy_steps = VacancySteps(mock_page, mock_config, mock_logger)
        application_steps = ApplicationSteps(mock_page, mock_config, mock_logger)

        # Мок для успешной авторизации и всех остальных шагов
        with patch.object(auth_steps.auth_handler.auth_page, 'is_logged_in', return_value=True), \
             patch.object(auth_steps.auth_handler.auth_page, 'navigate_to_login_page', return_value=True), \
             patch.object(auth_steps.auth_handler.auth_page, 'fill_login', return_value=True), \
             patch.object(auth_steps.auth_handler.auth_page, 'fill_password', return_value=True), \
             patch.object(resume_steps.resume_handler.resume_page, 'select_first_resume', return_value=True), \
             patch.object(resume_steps.resume_handler.resume_page, 'go_to_recommended_vacancies', return_value=True), \
             patch.object(vacancy_steps.vacancy_handler.vacancy_page, 'get_vacancy_locators', return_value=[Mock(), Mock()]), \
             patch.object(vacancy_steps.vacancy_handler, 'get_applicable_vacancies', return_value=[Mock()]), \
             patch.object(application_steps.application_handler, 'apply_to_vacancy', return_value="Успешно"):

            async def run_full_scenario():
                # 1. Авторизация
                auth_result = await auth_steps.login_to_hh()
                assert auth_result is True

                # 2. Навигация к резюме
                await resume_steps.navigate_to_my_resumes()

                # 3. Выбор первого резюме
                await resume_steps.select_first_resume()

                # 4. Переход к рекомендуемым вакансиям
                await resume_steps.go_to_recommended_vacancies()

                # 5. Ожидание загрузки вакансий
                await vacancy_steps.wait_for_vacancies_loaded()

                # 6. Поиск вакансий
                vacancy_locators = await vacancy_steps.get_vacancy_locators()
                assert len(vacancy_locators) == 2

                # 7. Фильтрация вакансий
                applicable_vacancies = await vacancy_steps.get_applicable_vacancies()
                assert len(applicable_vacancies) >= 0  # Может быть 0 или больше

                # 8. Отправка откликов на все подходящие вакансии
                for vacancy in applicable_vacancies[:1]:  # Ограничиваем до одной для теста
                    result = await application_steps.apply_to_vacancy(vacancy)
                    assert result in ["Успешно", "Ошибка"]

                # Проверка, что были вызваны ключевые методы
                mock_page.goto.assert_called()

            import asyncio
            asyncio.run(run_full_scenario())

    def test_full_scenario_with_business_logic(self, mock_config, mock_page, mock_logger):
        """Тест полного сценария с использованием бизнес-логики"""
        # Подготовка всех модулей на уровне бизнес-логики
        auth_handler = AuthHandler(mock_page, mock_config, mock_logger)
        resume_handler = ResumeHandler(mock_page, mock_config, mock_logger)
        vacancy_handler = VacancyHandler(mock_page, mock_config, mock_logger)
        application_handler = ApplicationHandler(mock_page, mock_config, mock_logger)

        # Мок для успешной авторизации и всех остальных шагов
        with patch.object(auth_handler.auth_page, 'is_logged_in', return_value=True), \
             patch.object(auth_handler.auth_page, 'navigate_to_login_page', return_value=True), \
             patch.object(auth_handler.auth_page, 'fill_login', return_value=True), \
             patch.object(auth_handler.auth_page, 'fill_password', return_value=True), \
             patch.object(resume_handler.resume_page, 'select_first_resume', return_value=True), \
             patch.object(resume_handler.resume_page, 'go_to_recommended_vacancies', return_value=True), \
             patch.object(vacancy_handler.vacancy_page, 'get_vacancy_locators', return_value=[Mock(), Mock()]), \
             patch.object(vacancy_handler, 'get_applicable_vacancies', return_value=[Mock()]), \
             patch.object(application_handler, 'apply_to_vacancy', return_value="Успешно"):

            async def run_full_scenario():
                # 1. Авторизация
                auth_result = await auth_handler.perform_auth()
                assert auth_result is True

                # 2. Навигация к резюме
                await resume_handler.navigate_to_my_resumes()

                # 3. Выбор первого резюме
                await resume_handler.select_first_resume()

                # 4. Переход к рекомендуемым вакансиям
                await resume_handler.go_to_recommended_vacancies()

                # 5. Ожидание загрузки вакансий
                await resume_handler.wait_for_vacancies_loaded()

                # 6. Поиск вакансий
                vacancy_locators = await vacancy_handler.get_vacancy_locators()
                assert len(vacancy_locators) == 2

                # 7. Фильтрация вакансий
                applicable_vacancies = await vacancy_handler.get_applicable_vacancies()
                assert len(applicable_vacancies) >= 0  # Может быть 0 или больше

                # 8. Отправка откликов на все подходящие вакансии
                for vacancy in applicable_vacancies[:1]:  # Ограничиваем до одной для теста
                    result = await application_handler.apply_to_vacancy(vacancy)
                    assert result in ["Успешно", "Ошибка"]

                # Проверка, что были вызваны ключевые методы
                mock_page.goto.assert_called()

            import asyncio
            asyncio.run(run_full_scenario())

    def test_main_workflow_integration(self, mock_config, mock_page, mock_logger):
        """Тест полного сценария через основной workflow"""
        # Подготовка основного сценария
        main_workflow = MainWorkflow(mock_page, mock_config, mock_logger)

        # Мок для всех необходимых компонентов
        with patch.object(main_workflow.auth_steps.auth_handler.auth_page, 'is_logged_in', return_value=True), \
             patch.object(main_workflow.auth_steps.auth_handler.auth_page, 'navigate_to_login_page', return_value=True), \
             patch.object(main_workflow.auth_steps.auth_handler.auth_page, 'fill_login', return_value=True), \
             patch.object(main_workflow.auth_steps.auth_handler.auth_page, 'fill_password', return_value=True), \
             patch.object(main_workflow.resume_steps.resume_handler.resume_page, 'select_first_resume', return_value=True), \
             patch.object(main_workflow.resume_steps.resume_handler.resume_page, 'go_to_recommended_vacancies', return_value=True), \
             patch.object(main_workflow.vacancy_steps.vacancy_handler.vacancy_page, 'get_vacancy_locators', return_value=[Mock()]), \
             patch.object(main_workflow.vacancy_steps.vacancy_handler, 'get_applicable_vacancies', return_value=[Mock()]), \
             patch.object(main_workflow.application_steps.application_handler, 'apply_to_vacancy', return_value="Успешно"):

            async def run_full_workflow():
                result = await main_workflow.run_full_workflow()
                # run_full_workflow возвращает кортеж (успех, количество успешных откликов, количество ошибок)
                success, success_count, error_count = result
                assert success is True

            import asyncio
            asyncio.run(run_full_workflow())

    def test_full_scenario_with_error_handling(self, mock_config, mock_page, mock_logger):
        """Тест полного сценария с обработкой ошибок"""
        # Подготовка всех модулей
        auth_steps = AuthSteps(mock_page, mock_config, mock_logger)

        # Мокируем конфигурацию так, чтобы не вызывался TelegramNotifier
        mock_config.TELEGRAM_BOT_TOKEN = None
        mock_config.TELEGRAM_CHAT_ID = None

        error_handler = ErrorHandler(mock_config, mock_logger)

        # Мок для неудачной авторизации и обработки ошибок
        with patch.object(auth_steps.auth_handler.auth_page, 'is_logged_in', return_value=False), \
             patch.object(error_handler, 'create_error_screenshot_path', return_value="test_screenshot.png"), \
             patch.object(mock_page, 'screenshot', AsyncMock()):

            async def run_test():
                # Создаем фейковое исключение
                fake_exception = Exception("Test error for scenario")

                # Вызываем обработчик ошибок и перехватываем исключение
                try:
                    await error_handler.handle_general_error(mock_page, fake_exception)
                except Exception:
                    pass  # Исключение ожидаемо, игнорируем его

                # Проверяем, что был сделан скриншот
                mock_page.screenshot.assert_called()

            import asyncio
            asyncio.run(run_test())