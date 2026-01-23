"""
Тесты для шагов работы с вакансиями
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch
from src.steps.vacancy_steps import VacancySteps
from src.config import Config


@pytest.mark.asyncio
class TestVacancySteps:
    """Тесты для VacancySteps"""
    
    @pytest.fixture
    def mock_page(self):
        """Мок страницы Playwright"""
        page = Mock()
        page.goto = AsyncMock()
        page.fill = AsyncMock()
        page.click = AsyncMock()
        page.wait_for_selector = AsyncMock()
        page.is_visible = AsyncMock(return_value=True)
        page.locator = Mock()
        page.press = AsyncMock()
        return page
    
    @pytest.fixture
    def mock_config(self):
        """Мок конфигурации"""
        config = Mock(spec=Config)
        config.HH_LOGIN = "test@example.com"
        config.HH_PASSWORD = "password123"
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
    def vacancy_steps(self, mock_page, mock_config, mock_logger):
        """Создание экземпляра VacancySteps для тестов"""
        return VacancySteps(mock_page, mock_config, mock_logger)
    
    async def test_get_vacancy_locators(self, vacancy_steps):
        """Тест получения локаторов вакансий"""
        mock_locators = [Mock(), Mock()]
        with patch.object(vacancy_steps.vacancy_handler, 'get_vacancy_locators', return_value=mock_locators):
            
            locators = await vacancy_steps.get_vacancy_locators()
            
            assert locators == mock_locators
    
    async def test_get_applicable_vacancies(self, vacancy_steps):
        """Тест получения вакансий, на которые можно откликнуться"""
        mock_vacancies = [Mock(), Mock()]
        with patch.object(vacancy_steps.vacancy_handler, 'get_applicable_vacancies', return_value=mock_vacancies):
            
            vacancies = await vacancy_steps.get_applicable_vacancies()
            
            assert vacancies == mock_vacancies
    
    async def test_wait_for_vacancies_loaded(self, vacancy_steps):
        """Тест ожидания загрузки вакансий"""
        timeout = 30000
        with patch.object(vacancy_steps.vacancy_handler, 'wait_for_vacancies_loaded', return_value=True):
            
            result = await vacancy_steps.wait_for_vacancies_loaded(timeout)
            
            assert result is True