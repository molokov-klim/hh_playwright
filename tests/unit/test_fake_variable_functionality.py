"""
Тесты для проверки новой функциональности переменной FAKE
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch
import asyncio
from src.config import Config


@pytest.mark.asyncio
class TestFakeVariableFunctionality:
    """Тесты для проверки функциональности переменной FAKE"""
    
    @pytest.fixture
    def mock_page(self):
        """Мок страницы Playwright"""
        page = Mock()
        page.goto = AsyncMock()
        page.fill = AsyncMock()
        page.click = AsyncMock()
        page.wait_for_selector = AsyncMock()
        page.is_visible = AsyncMock(return_value=True)
        page.screenshot = AsyncMock()
        page.locator = Mock()
        return page

    @pytest.fixture
    def mock_config_with_fake_enabled(self):
        """Мок конфигурации с включенным режимом FAKE"""
        config = Mock(spec=Config)
        config.HH_LOGIN = "test@example.com"
        config.HH_PASSWORD = "password123"
        config.TIMEOUT = 30000
        config.HEADLESS = True
        config.VIEWPORT_WIDTH = 1920
        config.VIEWPORT_HEIGHT = 1080
        config.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        config.FAKE = True  # Включаем режим FAKE
        return config

    @pytest.fixture
    def mock_config_with_fake_disabled(self):
        """Мок конфигурации с выключенным режимом FAKE"""
        config = Mock(spec=Config)
        config.HH_LOGIN = "test@example.com"
        config.HH_PASSWORD = "password123"
        config.TIMEOUT = 30000
        config.HEADLESS = True
        config.VIEWPORT_WIDTH = 1920
        config.VIEWPORT_HEIGHT = 1080
        config.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        config.FAKE = False  # Выключаем режим FAKE
        return config

    @pytest.fixture
    def mock_logger(self):
        """Мок логгера"""
        logger = Mock()
        logger.info = Mock()
        logger.error = Mock()
        logger.debug = Mock()
        return logger

    async def test_application_handler_with_fake_enabled_does_not_click_buttons(
        self, mock_page, mock_config_with_fake_enabled, mock_logger
    ):
        """Тест, что при включенной переменной FAKE не происходит реальных кликов по кнопкам"""
        from src.business_logic.application_handler import ApplicationHandler
        
        # Создаем обработчик с включенным режимом FAKE
        application_handler = ApplicationHandler(mock_page, mock_config_with_fake_enabled, mock_logger)

        # Подготовка вакансии
        vacancy = Mock()
        vacancy.click = AsyncMock()
        vacancy.wait_for_selector = AsyncMock()
        vacancy.locator = Mock()

        # Мок для получения информации о вакансии
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

        # Выполняем отклик
        result = await application_handler.apply_to_vacancy(vacancy)

        # Проверяем, что результат соответствует режиму FAKE
        assert result == "Успешно (FAKE)"

        # Проверяем, что реальные клики не были выполнены
        mock_page.click.assert_not_called()
        vacancy.click.assert_not_called()

    async def test_application_handler_with_fake_disabled_clicks_buttons(
        self, mock_page, mock_config_with_fake_disabled, mock_logger
    ):
        """Тест, что при выключенной переменной FAKE происходят реальные клики по кнопкам"""
        from src.business_logic.application_handler import ApplicationHandler
        
        # Создаем обработчик с выключенным режимом FAKE
        application_handler = ApplicationHandler(mock_page, mock_config_with_fake_disabled, mock_logger)

        # Подготовка вакансии
        vacancy = Mock()
        vacancy.click = AsyncMock()
        vacancy.wait_for_selector = AsyncMock()
        vacancy.locator = Mock()

        # Мок для получения информации о вакансии
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

        # Мок для методов обработчика
        with patch.object(application_handler, 'click_apply_button', return_value=True), \
             patch.object(application_handler, 'fill_cover_letter', return_value=True), \
             patch.object(application_handler, 'click_send_response', return_value=True), \
             patch.object(application_handler, 'wait_for_response_result', return_value="Успешно"):

            # Выполняем отклик
            result = await application_handler.apply_to_vacancy(vacancy)

            # Проверяем, что результат НЕ соответствует режиму FAKE
            assert result == "Успешно"

            # Проверяем, что методы клика были вызваны
            application_handler.click_apply_button.assert_called_once()
            application_handler.click_send_response.assert_called_once()

    async def test_application_steps_with_fake_enabled(
        self, mock_page, mock_config_with_fake_enabled, mock_logger
    ):
        """Тест, что шаги отклика учитывают переменную FAKE"""
        from src.steps.application_steps import ApplicationSteps
        
        # Создаем шаги с включенным режимом FAKE
        application_steps = ApplicationSteps(mock_page, mock_config_with_fake_enabled, mock_logger)

        # Подготовка вакансии
        vacancy = Mock()
        vacancy.click = AsyncMock()
        vacancy.wait_for_selector = AsyncMock()
        vacancy.locator = Mock()

        # Мок для получения информации о вакансии
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

        # Выполняем отклик
        result = await application_steps.apply_to_vacancy(vacancy)

        # Проверяем, что результат соответствует режиму FAKE
        assert result == "Успешно (FAKE)"

    async def test_main_workflow_with_fake_enabled(
        self, mock_page, mock_config_with_fake_enabled, mock_logger
    ):
        """Тест, что основной сценарий учитывает переменную FAKE"""
        from src.steps.main_workflow import MainWorkflow
        
        # Создаем основной сценарий с включенным режимом FAKE
        main_workflow = MainWorkflow(mock_page, mock_config_with_fake_enabled, mock_logger)

        # Мок для всех необходимых компонентов
        with patch.object(main_workflow.auth_steps.auth_handler.auth_page, 'is_logged_in', return_value=True), \
             patch.object(main_workflow.auth_steps.auth_handler.auth_page, 'navigate_to_login_page', return_value=True), \
             patch.object(main_workflow.auth_steps.auth_handler.auth_page, 'fill_login', return_value=True), \
             patch.object(main_workflow.auth_steps.auth_handler.auth_page, 'fill_password', return_value=True), \
             patch.object(main_workflow.resume_steps.resume_handler.resume_page, 'select_first_resume', return_value=True), \
             patch.object(main_workflow.resume_steps.resume_handler.resume_page, 'go_to_recommended_vacancies', return_value=True), \
             patch.object(main_workflow.vacancy_steps.vacancy_handler.vacancy_page, 'get_vacancy_locators', return_value=[Mock()]), \
             patch.object(main_workflow.vacancy_steps.vacancy_handler, 'get_applicable_vacancies', return_value=[Mock()]), \
             patch.object(main_workflow.application_steps.application_handler, 'apply_to_vacancy', return_value="Успешно (FAKE)"):
            
            # Выполняем полный сценарий
            result = await main_workflow.run_full_workflow()

            # run_full_workflow возвращает кортеж (успех, количество успешных откликов, количество ошибок)
            success, success_count, error_count = result
            # Проверяем, что сценарий завершился успешно
            assert success is True
            assert success_count == 1  # 1 вакансия, на которую откликнулись
            assert error_count == 0