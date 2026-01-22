"""
Модуль отправки откликов на вакансии
"""
import asyncio
import random
from typing import Protocol


class LocatorProtocol(Protocol):
    """Протокол для локатора Playwright"""
    async def click(self, selector: str) -> None: ...
    async def wait_for_selector(self, selector: str, **kwargs) -> None: ...
    def locator(self, selector: str): ...
    async def inner_text(self) -> str: ...
    async def get_attribute(self, name: str) -> str: ...


class ApplicationSender:
    """Класс для отправки откликов на вакансии"""

    def __init__(self, config, logger):
        """
        Инициализация класса отправки откликов
        
        :param config: Объект конфигурации
        :param logger: Объект логгера
        """
        self.config = config
        self.logger = logger

    async def click_apply_button(self, vacancy: LocatorProtocol) -> None:
        """
        Клик по кнопке отклика на вакансию
        
        :param vacancy: Локатор вакансии
        """
        self.logger.debug("Клик по кнопке отклика")
        await vacancy.click("[data-qa='apply-button']")

    async def wait_for_application_result(self, vacancy: LocatorProtocol) -> str:
        """
        Ожидание результата отклика
        
        :param vacancy: Локатор вакансии
        :return: Статус результата отклика ("Успешно", "Ошибка")
        """
        try:
            # Ожидаем появления элемента, сигнализирующего об успешном отклике
            await vacancy.wait_for_selector("[data-qa='success-message']", timeout=self.config.TIMEOUT)
            return "Успешно"
        except Exception as e:
            self.logger.error(f"Ошибка при ожидании результата отклика: {e}")
            return "Ошибка"

    async def log_application_result(self, vacancy_title: str, vacancy_id: str, result: str) -> None:
        """
        Логирование результата отклика
        
        :param vacancy_title: Название вакансии
        :param vacancy_id: ID вакансии
        :param result: Результат отклика
        """
        self.logger.info(f"Отклик на вакансию '{vacancy_title}' (ID: {vacancy_id}) завершен со статусом: {result}")

    async def apply_to_vacancy(self, vacancy: LocatorProtocol) -> str:
        """
        Полный цикл отклика на вакансию
        
        :param vacancy: Локатор вакансии
        :return: Результат отклика
        """
        # Получаем информацию о вакансии
        title_element = vacancy.locator("[data-qa='vacancy-title']")
        vacancy_title = await title_element.inner_text()
        
        id_element = vacancy.locator("[data-qa='vacancy-id']")
        vacancy_id = await id_element.get_attribute("data-id")
        
        self.logger.info(f"Отправка отклика на вакансию '{vacancy_title}' (ID: {vacancy_id})")
        
        # Клик по кнопке отклика
        await self.click_apply_button(vacancy)
        
        # Ожидание результата
        result = await self.wait_for_application_result(vacancy)
        
        # Логирование результата
        await self.log_application_result(vacancy_title, vacancy_id, result)
        
        # Добавляем паузу между откликами для имитации человеческого поведения
        pause_duration = random.uniform(1.5, 4)
        self.logger.debug(f"Пауза {pause_duration:.2f} секунд между откликами")
        await asyncio.sleep(pause_duration)
        
        return result