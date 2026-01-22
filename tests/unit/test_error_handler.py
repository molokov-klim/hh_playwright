"""
Тесты для модуля обработки ошибок
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch, MagicMock
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в путь Python
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.error_handler import ErrorHandler


class TestErrorHandler:
    """Тесты для класса ErrorHandler"""

    @pytest.fixture
    def mock_config(self):
        """Мок конфигурации"""
        config = Mock()
        config.TIMEOUT = 30000
        return config

    @pytest.fixture
    def mock_page(self):
        """Мок страницы Playwright"""
        page = Mock()
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

    def test_init_creates_correct_instance(self, mock_config, mock_logger):
        """Тест инициализации класса ErrorHandler"""
        # Выполнение
        handler = ErrorHandler(mock_config, mock_logger)

        # Проверка
        assert handler.config == mock_config
        assert handler.logger == mock_logger

    @pytest.mark.asyncio
    async def test_take_screenshot_on_error(self, mock_config, mock_page, mock_logger):
        """Тест создания скриншота при ошибке"""
        # Подготовка
        handler = ErrorHandler(mock_config, mock_logger)
        screenshot_path = "/tmp/error_screenshot.png"

        # Выполнение
        await handler.take_screenshot_on_error(mock_page, screenshot_path)

        # Проверка
        mock_page.screenshot.assert_called_once_with(path=screenshot_path)

    @pytest.mark.asyncio
    async def test_handle_captcha_detection(self, mock_config, mock_page, mock_logger):
        """Тест обработки обнаружения капчи"""
        # Подготовка
        handler = ErrorHandler(mock_config, mock_logger)
        error_msg = "Обнаружена капча"
        
        with patch.object(handler, 'take_screenshot_on_error', new_callable=AsyncMock) as mock_take_screenshot:
            # Выполнение
            with pytest.raises(Exception, match=error_msg):
                await handler.handle_captcha_detection(mock_page, error_msg)

            # Проверка
            mock_take_screenshot.assert_called_once()
            mock_logger.error.assert_called_once_with(error_msg)

    @pytest.mark.asyncio
    async def test_handle_unexpected_modal_window(self, mock_config, mock_page, mock_logger):
        """Тест обработки неожиданного модального окна"""
        # Подготовка
        handler = ErrorHandler(mock_config, mock_logger)
        error_msg = "Обнаружено неожиданное модальное окно"
        
        with patch.object(handler, 'take_screenshot_on_error', new_callable=AsyncMock) as mock_take_screenshot:
            # Выполнение
            with pytest.raises(Exception, match=error_msg):
                await handler.handle_unexpected_modal_window(mock_page, error_msg)

            # Проверка
            mock_take_screenshot.assert_called_once()
            mock_logger.error.assert_called_once_with(error_msg)

    @pytest.mark.asyncio
    async def test_handle_general_error(self, mock_config, mock_page, mock_logger):
        """Тест обработки общей ошибки"""
        # Подготовка
        handler = ErrorHandler(mock_config, mock_logger)
        error = Exception("Общая ошибка")
        
        with patch.object(handler, 'take_screenshot_on_error', new_callable=AsyncMock) as mock_take_screenshot:
            # Выполнение
            with pytest.raises(Exception, match=str(error)):
                await handler.handle_general_error(mock_page, error)

            # Проверка
            mock_take_screenshot.assert_called_once()
            mock_logger.error.assert_called_once_with(f"Произошла непредвиденная ошибка: {error}")

    def test_create_error_screenshot_path(self, mock_config, mock_logger):
        """Тест создания пути для скриншота ошибки"""
        # Подготовка
        handler = ErrorHandler(mock_config, mock_logger)

        # Выполнение
        path = handler.create_error_screenshot_path()

        # Проверка
        assert path.startswith("error_screenshot_")
        assert path.endswith(".png")
        assert len(path) > len("error_screenshot_.png")  # Проверяем, что в имени есть временная метка