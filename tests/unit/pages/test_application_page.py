"""
Тесты для Page Object страницы откликов
"""
import pytest
from unittest.mock import AsyncMock, Mock
from src.pages.application_page import ApplicationPage
from src.config import Config


@pytest.mark.asyncio
class TestApplicationPage:
    """Тесты для ApplicationPage"""
    
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
        page.wait_for_timeout = AsyncMock()
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
    def application_page(self, mock_page, mock_config, mock_logger):
        """Создание экземпляра ApplicationPage для тестов"""
        return ApplicationPage(mock_page, mock_config, mock_logger)
    
    async def test_fill_cover_letter_success(self, application_page, mock_page):
        """Тест успешного заполнения сопроводительного письма"""
        cover_letter = "Тестовое сопроводительное письмо"
        
        # Мок для успешного заполнения
        mock_page.wait_for_selector = AsyncMock()
        mock_page.fill = AsyncMock()
        
        result = await application_page.fill_cover_letter(cover_letter)
        
        assert result is True
    
    async def test_click_send_response_success(self, application_page, mock_page):
        """Тест успешного клика по кнопке отправки отклика"""
        # Мок для успешного клика
        mock_page.wait_for_selector = AsyncMock()
        mock_page.click = AsyncMock()
        
        result = await application_page.click_send_response()
        
        assert result is True
    
    async def test_wait_for_response_result_success(self, application_page, mock_page):
        """Тест ожидания результата отправки отклика - успех"""
        timeout = 30000
        
        # Мок для успешного ожидания
        mock_page.wait_for_selector = AsyncMock()
        
        result = await application_page.wait_for_response_result(timeout)
        
        assert result == "Успешно"
    
    async def test_wait_for_response_result_error(self, application_page, mock_page):
        """Тест ожидания результата отправки отклика - ошибка"""
        timeout = 100  # короткий таймаут для теста

        # Мок для ожидания с исключением (ошибка)
        mock_page.wait_for_selector = AsyncMock(side_effect=Exception())
        mock_page.wait_for_timeout = AsyncMock()

        result = await application_page.wait_for_response_result(timeout)

        # В текущей реализации при ошибках возвращается "Ошибка" или "Таймаут"
        assert result in ["Ошибка", "Таймаут"]
    
    async def test_wait_for_response_result_timeout(self, application_page, mock_page):
        """Тест ожидания результата отправки отклика - таймаут"""
        timeout = 100  # короткий таймаут для теста
        
        # Мок для ожидания с исключением (таймаут)
        mock_page.wait_for_selector = AsyncMock(side_effect=Exception())
        mock_page.wait_for_timeout = AsyncMock()
        
        result = await application_page.wait_for_response_result(timeout)
        
        assert result in ["Ошибка", "Таймаут"]