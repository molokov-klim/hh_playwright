"""
Тесты для основного сценария
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch
from src.steps.main_workflow import MainWorkflow
from src.config import Config


@pytest.mark.asyncio
class TestMainWorkflow:
    """Тесты для MainWorkflow"""
    
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
    def main_workflow(self, mock_page, mock_config, mock_logger):
        """Создание экземпляра MainWorkflow для тестов"""
        return MainWorkflow(mock_page, mock_config, mock_logger)
    
    async def test_run_full_workflow_success(self, main_workflow):
        """Тест успешного выполнения полного сценария"""
        cover_letter = "Тестовое сопроводительное письмо"
        
        with patch.object(main_workflow.auth_steps, 'login_to_hh', return_value=True), \
             patch.object(main_workflow.resume_steps, 'navigate_to_my_resumes', return_value=True), \
             patch.object(main_workflow.resume_steps, 'select_first_resume', return_value=True), \
             patch.object(main_workflow.resume_steps, 'go_to_recommended_vacancies', return_value=True), \
             patch.object(main_workflow.vacancy_steps, 'wait_for_vacancies_loaded', return_value=True), \
             patch.object(main_workflow.vacancy_steps, 'get_applicable_vacancies', return_value=[Mock(), Mock()]), \
             patch.object(main_workflow.application_steps, 'apply_to_vacancy', return_value="Успешно"):
            
            result = await main_workflow.run_full_workflow(cover_letter)
            
            assert result is True
    
    async def test_run_full_workflow_auth_failure(self, main_workflow):
        """Тест неудачной авторизации в полном сценарии"""
        cover_letter = "Тестовое сопроводительное письмо"
        
        with patch.object(main_workflow.auth_steps, 'login_to_hh', return_value=False):
            
            result = await main_workflow.run_full_workflow(cover_letter)
            
            assert result is False
    
    async def test_run_full_workflow_navigate_to_resumes_failure(self, main_workflow):
        """Тест неудачного перехода к резюме в полном сценарии"""
        cover_letter = "Тестовое сопроводительное письмо"
        
        with patch.object(main_workflow.auth_steps, 'login_to_hh', return_value=True), \
             patch.object(main_workflow.resume_steps, 'navigate_to_my_resumes', return_value=False):
            
            result = await main_workflow.run_full_workflow(cover_letter)
            
            assert result is False
    
    async def test_run_full_workflow_no_applicable_vacancies(self, main_workflow):
        """Тест случая, когда нет подходящих вакансий"""
        cover_letter = "Тестовое сопроводительное письмо"
        
        with patch.object(main_workflow.auth_steps, 'login_to_hh', return_value=True), \
             patch.object(main_workflow.resume_steps, 'navigate_to_my_resumes', return_value=True), \
             patch.object(main_workflow.resume_steps, 'select_first_resume', return_value=True), \
             patch.object(main_workflow.resume_steps, 'go_to_recommended_vacancies', return_value=True), \
             patch.object(main_workflow.vacancy_steps, 'wait_for_vacancies_loaded', return_value=True), \
             patch.object(main_workflow.vacancy_steps, 'get_applicable_vacancies', return_value=[]):
            
            result = await main_workflow.run_full_workflow(cover_letter)
            
            # Должно вернуть True, потому что отсутствие вакансий - это не ошибка
            assert result is True
    
    async def test_run_full_workflow_exception_handling(self, main_workflow):
        """Тест обработки исключения в полном сценарии"""
        cover_letter = "Тестовое сопроводительное письмо"
        
        with patch.object(main_workflow.auth_steps, 'login_to_hh', side_effect=Exception("Test error")):
            
            result = await main_workflow.run_full_workflow(cover_letter)
            
            assert result is False