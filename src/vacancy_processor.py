"""
Модуль обработки вакансий
"""
from typing import Protocol, List


class PageProtocol(Protocol):
    """Протокол для страницы Playwright"""
    def locator(self, selector: str): ...
    async def wait_for_selector(self, selector: str, **kwargs) -> None: ...


class LocatorProtocol(Protocol):
    """Протокол для локатора Playwright"""
    async def count(self) -> int: ...
    async def inner_text(self) -> str: ...
    async def get_attribute(self, name: str) -> str: ...


class VacancyProcessor:
    """Класс для обработки вакансий"""

    def __init__(self, config, logger):
        """
        Инициализация класса обработки вакансий
        
        :param config: Объект конфигурации
        :param logger: Объект логгера
        """
        self.config = config
        self.logger = logger

    async def find_vacancy_cards(self, page: PageProtocol) -> int:
        """
        Поиск всех карточек вакансий на странице
        
        :param page: Страница Playwright
        :return: Количество найденных карточек вакансий
        """
        self.logger.debug("Поиск карточек вакансий")
        vacancy_locator = page.locator("[data-qa='vacancy']")
        count = await vacancy_locator.count()
        return count

    async def is_apply_button_available(self, vacancy: LocatorProtocol) -> bool:
        """
        Проверка доступности кнопки отклика для вакансии
        
        :param vacancy: Локатор вакансии
        :return: True, если кнопка отклика доступна
        """
        apply_button_locator = vacancy.locator("[data-qa='apply-button']")
        button_count = await apply_button_locator.count()
        return button_count > 0

    async def filter_applicable_vacancies(self, vacancies: List[LocatorProtocol]) -> List[LocatorProtocol]:
        """
        Фильтрация вакансий по возможности отклика
        
        :param vacancies: Список локаторов вакансий
        :return: Список вакансий, на которые можно откликнуться
        """
        self.logger.debug(f"Фильтрация {len(vacancies)} вакансий по возможности отклика")
        applicable_vacancies = []
        
        for vacancy in vacancies:
            if await self.is_apply_button_available(vacancy):
                applicable_vacancies.append(vacancy)
        
        self.logger.info(f"Найдено {len(applicable_vacancies)} вакансий, на которые можно откликнуться")
        return applicable_vacancies

    async def get_vacancy_info(self, vacancy: LocatorProtocol) -> tuple[str, str]:
        """
        Получение информации о вакансии
        
        :param vacancy: Локатор вакансии
        :return: Кортеж с названием и ID вакансии
        """
        title_element = vacancy.locator("[data-qa='vacancy-title']")
        title = await title_element.inner_text()
        
        id_element = vacancy.locator("[data-qa='vacancy-id']")
        vacancy_id = await id_element.get_attribute("data-id")
        
        return title, vacancy_id