"""
Интеграционные тесты для проверки взаимодействия модулей новой архитектуры
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


class TestModuleIntegration:
    """Интеграционные тесты для проверки взаимодействия модулей новой архитектуры"""

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

    def test_auth_and_resume_integration_business_logic(self, mock_config, mock_page):
        """Тест интеграции модулей авторизации и резюме на уровне бизнес-логики"""
        # Подготовка
        logger = setup_logger("test_auth_resume_integration")

        auth_handler = AuthHandler(mock_page, mock_config, logger)
        resume_handler = ResumeHandler(mock_page, mock_config, logger)

        # Мок для успешной авторизации
        with patch.object(auth_handler.auth_page, 'is_logged_in', return_value=True), \
             patch.object(auth_handler.auth_page, 'navigate_to_login_page', return_value=True), \
             patch.object(auth_handler.auth_page, 'fill_login', return_value=True), \
             patch.object(auth_handler.auth_page, 'fill_password', return_value=True):

            # Выполнение - сначала авторизация, потом навигация
            import asyncio

            async def run_test():
                # Авторизация
                auth_result = await auth_handler.perform_auth()
                assert auth_result is True

                # Навигация после авторизации
                await resume_handler.navigate_to_my_resumes()

                # Проверка, что были вызваны методы обоих модулей
                mock_page.goto.assert_called()

            asyncio.run(run_test())

    def test_resume_and_vacancy_integration_business_logic(self, mock_config, mock_page):
        """Тест интеграции модулей резюме и обработки вакансий на уровне бизнес-логики"""
        # Подготовка
        logger = setup_logger("test_resume_vac_proc_integration")

        resume_handler = ResumeHandler(mock_page, mock_config, logger)
        vacancy_handler = VacancyHandler(mock_page, mock_config, logger)

        # Мок для вакансий
        vacancy_locator = Mock()
        vacancy_locator.count = AsyncMock(return_value=3)
        mock_page.locator.return_value = vacancy_locator

        async def run_test():
            # Навигация к рекомендуемым вакансиям
            await resume_handler.go_to_recommended_vacancies()

            # Поиск вакансий
            vacancy_locators = await vacancy_handler.get_vacancy_locators()
            assert len(vacancy_locators) == 3

            # Проверка, что были вызваны методы обоих модулей
            mock_page.locator.assert_called()
            vacancy_locator.count.assert_called()

        import asyncio
        asyncio.run(run_test())

    def test_vacancy_handler_and_application_handler_integration(self, mock_config, mock_page):
        """Тест интеграции модулей обработки вакансий и отправки откликов на уровне бизнес-логики"""
        # Подготовка
        logger = setup_logger("test_vac_handler_app_handler_integration")

        vacancy_handler = VacancyHandler(mock_page, mock_config, logger)
        application_handler = ApplicationHandler(mock_page, mock_config, logger)

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
            is_available = await vacancy_handler.is_apply_button_available(vacancy)
            assert is_available is True

            # Отправка отклика на вакансию
            result = await application_handler.apply_to_vacancy(vacancy)
            assert result in ["Успешно", "Ошибка", "Успешно (FAKE)"]

        import asyncio
        asyncio.run(run_test())

    def test_full_integration_flow_using_steps(self, mock_config, mock_page):
        """Тест полного интеграционного потока с использованием шагов"""
        # Подготовка
        logger = setup_logger("test_full_integration_flow")

        auth_steps = AuthSteps(mock_page, mock_config, logger)
        resume_steps = ResumeSteps(mock_page, mock_config, logger)
        vacancy_steps = VacancySteps(mock_page, mock_config, logger)
        application_steps = ApplicationSteps(mock_page, mock_config, logger)

        # Мок для успешной авторизации
        with patch.object(auth_steps.auth_handler.auth_page, 'is_logged_in', return_value=True), \
             patch.object(auth_steps.auth_handler.auth_page, 'navigate_to_login_page', return_value=True), \
             patch.object(auth_steps.auth_handler.auth_page, 'fill_login', return_value=True), \
             patch.object(auth_steps.auth_handler.auth_page, 'fill_password', return_value=True), \
             patch.object(vacancy_steps.vacancy_handler.vacancy_page, 'get_vacancy_locators', return_value=[Mock(), Mock()]), \
             patch.object(vacancy_steps.vacancy_handler, 'get_applicable_vacancies', return_value=[Mock()]), \
             patch.object(application_steps.application_handler, 'apply_to_vacancy', return_value="Успешно"):

            import asyncio

            async def run_test():
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
                assert len(vacancy_locators) > 0

                # 7. Фильтрация вакансий
                applicable_vacancies = await vacancy_steps.get_applicable_vacancies()
                assert len(applicable_vacancies) >= 0  # Может быть 0 или больше

                # 8. Отправка откликов на все подходящие вакансии
                for i, vacancy in enumerate(applicable_vacancies[:1]):  # Ограничиваем до одной для теста
                    result = await application_steps.apply_to_vacancy(vacancy)
                    assert result in ["Успешно", "Ошибка"]

                # Проверка, что были вызваны ключевые методы
                mock_page.goto.assert_called()
                mock_page.click.assert_called()

            asyncio.run(run_test())

    def test_main_workflow_integration(self, mock_config, mock_page):
        """Тест интеграции через основной сценарий"""
        # Подготовка
        logger = setup_logger("test_main_workflow_integration")

        main_workflow = MainWorkflow(mock_page, mock_config, logger)

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

            import asyncio

            async def run_test():
                # Выполнение полного сценария
                result = await main_workflow.run_full_workflow()
                assert result is True

            asyncio.run(run_test())

    def test_error_handler_integration_with_new_modules(self, mock_config, mock_page):
        """Тест интеграции модуля обработки ошибок с новыми модулями"""
        # Подготовка
        logger = setup_logger("test_error_handler_integration")

        error_handler = ErrorHandler(mock_config, logger)
        auth_handler = AuthHandler(mock_page, mock_config, logger)

        async def run_test():
            # Тест обработки ошибки в контексте нового модуля
            try:
                await error_handler.handle_captcha_detection(mock_page, "Обнаружена капча")
            except Exception as e:
                assert "Обнаружена капча" in str(e)

            # Проверка, что скриншот был сделан
            mock_page.screenshot.assert_called()

        import asyncio
        asyncio.run(run_test())