from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from src.logger import logger

if TYPE_CHECKING:
    from src.hh_session import HHSession


class Step(ABC):
    """
    Базовый класс для всех шагов
    """

    def __init__(self, session: 'HHSession'):
        self.session = session
        self.page = session.get_page() if session else None
        logger.debug(f"Инициализирован шаг: {self.__class__.__name__}")

    def update_session(self, session: 'HHSession'):
        """
        Обновление сессии для шага
        """
        self.session = session
        self.page = session.get_page()
        logger.debug(f"Сессия обновлена для шага: {self.__class__.__name__}")

    @abstractmethod
    async def execute(self):
        """
        Метод для выполнения шага
        """
        pass