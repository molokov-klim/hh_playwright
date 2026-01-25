import asyncio
from src.hh_bot import HHBot
from src.steps.hh_auth import HHAuthStep
from src.steps.recommended_vacancies import RecommendedVacanciesStep
from src.logger import logger


async def main():
    logger.info("Запуск HHBot")
    # Создаем бота и добавляем шаги
    bot = HHBot()
    bot.add_step(HHAuthStep(None))  # session будет передан позже
    bot.add_step(RecommendedVacanciesStep(None))  # session будет передан позже

    # Запускаем выполнение всех шагов
    await bot.run()
    logger.info("Завершение работы HHBot")


if __name__ == '__main__':
    asyncio.run(main())
