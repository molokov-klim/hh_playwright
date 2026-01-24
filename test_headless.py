"""
Тестовый скрипт для проверки режима HEADLESS
"""
import os
import asyncio
from playwright.async_api import async_playwright
from src.config import get_config_from_env
from src.browser_config import get_browser_options


async def test_headless_mode():
    """Тестирование режима HEADLESS"""
    # Установим переменную окружения HEADLESS в false для теста
    os.environ['HEADLESS'] = 'false'
    
    # Загрузим конфигурацию
    config = get_config_from_env()
    print(f"Значение HEADLESS из конфигурации: {config.HEADLESS}")
    
    # Получим опции браузера
    browser_options = get_browser_options(config.HEADLESS)
    print(f"Значение headless в опциях браузера: {browser_options['headless']}")
    
    # Запустим браузер
    async with async_playwright() as p:
        browser = await p.chromium.launch(**browser_options)
        page = await browser.new_page()
        
        print("Браузер запущен. Нажмите Ctrl+C для завершения.")
        
        # Подождем немного, чтобы можно было увидеть браузер
        await asyncio.sleep(10)
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(test_headless_mode())