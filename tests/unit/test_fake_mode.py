"""
Тесты для проверки работы режима FAKE в бизнес-логике
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch
from src.business_logic.application_handler import ApplicationHandler
from src.config import Config


@pytest.mark.asyncio
class TestFakeModeInBusinessLogic:
    """Тесты для проверки работы режима FAKE в бизнес-логике"""

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
    def mock_config(self):
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
    def mock_logger(self):
        """Мок логгера"""
        logger = Mock()
        logger.info = Mock()
        logger.error = Mock()
        logger.debug = Mock()
        return logger

    @pytest.fixture
    def application_handler_with_fake(self, mock_page, mock_config, mock_logger):
        """Создание экземпляра ApplicationHandler с включенным режимом FAKE"""
        return ApplicationHandler(mock_page, mock_config, mock_logger)

    async def test_apply_to_vacancy_in_fake_mode_does_not_click_buttons(self, application_handler_with_fake, mock_page):
        """Тест, что в режиме FAKE не происходит реальных кликов по кнопкам"""
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

        # Выполнение отклика
        result = await application_handler_with_fake.apply_to_vacancy(vacancy)

        # Проверка результата
        assert result == "Успешно (FAKE)"

        # Проверка, что в режиме FAKE не были вызваны методы клика
        mock_page.click.assert_not_called()
        vacancy.click.assert_not_called()

    async def test_apply_to_vacancy_in_fake_mode_still_logs_result(self, application_handler_with_fake, mock_logger):
        """Тест, что в режиме FAKE все равно происходит логирование результата"""
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

        # Выполнение отклика
        result = await application_handler_with_fake.apply_to_vacancy(vacancy)

        # Проверка, что результат правильный
        assert result == "Успешно (FAKE)"

        # Проверка, что метод логирования был вызван
        mock_logger.info.assert_called()

    async def test_apply_to_vacancy_real_mode_calls_click_methods(self, mock_page, mock_config, mock_logger):
        """Тест, что в обычном режиме (FAKE=False) происходят реальные клики"""
        # Отключаем режим FAKE
        mock_config.FAKE = False

        # Создаем обработчик
        application_handler = ApplicationHandler(mock_page, mock_config, mock_logger)

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
             patch.object(application_handler, 'wait_for_response_result', return_value="Успешно"), \
             patch.object(application_handler, 'log_application_result'):

            # Выполнение отклика
            result = await application_handler.apply_to_vacancy(vacancy)

            # Проверка результата
            assert result == "Успешно"

            # В нормальном режиме должны были быть вызваны методы клика
            application_handler.click_apply_button.assert_called_once()
            application_handler.click_send_response.assert_called_once()