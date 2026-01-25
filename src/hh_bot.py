from typing import List
from src.hh_session import HHSession
from src.config import Config
from src.step import Step


class HHBot:
    """
    Основной класс бота для взаимодействия с hh.ru
    """

    def __init__(self):
        self.session = HHSession()
        self.steps: List[Step] = []

    def add_step(self, step: Step):
        """
        Добавление шага к боту
        """
        self.steps.append(step)

    async def run(self):
        """
        Запуск выполнения всех шагов с общей сессией
        """
        async with self.session.create_session(headless=Config.HEADLESS) as session:
            for step in self.steps:
                # Обновляем сессию для каждого шага
                step.update_session(session)
                await step.execute()