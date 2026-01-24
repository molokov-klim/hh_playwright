"""
Модуль с утилитами для работы со страницами Playwright
"""
import asyncio
from datetime import datetime
from pathlib import Path
from playwright.async_api import Page


async def save_page_source_on_error(page: Page, error_context: str = "") -> str:
    """
    Сохраняет исходник страницы в файл при ошибке взаимодействия с UI

    :param page: Объект страницы Playwright
    :param error_context: Контекст ошибки (например, название метода или шага)
    :return: Путь к файлу с исходником страницы
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # Миллисекунды
    filename = f"page_source_{timestamp}_{error_context.replace(' ', '_').replace('.', '_')}.html"
    filepath = Path("debug_pages") / filename

    # Создаем директорию, если она не существует
    filepath.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Получаем HTML-код страницы
        html_content = await page.content()

        # Сохраняем в файл
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)

        return str(filepath)
    except Exception as e:
        # Если не удалось получить исходник страницы, возвращаем сообщение об ошибке
        error_filepath = f"error_getting_page_source_{timestamp}.txt"
        with open(error_filepath, "w", encoding="utf-8") as f:
            f.write(f"Ошибка при получении исходника страницы: {e}")
        return error_filepath