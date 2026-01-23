"""
Модуль обработки вакансий
"""
import warnings
from typing import Protocol, List


# Предупреждение об устаревшем модуле
warnings.warn(
    "Модуль src.vacancy_processor устарел. Используйте src.steps.vacancy_steps.VacancySteps или "
    "src.business_logic.vacancy_handler.VacancyHandler вместо этого модуля.",
    DeprecationWarning,
    stacklevel=2
)


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
    """Класс для обработки вакансий (устаревший)"""

    def __init__(self, config, logger):
        """
        Инициализация класса обработки вакансий

        :param config: Объект конфигурации
        :param logger: Объект логгера
        """
        warnings.warn(
            "VacancyProcessor устарел. Используйте VacancyHandler или VacancySteps вместо этого класса.",
            DeprecationWarning,
            stacklevel=2
        )
        self.config = config
        self.logger = logger

    async def find_vacancy_cards(self, page: PageProtocol) -> int:
        """
        Поиск всех карточек вакансий на странице

        :param page: Страница Playwright
        :return: Количество найденных карточек вакансий
        """
        warnings.warn(
            "find_vacancy_cards устарел. Используйте VacancyHandler.get_vacancy_locators "
            "для получения локаторов вакансий.",
            DeprecationWarning,
            stacklevel=2
        )
        # Используем новый подход
        from src.business_logic.vacancy_handler import VacancyHandler
        vacancy_handler = VacancyHandler(page, self.config, self.logger)
        locators = await vacancy_handler.get_vacancy_locators()
        return len(locators)

    async def is_apply_button_available(self, vacancy: LocatorProtocol) -> bool:
        """
        Проверка доступности кнопки отклика для вакансии

        :param vacancy: Локатор вакансии
        :return: True, если кнопка отклика доступна
        """
        warnings.warn(
            "is_apply_button_available устарел. Используйте VacancyHandler.is_apply_button_available.",
            DeprecationWarning,
            stacklevel=2
        )
        # Используем новый подход
        from src.business_logic.vacancy_handler import VacancyHandler
        # В новой архитектуре этот метод принимает page, а не отдельный локатор
        # поэтому мы не можем напрямую использовать VacancyHandler здесь
        # вместо этого, реализуем логику напрямую
        apply_button_locator = vacancy.locator("[data-qa='apply-button']")
        button_count = await apply_button_locator.count()
        return button_count > 0

    async def filter_applicable_vacancies(self, vacancies: List[LocatorProtocol]) -> List[LocatorProtocol]:
        """
        Фильтрация вакансий по возможности отклика

        :param vacancies: Список локаторов вакансий
        :return: Список вакансий, на которые можно откликнуться
        """
        warnings.warn(
            "filter_applicable_vacancies устарел. Используйте VacancyHandler.get_applicable_vacancies.",
            DeprecationWarning,
            stacklevel=2
        )
        # Используем новый подход
        from src.business_logic.vacancy_handler import VacancyHandler
        # В новой архитектуре этот метод работает с текущей страницей, а не с переданным списком
        # поэтому мы реализуем логику напрямую
        applicable_vacancies = []

        for vacancy in vacancies:
            if await self.is_apply_button_available(vacancy):
                applicable_vacancies.append(vacancy)

        if self.logger:
            self.logger.info(f"Найдено {len(applicable_vacancies)} вакансий, на которые можно откликнуться")
        return applicable_vacancies

    async def get_vacancy_info(self, vacancy: LocatorProtocol) -> tuple[str, str]:
        """
        Получение информации о вакансии

        :param vacancy: Локатор вакансии
        :return: Кортеж с названием и ID вакансии
        """
        warnings.warn(
            "get_vacancy_info устарел. Используйте VacancyHandler.get_vacancy_info.",
            DeprecationWarning,
            stacklevel=2
        )
        # Используем новый подход
        from src.business_logic.vacancy_handler import VacancyHandler
        # В новой архитектуре этот метод работает с текущей страницей, а не с переданным локатором
        # поэтому мы реализуем логику напрямую
        title_element = vacancy.locator("[data-qa='vacancy-title']")
        title = await title_element.inner_text()

        id_element = vacancy.locator("[data-qa='vacancy-id']")
        vacancy_id = await id_element.get_attribute("data-id") or ""

        return title.strip(), vacancy_id.strip()