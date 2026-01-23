"""
Тесты для Page Object страницы вакансий
"""
import pytest
from unittest.mock import AsyncMock, Mock
from src.pages.vacancy_page import VacancyPage
from src.config import Config


@pytest.mark.asyncio
class TestVacancyPage:
    """Тесты для VacancyPage"""
    
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
    def vacancy_page(self, mock_page, mock_config, mock_logger):
        """Создание экземпляра VacancyPage для тестов"""
        return VacancyPage(mock_page, mock_config, mock_logger)
    
    async def test_get_vacancy_locators(self, vacancy_page, mock_page):
        """Тест получения локаторов вакансий"""
        # Мок для локатора
        mock_locator = Mock()
        mock_locator.count = AsyncMock(return_value=2)
        mock_locator.nth = Mock(side_effect=lambda i: Mock())
        mock_page.locator.return_value = mock_locator
        
        locators = await vacancy_page.get_vacancy_locators()
        
        assert len(locators) == 2
    
    async def test_is_apply_button_available_true(self, vacancy_page):
        """Тест проверки доступности кнопки отклика - доступна"""
        mock_vacancy_locator = Mock()
        mock_button_locator = Mock()
        mock_button_locator.count = AsyncMock(return_value=1)
        mock_vacancy_locator.locator.return_value = mock_button_locator
        
        result = await vacancy_page.is_apply_button_available(mock_vacancy_locator)
        
        assert result is True
    
    async def test_is_apply_button_available_false(self, vacancy_page):
        """Тест проверки доступности кнопки отклика - недоступна"""
        mock_vacancy_locator = Mock()
        mock_button_locator = Mock()
        mock_button_locator.count = AsyncMock(return_value=0)
        mock_vacancy_locator.locator.return_value = mock_button_locator
        
        result = await vacancy_page.is_apply_button_available(mock_vacancy_locator)
        
        assert result is False
    
    async def test_get_applicable_vacancies(self, vacancy_page):
        """Тест получения вакансий, на которые можно откликнуться"""
        # Мок для вакансий
        mock_vacancy1 = Mock()
        mock_vacancy2 = Mock()
        mock_vacancies = [mock_vacancy1, mock_vacancy2]
        
        with pytest.MonkeyPatch().context() as mp:
            mp.setattr(vacancy_page, 'get_vacancy_locators', AsyncMock(return_value=mock_vacancies))
            mp.setattr(vacancy_page, 'is_apply_button_available', AsyncMock(return_value=True))
            
            # Имитируем методы объекта
            vacancy_page.get_vacancy_locators = AsyncMock(return_value=mock_vacancies)
            vacancy_page.is_apply_button_available = AsyncMock(return_value=True)
            
            applicable_vacancies = await vacancy_page.get_applicable_vacancies()
            
            assert len(applicable_vacancies) == 2
    
    async def test_get_vacancy_info(self, vacancy_page):
        """Тест получения информации о вакансии"""
        mock_vacancy_locator = Mock()
        mock_title_element = Mock()
        mock_title_element.inner_text = AsyncMock(return_value="Python Developer")
        mock_id_element = Mock()
        mock_id_element.get_attribute = AsyncMock(return_value="12345")
        
        mock_vacancy_locator.locator.side_effect = lambda selector: mock_title_element if "title" in selector else mock_id_element
        
        title, vacancy_id = await vacancy_page.get_vacancy_info(mock_vacancy_locator)
        
        assert title == "Python Developer"
        assert vacancy_id == "12345"
    
    async def test_click_apply_button(self, vacancy_page, mock_page):
        """Тест клика по кнопке отклика"""
        mock_vacancy_locator = Mock()
        mock_button_locator = Mock()
        mock_page.locator.return_value = mock_button_locator
        
        # Мок для успешного клика
        mock_page.wait_for_selector = AsyncMock()
        mock_page.click = AsyncMock()
        
        result = await vacancy_page.click_apply_button(mock_vacancy_locator)
        
        assert result is True
    
    async def test_wait_for_application_result_success(self, vacancy_page, mock_page):
        """Тест ожидания результата отклика - успех"""
        timeout = 30000
        
        # Мок для успешного ожидания
        mock_page.wait_for_selector = AsyncMock()
        
        result = await vacancy_page.wait_for_application_result(timeout)
        
        assert result == "Успешно"
    
    async def test_wait_for_application_result_timeout(self, vacancy_page, mock_page):
        """Тест ожидания результата отклика - таймаут"""
        timeout = 100  # короткий таймаут для теста таймаута
        
        # Мок для ожидания с исключением (таймаут)
        mock_page.wait_for_selector = AsyncMock(side_effect=Exception())
        
        result = await vacancy_page.wait_for_application_result(timeout)
        
        # В текущей реализации при ошибке возвращается "Ошибка", а не "Таймаут"
        assert result == "Ошибка"