"""
Тест для проверки работы переменной FAKE в новой архитектуре
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch
import asyncio
from src.business_logic.application_handler import ApplicationHandler
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

    async def test_apply_to_vacancy_with_fake_enabled_does_not_click_buttons(
        self, mock_page, mock_config_with_fake_enabled, mock_logger
    ):
        """Тест, что при включенном режиме FAKE не происходит реальных кликов по кнопкам"""
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

        # Проверяем, что логгер получил сообщение о результате в режиме FAKE
        mock_logger.info.assert_called()
        # Проверяем, что в логах есть сообщение о режиме FAKE
        logged_messages = [call[0][0] for call in mock_logger.info.call_args_list]
        fake_message_found = any("Успешно (FAKE)" in msg for msg in logged_messages)
        assert fake_message_found, f"Ожидается сообщение о режиме FAKE в логах, получены: {logged_messages}"

    async def test_apply_to_vacancy_with_fake_disabled_clicks_buttons(
        self, mock_page, mock_config_with_fake_disabled, mock_logger
    ):
        """Тест, что при выключенном режиме FAKE происходят реальные клики по кнопкам"""
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

            # Проверяем, что логгер получил сообщение о реальном отклике (а не о режиме FAKE)
            # В реальной ситуации логгер.info будет вызван с сообщением о реальном отклике
            # но в тесте мы проверяем, что сообщение о режиме FAKE не появилось
            # Проверим, что в логах нет сообщения о режиме FAKE
            for call in mock_logger.info.call_args_list:
                assert "Режим FAKE включен" not in str(call)