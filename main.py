import asyncio

from src.hh_bot import HHBot
from src.logger import logger
from src.steps.hh_auth import HHAuthStep
from src.steps.move_to_recommended_vacancies import MoveToRecommendedVacanciesStep


async def main():
    logger.info("Запуск HHBot")
    # Создаем бота и добавляем шаги
    bot = HHBot()
    bot.add_step(HHAuthStep(None))  # session будет передан позже
    bot.add_step(MoveToRecommendedVacanciesStep(None))  # session будет передан позже

    # Запускаем выполнение всех шагов
    await bot.run()
    logger.info("Завершение работы HHBot")


if __name__ == "__main__":
    asyncio.run(main())
