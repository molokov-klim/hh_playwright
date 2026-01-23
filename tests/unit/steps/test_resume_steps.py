"""
Тесты для шагов работы с резюме
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch
from src.steps.resume_steps import ResumeSteps
from src.config import Config


@pytest.mark.asyncio
class TestResumeSteps:
    """Тесты для ResumeSteps"""
    
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
    def resume_steps(self, mock_page, mock_config, mock_logger):
        """Создание экземпляра ResumeSteps для тестов"""
        return ResumeSteps(mock_page, mock_config, mock_logger)
    
    async def test_navigate_to_my_resumes(self, resume_steps):
        """Тест перехода к моим резюме"""
        with patch.object(resume_steps.resume_handler, 'navigate_to_my_resumes', return_value=True):
            
            result = await resume_steps.navigate_to_my_resumes()
            
            assert result is True
    
    async def test_select_first_resume(self, resume_steps):
        """Тест выбора первого резюме"""
        with patch.object(resume_steps.resume_handler, 'select_first_resume', return_value=True):
            
            result = await resume_steps.select_first_resume()
            
            assert result is True
    
    async def test_select_resume_by_index(self, resume_steps):
        """Тест выбора резюме по индексу"""
        index = 0
        with patch.object(resume_steps.resume_handler, 'select_resume_by_index', return_value=True):
            
            result = await resume_steps.select_resume_by_index(index)
            
            assert result is True
    
    async def test_go_to_recommended_vacancies(self, resume_steps):
        """Тест перехода к рекомендуемым вакансиям"""
        with patch.object(resume_steps.resume_handler, 'go_to_recommended_vacancies', return_value=True):
            
            result = await resume_steps.go_to_recommended_vacancies()
            
            assert result is True
    
    async def test_wait_for_vacancies_loaded(self, resume_steps):
        """Тест ожидания загрузки вакансий"""
        timeout = 30000
        with patch.object(resume_steps.resume_handler, 'wait_for_vacancies_loaded', return_value=True):
            
            result = await resume_steps.wait_for_vacancies_loaded(timeout)
            
            assert result is True