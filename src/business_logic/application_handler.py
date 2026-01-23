"""
Обработчик отправки откликов на hh.ru
"""
import asyncio
import random
from ..pages.vacancy_page import VacancyPage
from ..pages.application_page import ApplicationPage


class ApplicationHandler:
    """Класс для обработки отправки откликов на hh.ru"""
    
    def __init__(self, page, config, logger):
        """
        Инициализация обработчика откликов
        
        :param page: Страница Playwright
        :param config: Объект конфигурации
        :param logger: Объект логгера
        """
        self.page = page
        self.config = config
        self.logger = logger
        self.vacancy_page = VacancyPage(page, config, logger)
        self.application_page = ApplicationPage(page, config, logger)
    
    async def click_apply_button(self, vacancy_locator) -> bool:
        """
        Клик по кнопке отклика на вакансию
        
        :param vacancy_locator: Локатор вакансии
        :return: True, если клик выполнен успешно
        """
        if self.logger:
            self.logger.debug("Клик по кнопке отклика")
        
        return await self.vacancy_page.click_apply_button(vacancy_locator)
    
    async def wait_for_application_result(self, timeout: int = 30000) -> str:
        """
        Ожидание результата отклика
        
        :param timeout: Таймаут ожидания в миллисекундах
        :return: Статус результата отклика ("Успешно", "Ошибка", "Таймаут")
        """
        if self.logger:
            self.logger.debug("Ожидание результата отклика")
        
        return await self.vacancy_page.wait_for_application_result(timeout)
    
    async def fill_cover_letter(self, cover_letter: str) -> bool:
        """
        Заполнение сопроводительного письма
        
        :param cover_letter: Текст сопроводительного письма
        :return: True, если заполнение выполнено успешно
        """
        if self.logger:
            self.logger.debug("Заполнение сопроводительного письма")
        
        return await self.application_page.fill_cover_letter(cover_letter)
    
    async def click_send_response(self) -> bool:
        """
        Клик по кнопке отправки отклика
        
        :return: True, если клик выполнен успешно
        """
        if self.logger:
            self.logger.debug("Клик по кнопке отправки отклика")
        
        return await self.application_page.click_send_response()
    
    async def wait_for_response_result(self, timeout: int = 30000) -> str:
        """
        Ожидание результата отправки отклика
        
        :param timeout: Таймаут ожидания в миллисекундах
        :return: Статус результата ("Успешно", "Ошибка", "Таймаут")
        """
        if self.logger:
            self.logger.debug("Ожидание результата отправки отклика")
        
        return await self.application_page.wait_for_response_result(timeout)
    
    async def log_application_result(self, vacancy_title: str, vacancy_id: str, result: str) -> None:
        """
        Логирование результата отклика
        
        :param vacancy_title: Название вакансии
        :param vacancy_id: ID вакансии
        :param result: Результат отклика
        """
        if self.logger:
            self.logger.info(f"Отклик на вакансию '{vacancy_title}' (ID: {vacancy_id}) завершен со статусом: {result}")
    
    async def apply_to_vacancy(self, vacancy_locator, cover_letter: str = "") -> str:
        """
        Полный цикл отклика на вакансию
        
        :param vacancy_locator: Локатор вакансии
        :param cover_letter: Текст сопроводительного письма (опционально)
        :return: Результат отклика
        """
        # Получаем информацию о вакансии
        vacancy_title, vacancy_id = await self.vacancy_page.get_vacancy_info(vacancy_locator)
        
        if self.logger:
            self.logger.info(f"Отправка отклика на вакансию '{vacancy_title}' (ID: {vacancy_id})")
        
        # Клик по кнопке отклика
        if not await self.click_apply_button(vacancy_locator):
            result = "Ошибка"
            await self.log_application_result(vacancy_title, vacancy_id, result)
            return result
        
        # Если есть сопроводительное письмо, заполняем его
        if cover_letter:
            if not await self.fill_cover_letter(cover_letter):
                if self.logger:
                    self.logger.warning(f"Не удалось заполнить сопроводительное письмо для вакансии {vacancy_title}")
        
        # Клик по кнопке отправки
        if not await self.click_send_response():
            result = "Ошибка"
            await self.log_application_result(vacancy_title, vacancy_id, result)
            return result
        
        # Ожидание результата
        result = await self.wait_for_response_result()
        
        # Логирование результата
        await self.log_application_result(vacancy_title, vacancy_id, result)
        
        # Добавляем паузу между откликами для имитации человеческого поведения
        pause_duration = random.uniform(1.5, 4)
        if self.logger:
            self.logger.debug(f"Пауза {pause_duration:.2f} секунд между откликами")
        await asyncio.sleep(pause_duration)
        
        return result