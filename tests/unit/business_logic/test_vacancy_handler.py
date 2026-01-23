"""
Тесты для обработчика вакансий
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch
from src.business_logic.vacancy_handler import VacancyHandler
from src.config import Config


@pytest.mark.asyncio
class TestVacancyHandler:
    """Тесты для VacancyHandler"""
    
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
    def vacancy_handler(self, mock_page, mock_config, mock_logger):
        """Создание экземпляра VacancyHandler для тестов"""
        return VacancyHandler(mock_page, mock_config, mock_logger)
    
    async def test_get_vacancy_locators(self, vacancy_handler):
        """Тест получения локаторов вакансий"""
        mock_locators = [Mock(), Mock()]
        with patch.object(vacancy_handler.vacancy_page, 'get_vacancy_locators', return_value=mock_locators):
            
            locators = await vacancy_handler.get_vacancy_locators()
            
            assert locators == mock_locators
    
    async def test_is_apply_button_available(self, vacancy_handler):
        """Тест проверки доступности кнопки отклика"""
        mock_vacancy_locator = Mock()
        with patch.object(vacancy_handler.vacancy_page, 'is_apply_button_available', return_value=True):
            
            result = await vacancy_handler.is_apply_button_available(mock_vacancy_locator)
            
            assert result is True
    
    async def test_get_applicable_vacancies(self, vacancy_handler):
        """Тест получения вакансий, на которые можно откликнуться"""
        mock_vacancies = [Mock(), Mock()]
        with patch.object(vacancy_handler.vacancy_page, 'get_applicable_vacancies', return_value=mock_vacancies):
            
            vacancies = await vacancy_handler.get_applicable_vacancies()
            
            assert vacancies == mock_vacancies
    
    async def test_get_vacancy_info(self, vacancy_handler):
        """Тест получения информации о вакансии"""
        mock_vacancy_locator = Mock()
        expected_title = "Python Developer"
        expected_id = "12345"
        
        with patch.object(vacancy_handler.vacancy_page, 'get_vacancy_info', 
                         return_value=(expected_title, expected_id)):
            
            title, vacancy_id = await vacancy_handler.get_vacancy_info(mock_vacancy_locator)
            
            assert title == expected_title
            assert vacancy_id == expected_id
    
    async def test_wait_for_vacancies_loaded(self, vacancy_handler):
        """Тест ожидания загрузки вакансий"""
        timeout = 30000
        with patch.object(vacancy_handler.vacancy_page, 'wait_for_vacancies_loaded', return_value=True):

            result = await vacancy_handler.wait_for_vacancies_loaded(timeout)

            assert result is True