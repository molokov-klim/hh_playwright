"""
Тесты для шагов отправки откликов
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch
from src.steps.application_steps import ApplicationSteps
from src.config import Config


@pytest.mark.asyncio
class TestApplicationSteps:
    """Тесты для ApplicationSteps"""
    
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
    def application_steps(self, mock_page, mock_config, mock_logger):
        """Создание экземпляра ApplicationSteps для тестов"""
        return ApplicationSteps(mock_page, mock_config, mock_logger)
    
    async def test_apply_to_vacancy(self, application_steps):
        """Тест отправки отклика на вакансию"""
        mock_vacancy_locator = Mock()
        cover_letter = "Тестовое сопроводительное письмо"
        expected_result = "Успешно"
        
        with patch.object(application_steps.application_handler, 'apply_to_vacancy', 
                         return_value=expected_result):
            
            result = await application_steps.apply_to_vacancy(mock_vacancy_locator, cover_letter)
            
            assert result == expected_result