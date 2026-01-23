"""
Тесты для модуля навигации по hh.ru (устаревший)
"""
import pytest
import warnings
from unittest.mock import AsyncMock, Mock, patch
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в путь Python
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.navigation import HHNavigation


class TestHHNavigation:
    """Тесты для класса HHNavigation (устаревший)"""

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
        page.goto = AsyncMock()
        page.click = AsyncMock()
        page.wait_for_selector = AsyncMock()
        page.wait_for_url = AsyncMock()
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
        """Тест инициализации класса HHNavigation"""
        # Проверяем, что генерируется предупреждение об устаревании
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # Выполнение
            nav = HHNavigation(mock_config, mock_logger)

            # Проверка
            assert nav.config == mock_config
            assert nav.logger == mock_logger
            # Проверяем, что было сгенерировано предупреждение
            assert len(w) >= 1
            assert issubclass(w[-1].category, DeprecationWarning)

    @pytest.mark.asyncio
    async def test_navigate_to_my_resumes_uses_new_handler(self, mock_config, mock_page, mock_logger):
        """Тест перехода на страницу 'Мои резюме' через новый обработчик"""
        # Проверяем, что генерируется предупреждение об устаревании
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # Подготовка
            nav = HHNavigation(mock_config, mock_logger)

            # Проверяем, что было сгенерировано предупреждение
            assert len(w) >= 1
            assert issubclass(w[-1].category, DeprecationWarning)

        # Мок для нового обработчика
        with patch('src.navigation.ResumeHandler') as mock_resume_handler_class:
            mock_resume_handler = Mock()
            mock_resume_handler.navigate_to_my_resumes = AsyncMock()
            mock_resume_handler_class.return_value = mock_resume_handler

            # Выполнение
            await nav.navigate_to_my_resumes(mock_page)

            # Проверка, что был вызван новый обработчик
            mock_resume_handler.navigate_to_my_resumes.assert_called_once()

    @pytest.mark.asyncio
    async def test_select_first_resume_uses_new_handler(self, mock_config, mock_page, mock_logger):
        """Тест выбора первого резюме через новый обработчик"""
        # Проверяем, что генерируется предупреждение об устаревании
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # Подготовка
            nav = HHNavigation(mock_config, mock_logger)

            # Проверяем, что было сгенерировано предупреждение
            assert len(w) >= 1
            assert issubclass(w[-1].category, DeprecationWarning)

        # Мок для нового обработчика
        with patch('src.navigation.ResumeHandler') as mock_resume_handler_class:
            mock_resume_handler = Mock()
            mock_resume_handler.select_first_resume = AsyncMock()
            mock_resume_handler_class.return_value = mock_resume_handler

            # Выполнение
            await nav.select_first_resume(mock_page)

            # Проверка, что был вызван новый обработчик
            mock_resume_handler.select_first_resume.assert_called_once()

    @pytest.mark.asyncio
    async def test_go_to_recommended_vacancies_uses_new_handler(self, mock_config, mock_page, mock_logger):
        """Тест перехода к рекомендуемым вакансиям через новый обработчик"""
        # Проверяем, что генерируется предупреждение об устаревании
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # Подготовка
            nav = HHNavigation(mock_config, mock_logger)

            # Проверяем, что было сгенерировано предупреждение
            assert len(w) >= 1
            assert issubclass(w[-1].category, DeprecationWarning)

        # Мок для нового обработчика
        with patch('src.navigation.ResumeHandler') as mock_resume_handler_class:
            mock_resume_handler = Mock()
            mock_resume_handler.go_to_recommended_vacancies = AsyncMock()
            mock_resume_handler_class.return_value = mock_resume_handler

            # Выполнение
            await nav.go_to_recommended_vacancies(mock_page, "resume123")

            # Проверка, что был вызван новый обработчик
            mock_resume_handler.go_to_recommended_vacancies.assert_called_once()

    @pytest.mark.asyncio
    async def test_wait_for_vacancies_loaded_uses_new_handler(self, mock_config, mock_page, mock_logger):
        """Тест ожидания загрузки вакансий через новый обработчик"""
        # Проверяем, что генерируется предупреждение об устаревании
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # Подготовка
            nav = HHNavigation(mock_config, mock_logger)

            # Проверяем, что было сгенерировано предупреждение
            assert len(w) >= 1
            assert issubclass(w[-1].category, DeprecationWarning)

        # Мок для нового обработчика
        with patch('src.navigation.ResumeHandler') as mock_resume_handler_class:
            mock_resume_handler = Mock()
            mock_resume_handler.wait_for_vacancies_loaded = AsyncMock()
            mock_resume_handler_class.return_value = mock_resume_handler

            # Выполнение
            await nav.wait_for_vacancies_loaded(mock_page)

            # Проверка, что был вызван новый обработчик
            mock_resume_handler.wait_for_vacancies_loaded.assert_called_once()