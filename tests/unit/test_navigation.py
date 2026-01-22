"""
Тесты для модуля навигации по hh.ru
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в путь Python
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.navigation import HHNavigation


class TestHHNavigation:
    """Тесты для класса HHNavigation"""

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
        # Выполнение
        nav = HHNavigation(mock_config, mock_logger)

        # Проверка
        assert nav.config == mock_config
        assert nav.logger == mock_logger

    @pytest.mark.asyncio
    async def test_navigate_to_my_resumes(self, mock_config, mock_page, mock_logger):
        """Тест перехода на страницу 'Мои резюме'"""
        # Подготовка
        nav = HHNavigation(mock_config, mock_logger)

        # Выполнение
        await nav.navigate_to_my_resumes(mock_page)

        # Проверка
        mock_page.goto.assert_called_once_with("https://hh.ru/applicant/resumes")

    @pytest.mark.asyncio
    async def test_select_resume_by_id(self, mock_config, mock_page, mock_logger):
        """Тест выбора резюме по ID"""
        # Подготовка
        nav = HHNavigation(mock_config, mock_logger)
        resume_id = "123456"

        # Выполнение
        await nav.select_resume(mock_page, resume_id)

        # Проверка
        mock_page.click.assert_called_once_with(f"[data-qa='resume-list-item-{resume_id}']")

    @pytest.mark.asyncio
    async def test_select_first_resume(self, mock_config, mock_page, mock_logger):
        """Тест выбора первого резюме"""
        # Подготовка
        nav = HHNavigation(mock_config, mock_logger)

        # Выполнение
        await nav.select_first_resume(mock_page)

        # Проверка
        mock_page.click.assert_called_once_with("[data-qa='resume-list-item']:first-child")

    @pytest.mark.asyncio
    async def test_go_to_recommended_vacancies_with_resume_id(self, mock_config, mock_page, mock_logger):
        """Тест перехода к рекомендуемым вакансиям с указанием ID резюме"""
        # Подготовка
        nav = HHNavigation(mock_config, mock_logger)
        resume_id = "123456"

        # Выполнение
        await nav.go_to_recommended_vacancies(mock_page, resume_id)

        # Проверка
        mock_page.click.assert_called_once_with("[data-qa='recommended-vacancies-tab']")

    @pytest.mark.asyncio
    async def test_wait_for_vacancies_loaded(self, mock_config, mock_page, mock_logger):
        """Тест ожидания загрузки вакансий"""
        # Подготовка
        nav = HHNavigation(mock_config, mock_logger)

        # Выполнение
        await nav.wait_for_vacancies_loaded(mock_page)

        # Проверка
        mock_page.wait_for_selector.assert_called_once_with("[data-qa='vacancy']", timeout=mock_config.TIMEOUT)