import asyncio
from src.hh_bot import HHBot
from src.steps.hh_auth import HHAuthStep


async def main():
    # Создаем бота и добавляем шаги
    bot = HHBot()
    bot.add_step(HHAuthStep(None))  # session будет передан позже

    # Запускаем выполнение всех шагов
    await bot.run()


if __name__ == '__main__':
    asyncio.run(main())
