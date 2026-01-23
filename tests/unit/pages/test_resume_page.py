"""
Тесты для Page Object страницы резюме
"""
import pytest
from unittest.mock import AsyncMock, Mock
from src.pages.resume_page import ResumePage
from src.config import Config


@pytest.mark.asyncio
class TestResumePage:
    """Тесты для ResumePage"""
    
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
    def resume_page(self, mock_page, mock_config, mock_logger):
        """Создание экземпляра ResumePage для тестов"""
        return ResumePage(mock_page, mock_config, mock_logger)
    
    async def test_select_first_resume_success(self, resume_page, mock_page):
        """Тест успешного выбора первого резюме"""
        # Мок для успешного клика
        mock_page.wait_for_selector = AsyncMock()
        mock_page.click = AsyncMock()
        
        result = await resume_page.select_first_resume()
        
        assert result is True
    
    async def test_select_resume_by_index_success(self, resume_page, mock_page):
        """Тест успешного выбора резюме по индексу"""
        index = 0
        
        # Мок для успешного клика
        mock_page.wait_for_selector = AsyncMock()
        mock_page.click = AsyncMock()
        
        result = await resume_page.select_resume_by_index(index)
        
        assert result is True
    
    async def test_go_to_recommended_vacancies_success(self, resume_page, mock_page):
        """Тест успешного перехода к рекомендуемым вакансиям"""
        # Мок для успешного клика
        mock_page.wait_for_selector = AsyncMock()
        mock_page.click = AsyncMock()
        
        result = await resume_page.go_to_recommended_vacancies()
        
        assert result is True
    
    async def test_wait_for_vacancies_loaded_success(self, resume_page, mock_page):
        """Тест успешного ожидания загрузки вакансий"""
        timeout = 30000
        
        # Мок для успешного ожидания
        mock_page.wait_for_selector = AsyncMock()
        
        result = await resume_page.wait_for_vacancies_loaded(timeout)
        
        assert result is True
    
    async def test_get_vacancy_count(self, resume_page, mock_page):
        """Тест получения количества вакансий"""
        # Мок для локатора
        mock_locator = Mock()
        mock_locator.count = AsyncMock(return_value=5)
        mock_page.locator.return_value = mock_locator
        
        count = await resume_page.get_vacancy_count()
        
        assert count == 5