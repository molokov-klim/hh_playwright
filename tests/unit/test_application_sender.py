"""
Тесты для модуля отправки откликов
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в путь Python
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.application_sender import ApplicationSender


class TestApplicationSender:
    """Тесты для класса ApplicationSender"""

    @pytest.fixture
    def mock_config(self):
        """Мок конфигурации"""
        config = Mock()
        config.TIMEOUT = 30000
        config.FAKE = False  # По умолчанию режим FAKE выключен
        return config

    @pytest.fixture
    def mock_page(self):
        """Мок страницы Playwright"""
        page = Mock()
        page.click = AsyncMock()
        page.wait_for_selector = AsyncMock()
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

    def test_init_creates_correct_instance(self, mock_config, mock_logger):
        """Тест инициализации класса ApplicationSender"""
        # Выполнение
        sender = ApplicationSender(mock_config, mock_logger)

        # Проверка
        assert sender.config == mock_config
        assert sender.logger == mock_logger

    @pytest.mark.asyncio
    async def test_click_apply_button(self, mock_config, mock_page, mock_logger):
        """Тест клика по кнопке отклика"""
        # Подготовка
        sender = ApplicationSender(mock_config, mock_logger)
        vacancy = Mock()
        vacancy.click = AsyncMock()

        # Выполнение
        await sender.click_apply_button(vacancy)

        # Проверка
        vacancy.click.assert_called_once_with("[data-qa='apply-button']")

    @pytest.mark.asyncio
    async def test_wait_for_application_result_success(self, mock_config, mock_page, mock_logger):
        """Тест ожидания результата отклика - успех"""
        # Подготовка
        sender = ApplicationSender(mock_config, mock_logger)
        vacancy = Mock()

        # Мок для успешного ожидания
        vacancy.wait_for_selector = AsyncMock()

        # Выполнение
        result = await sender.wait_for_application_result(vacancy)

        # Проверка
        assert result == "Успешно"

    @pytest.mark.asyncio
    async def test_wait_for_application_result_timeout(self, mock_config, mock_page, mock_logger):
        """Тест ожидания результата отклика - таймаут"""
        # Подготовка
        sender = ApplicationSender(mock_config, mock_logger)
        vacancy = Mock()

        # Мок для таймаута
        vacancy.wait_for_selector.side_effect = Exception("Timeout")

        # Выполнение
        result = await sender.wait_for_application_result(vacancy)

        # Проверка
        assert result == "Ошибка"

    @pytest.mark.asyncio
    async def test_log_application_result(self, mock_config, mock_logger):
        """Тест логирования результата отклика"""
        # Подготовка
        sender = ApplicationSender(mock_config, mock_logger)
        vacancy_title = "Python Developer"
        vacancy_id = "vac123"
        result = "Успешно"

        # Выполнение
        await sender.log_application_result(vacancy_title, vacancy_id, result)

        # Проверка
        mock_logger.info.assert_called_once_with(f"Отклик на вакансию '{vacancy_title}' (ID: {vacancy_id}) завершен со статусом: {result}")

    @pytest.mark.asyncio
    async def test_apply_to_vacancy_success(self, mock_config, mock_page, mock_logger):
        """Тест полного цикла отклика на вакансию - успех"""
        # Подготовка
        sender = ApplicationSender(mock_config, mock_logger)
        vacancy = Mock()

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
                return Mock()

        vacancy.locator.side_effect = mock_locator

        # Мок для методов
        with patch.object(sender, 'click_apply_button', new_callable=AsyncMock) as mock_click_apply, \
             patch.object(sender, 'wait_for_application_result', new_callable=AsyncMock) as mock_wait_result, \
             patch.object(sender, 'log_application_result', new_callable=AsyncMock) as mock_log_result:

            # В зависимости от режима FAKE ожидаем разные результаты
            if mock_config.FAKE:
                # В режиме FAKE не должен вызываться click_apply_button
                result = await sender.apply_to_vacancy(vacancy)

                # Проверяем, что результат соответствует режиму FAKE
                assert result == "Успешно (FAKE)"

                # Проверяем, что click_apply_button не был вызван в режиме FAKE
                mock_click_apply.assert_not_called()
            else:
                # В обычном режиме должен вызываться click_apply_button
                mock_wait_result.return_value = "Успешно"

                # Выполнение
                result = await sender.apply_to_vacancy(vacancy)

                # Проверка
                mock_click_apply.assert_called_once_with(vacancy)
                mock_wait_result.assert_called_once_with(vacancy)
                mock_log_result.assert_called_once_with("Python Developer", "vac123", "Успешно")
                assert result == "Успешно"