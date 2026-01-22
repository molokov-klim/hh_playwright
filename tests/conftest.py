"""
Общие фикстуры для тестов
"""
import pytest
from unittest.mock import Mock, MagicMock


@pytest.fixture
def mock_page():
    """Мок для объекта страницы Playwright"""
    page = Mock()
    page.goto = Mock()
    page.locator = Mock()
    page.click = Mock()
    page.fill = Mock()
    page.wait_for_load_state = Mock()
    page.wait_for_selector = Mock()
    page.wait_for_url = Mock()
    return page


@pytest.fixture
def mock_browser():
    """Мок для объекта браузера Playwright"""
    browser = Mock()
    browser.new_context = Mock()
    return browser


@pytest.fixture
def mock_context():
    """Мок для контекста браузера Playwright"""
    context = Mock()
    context.new_page = Mock()
    return context


@pytest.fixture
def mock_resume_data():
    """Мок для данных резюме"""
    return {
        "id": "123456",
        "title": "Software Developer",
        "url": "https://hh.ru/applicant/resumes/123456"
    }


@pytest.fixture
def mock_vacancy_data():
    """Мок для данных вакансии"""
    return [
        {
            "id": "vac1",
            "title": "Python Developer",
            "apply_button_available": True
        },
        {
            "id": "vac2", 
            "title": "Frontend Developer",
            "apply_button_available": False  # Требует заполнения анкеты
        }
    ]