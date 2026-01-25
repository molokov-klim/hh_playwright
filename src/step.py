from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.hh_session import HHSession


class Step(ABC):
    """
    Базовый класс для всех шагов
    """

    def __init__(self, session: 'HHSession'):
        self.session = session
        self.page = session.get_page() if session else None

    def update_session(self, session: 'HHSession'):
        """
        Обновление сессии для шага
        """
        self.session = session
        self.page = session.get_page()

    @abstractmethod
    async def execute(self):
        """
        Метод для выполнения шага
        """
        pass