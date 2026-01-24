"""
Скрипт для отладки диалога выбора региона на HH.ru
"""
import asyncio
import os
from playwright.async_api import async_playwright


async def debug_region_dialog():
    """Отладка диалога выбора региона"""
    # Устанавливаем HEADLESS в False, чтобы видеть браузер
    os.environ['HEADLESS'] = 'false'
    
    async with async_playwright() as p:
        # Запускаем браузер в headed режиме
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Переходим на главную страницу HH.ru
        await page.goto("https://hh.ru")
        
        # Ждем немного, чтобы страница загрузилась
        await page.wait_for_timeout(5000)
        
        # Проверяем, есть ли диалог выбора региона
        # Пробуем разные возможные селекторы для диалога региона
        possible_selectors = [
            "text=Ваш регион",
            "text=регион",
            ".HH-RegionSelector-Hint",
            "[data-qa='region-selector-hint']",
            ".supernova-region-selector",
            "[data-qa='suggest-region-input']",
            ".supernova-current-region",
            "text=Химки",
            "text=Московская область"
        ]
        
        print("Проверяем наличие элементов, связанных с регионом:")
        for selector in possible_selectors:
            try:
                count = await page.locator(selector).count()
                if count > 0:
                    print(f"  Найден элемент по селектору '{selector}': {count} шт.")
                    
                    # Проверяем, видим ли он
                    is_visible = await page.locator(selector).is_visible()
                    print(f"    Видимость: {is_visible}")
                    
                    # Получаем текст элемента
                    text = await page.locator(selector).text_content()
                    print(f"    Текст: {text}")
                    
                else:
                    print(f"  Элемент по селектору '{selector}' не найден")
            except Exception as e:
                print(f"  Ошибка при проверке селектора '{selector}': {e}")
        
        # Делаем скриншот для дальнейшего анализа
        await page.screenshot(path="debug_region_dialog.png", full_page=True)
        print("\nСкриншот сохранен как debug_region_dialog.png")
        
        # Выводим HTML-код страницы для анализа
        content = await page.content()
        with open("debug_region_dialog.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("HTML-код страницы сохранен как debug_region_dialog.html")
        
        print("\nБраузер открыт. Нажмите Ctrl+C для завершения.")
        # Ждем, пока пользователь не завершит выполнение
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nЗавершение работы...")
            await browser.close()


if __name__ == "__main__":
    asyncio.run(debug_region_dialog())