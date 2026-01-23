"""
Тесты для Page Object главной страницы
"""
import pytest
from unittest.mock import AsyncMock, Mock
from src.pages.main_page import MainPage
from src.config import Config


@pytest.mark.asyncio
class TestMainPage:
    """Тесты для MainPage"""
    
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
    def main_page(self, mock_page, mock_config, mock_logger):
        """Создание экземпляра MainPage для тестов"""
        return MainPage(mock_page, mock_config, mock_logger)
    
    async def test_navigate_to_my_resumes_success(self, main_page, mock_page):
        """Тест успешного перехода к моим резюме"""
        # Мок для успешного клика
        mock_page.wait_for_selector = AsyncMock()
        mock_page.click = AsyncMock()
        
        result = await main_page.navigate_to_my_resumes()
        
        assert result is True
    
    async def test_search_vacancies_success(self, main_page, mock_page):
        """Тест успешного поиска вакансий"""
        query = "Python developer"
        
        # Мок для успешного заполнения и клика
        mock_page.wait_for_selector = AsyncMock()
        mock_page.fill = AsyncMock()
        mock_page.click = AsyncMock()
        
        result = await main_page.search_vacancies(query)
        
        assert result is True