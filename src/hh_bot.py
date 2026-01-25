from typing import List
from src.hh_session import HHSession
from src.config import Config
from src.step import Step
from src.logger import logger


class HHBot:
    """
    Основной класс бота для взаимодействия с hh.ru
    """

    def __init__(self):
        self.session = HHSession()
        self.steps: List[Step] = []
        logger.info("HHBot инициализирован")

    def add_step(self, step: Step):
        """
        Добавление шага к боту
        """
        self.steps.append(step)
        logger.debug(f"Шаг {type(step).__name__} добавлен к боту")

    async def run(self):
        """
        Запуск выполнения всех шагов с общей сессией
        После выполнения всех шагов сессия и браузер будут закрыты
        """
        logger.info("Запуск выполнения всех шагов")
        async with self.session.create_session(headless=Config.HEADLESS) as session:
            logger.info("Сессия браузера создана")
            for i, step in enumerate(self.steps, 1):
                logger.info(f"Выполнение шага {i}: {type(step).__name__}")
                # Обновляем сессию для каждого шага
                step.update_session(session)
                await step.execute()
                logger.info(f"Шаг {i}: {type(step).__name__} завершен")
        logger.info("Все шаги выполнены, сессия закрыта")