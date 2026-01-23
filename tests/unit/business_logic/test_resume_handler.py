"""
Тесты для обработчика резюме
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch
from src.business_logic.resume_handler import ResumeHandler
from src.config import Config


@pytest.mark.asyncio
class TestResumeHandler:
    """Тесты для ResumeHandler"""
    
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
    def resume_handler(self, mock_page, mock_config, mock_logger):
        """Создание экземпляра ResumeHandler для тестов"""
        return ResumeHandler(mock_page, mock_config, mock_logger)
    
    async def test_navigate_to_my_resumes_success(self, resume_handler, mock_page):
        """Тест успешного перехода к моим резюме"""
        # Мок для успешного перехода
        mock_page.goto = AsyncMock()

        result = await resume_handler.navigate_to_my_resumes()

        assert result is True
        mock_page.goto.assert_called_once_with("https://hh.ru/applicant/resumes")
    
    async def test_select_first_resume_success(self, resume_handler):
        """Тест успешного выбора первого резюме"""
        with patch.object(resume_handler.resume_page, 'select_first_resume', return_value=True):
            
            result = await resume_handler.select_first_resume()
            
            assert result is True
    
    async def test_select_resume_by_index_success(self, resume_handler):
        """Тест успешного выбора резюме по индексу"""
        index = 0
        with patch.object(resume_handler.resume_page, 'select_resume_by_index', return_value=True):
            
            result = await resume_handler.select_resume_by_index(index)
            
            assert result is True
    
    async def test_go_to_recommended_vacancies_success(self, resume_handler):
        """Тест успешного перехода к рекомендуемым вакансиям"""
        with patch.object(resume_handler.resume_page, 'go_to_recommended_vacancies', return_value=True):
            
            result = await resume_handler.go_to_recommended_vacancies()
            
            assert result is True
    
    async def test_wait_for_vacancies_loaded_success(self, resume_handler):
        """Тест успешного ожидания загрузки вакансий"""
        timeout = 30000
        with patch.object(resume_handler.resume_page, 'wait_for_vacancies_loaded', return_value=True):
            
            result = await resume_handler.wait_for_vacancies_loaded(timeout)
            
            assert result is True
    
    async def test_get_vacancy_count(self, resume_handler):
        """Тест получения количества вакансий"""
        with patch.object(resume_handler.resume_page, 'get_vacancy_count', return_value=5):
            
            count = await resume_handler.get_vacancy_count()
            
            assert count == 5