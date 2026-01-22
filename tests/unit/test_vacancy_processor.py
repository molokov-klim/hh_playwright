"""
Тесты для модуля обработки вакансий
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в путь Python
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.vacancy_processor import VacancyProcessor


class TestVacancyProcessor:
    """Тесты для класса VacancyProcessor"""

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
        page.locator = Mock()
        page.wait_for_selector = AsyncMock()
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
        """Тест инициализации класса VacancyProcessor"""
        # Выполнение
        processor = VacancyProcessor(mock_config, mock_logger)

        # Проверка
        assert processor.config == mock_config
        assert processor.logger == mock_logger

    @pytest.mark.asyncio
    async def test_find_vacancy_cards(self, mock_config, mock_page, mock_logger):
        """Тест поиска карточек вакансий"""
        # Подготовка
        processor = VacancyProcessor(mock_config, mock_logger)
        
        # Мок для возвращения списка вакансий
        vacancy_locator = Mock()
        vacancy_locator.count = AsyncMock(return_value=5)
        mock_page.locator.return_value = vacancy_locator

        # Выполнение
        result = await processor.find_vacancy_cards(mock_page)

        # Проверка
        mock_page.locator.assert_called_once_with("[data-qa='vacancy']")
        assert result == 5  # count возвращает 5

    @pytest.mark.asyncio
    async def test_filter_applicable_vacancies(self, mock_config, mock_page, mock_logger):
        """Тест фильтрации вакансий по возможности отклика"""
        # Подготовка
        processor = VacancyProcessor(mock_config, mock_logger)
        
        # Создаем моки для вакансий
        vacancy1 = Mock()
        vacancy1.locator.return_value.count = AsyncMock(return_value=1)  # Есть кнопка "Откликнуться"
        
        vacancy2 = Mock()
        vacancy2.locator.return_value.count = AsyncMock(return_value=0)  # Нет кнопки "Откликнуться"
        
        vacancies = [vacancy1, vacancy2]

        # Выполнение
        result = await processor.filter_applicable_vacancies(vacancies)

        # Проверка
        assert len(result) == 1  # Только одна вакансия с кнопкой "Откликнуться"
        assert result[0] == vacancy1

    @pytest.mark.asyncio
    async def test_is_apply_button_available_returns_true(self, mock_config, mock_page, mock_logger):
        """Тест проверки доступности кнопки отклика - доступна"""
        # Подготовка
        processor = VacancyProcessor(mock_config, mock_logger)
        
        # Мок для вакансии с кнопкой отклика
        vacancy = Mock()
        apply_button_locator = Mock()
        apply_button_locator.count = AsyncMock(return_value=1)
        vacancy.locator.return_value = apply_button_locator

        # Выполнение
        result = await processor.is_apply_button_available(vacancy)

        # Проверка
        assert result is True

    @pytest.mark.asyncio
    async def test_is_apply_button_available_returns_false(self, mock_config, mock_page, mock_logger):
        """Тест проверки доступности кнопки отклика - недоступна"""
        # Подготовка
        processor = VacancyProcessor(mock_config, mock_logger)
        
        # Мок для вакансии без кнопки отклика
        vacancy = Mock()
        apply_button_locator = Mock()
        apply_button_locator.count = AsyncMock(return_value=0)
        vacancy.locator.return_value = apply_button_locator

        # Выполнение
        result = await processor.is_apply_button_available(vacancy)

        # Проверка
        assert result is False

    @pytest.mark.asyncio
    async def test_get_vacancy_info(self, mock_config, mock_page, mock_logger):
        """Тест получения информации о вакансии"""
        # Подготовка
        processor = VacancyProcessor(mock_config, mock_logger)
        
        # Мок для вакансии
        vacancy = Mock()
        title_element = Mock()
        title_element.inner_text = AsyncMock(return_value="Python Developer")
        vacancy.locator.return_value = title_element
        
        id_element = Mock()
        id_element.get_attribute = AsyncMock(return_value="vac123")
        vacancy.locator.return_value = id_element  # Это перезапишет предыдущее, нужно немного изменить

        # Для корректного тестирования создадим мок, который будет возвращать разные элементы в зависимости от селектора
        def mock_locator(selector):
            element = Mock()
            if selector == "[data-qa='vacancy-title']":
                element.inner_text = AsyncMock(return_value="Python Developer")
            elif selector == "[data-qa='vacancy-id']":
                element.get_attribute = AsyncMock(return_value="vac123")
            return element

        vacancy.locator.side_effect = mock_locator

        # Выполнение
        title, vacancy_id = await processor.get_vacancy_info(vacancy)

        # Проверка
        assert title == "Python Developer"
        assert vacancy_id == "vac123"