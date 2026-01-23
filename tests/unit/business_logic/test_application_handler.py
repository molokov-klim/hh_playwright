"""
Тесты для обработчика откликов
"""
import pytest
from unittest.mock import AsyncMock, Mock, patch
from src.business_logic.application_handler import ApplicationHandler
from src.config import Config


@pytest.mark.asyncio
class TestApplicationHandler:
    """Тесты для ApplicationHandler"""
    
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
    def application_handler(self, mock_page, mock_config, mock_logger):
        """Создание экземпляра ApplicationHandler для тестов"""
        return ApplicationHandler(mock_page, mock_config, mock_logger)
    
    async def test_click_apply_button(self, application_handler):
        """Тест клика по кнопке отклика"""
        mock_vacancy_locator = Mock()
        with patch.object(application_handler.vacancy_page, 'click_apply_button', return_value=True):
            
            result = await application_handler.click_apply_button(mock_vacancy_locator)
            
            assert result is True
    
    async def test_wait_for_application_result(self, application_handler):
        """Тест ожидания результата отклика"""
        timeout = 30000
        expected_result = "Успешно"
        
        with patch.object(application_handler.vacancy_page, 'wait_for_application_result', 
                         return_value=expected_result):
            
            result = await application_handler.wait_for_application_result(timeout)
            
            assert result == expected_result
    
    async def test_fill_cover_letter(self, application_handler):
        """Тест заполнения сопроводительного письма"""
        cover_letter = "Тестовое сопроводительное письмо"
        with patch.object(application_handler.application_page, 'fill_cover_letter', return_value=True):
            
            result = await application_handler.fill_cover_letter(cover_letter)
            
            assert result is True
    
    async def test_click_send_response(self, application_handler):
        """Тест клика по кнопке отправки отклика"""
        with patch.object(application_handler.application_page, 'click_send_response', return_value=True):
            
            result = await application_handler.click_send_response()
            
            assert result is True
    
    async def test_wait_for_response_result(self, application_handler):
        """Тест ожидания результата отправки отклика"""
        timeout = 30000
        expected_result = "Успешно"
        
        with patch.object(application_handler.application_page, 'wait_for_response_result', 
                         return_value=expected_result):
            
            result = await application_handler.wait_for_response_result(timeout)
            
            assert result == expected_result
    
    async def test_log_application_result(self, application_handler):
        """Тест логирования результата отклика"""
        vacancy_title = "Python Developer"
        vacancy_id = "12345"
        result = "Успешно"
        
        # Просто проверим, что метод вызывается без ошибок
        await application_handler.log_application_result(vacancy_title, vacancy_id, result)
        
        # Проверим, что логгер был вызван, если он существует
        if application_handler.logger:
            application_handler.logger.info.assert_called()
    
    async def test_apply_to_vacancy_success(self, application_handler):
        """Тест полного цикла отклика на вакансию"""
        mock_vacancy_locator = Mock()
        cover_letter = "Тестовое сопроводительное письмо"
        expected_result = "Успешно"
        
        # Мок для всех необходимых методов
        with patch.object(application_handler.vacancy_page, 'get_vacancy_info', 
                         return_value=("Python Developer", "12345")), \
             patch.object(application_handler, 'click_apply_button', return_value=True), \
             patch.object(application_handler, 'fill_cover_letter', return_value=True), \
             patch.object(application_handler, 'click_send_response', return_value=True), \
             patch.object(application_handler, 'wait_for_response_result', return_value=expected_result), \
             patch.object(application_handler, 'log_application_result'):
            
            result = await application_handler.apply_to_vacancy(mock_vacancy_locator, cover_letter)
            
            assert result == expected_result