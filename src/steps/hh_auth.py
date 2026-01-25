from src.config import Config
from src.logger import logger
from src.step import Step


class HHAuthStep(Step):
    """
    Шаг авторизации на hh.ru с интерактивным вводом SMS-кода
    """

    def __init__(self, session):
        # Вызываем родительский конструктор, передавая session
        # Если session None, родительский класс корректно обработает это
        super().__init__(session)

    async def execute(self):
        """
        Выполнение шага авторизации
        """
        logger.info("Начало выполнения шага авторизации")

        if not self.page:
            error_msg = "Не удалось получить страницу"
            logger.error(error_msg)
            raise Exception(error_msg)

        # Переход на сайт Химки
        logger.info("Переход на сайт Химки")
        await self.page.goto(Config.HIMKI_URL)

        # Выбор города
        logger.info("Выбор города Москва")
        await self.page.get_by_role("button", name="Химки (Московская область)").click()
        logger.info("Выбор города Москва 1")
        await self.page.get_by_role("radio", name="Москва").nth(1).click()
        logger.info("Выбор города Москва 2")

        # Переход на основной сайт hh.ru
        logger.info("Переход на основной сайт hh.ru")
        await self.page.goto(f"{Config.BASE_URL}?customDomain=1&overRideDomainAreaId=1")

        # Клик по кнопке "Войти"
        logger.info("Клик по кнопке 'Войти'")
        await self.page.get_by_role("link", name="Войти").click()
        await self.page.get_by_role("button", name="Войти").click()

        # Ввод номера телефона
        logger.info("Ввод номера телефона")
        await self.page.get_by_role("textbox").nth(1).fill(Config.PHONE_NUMBER)
        await self.page.get_by_role("button", name="Дальше").click()

        # Интерактивный ввод SMS-кода
        logger.info("Ожидание ввода SMS-кода пользователем")
        sms_code = input("Введите SMS-код: ")
        logger.info("SMS-код получен от пользователя")

        # Заполнение поля ввода кода
        logger.info("Заполнение поля ввода кода")
        await self.page.get_by_role("textbox", name="Введите код").fill(sms_code)

        # Завершение авторизации (при необходимости можно добавить дополнительные действия)

        # Ждем несколько секунд перед закрытием браузера
        logger.info("Ожидание завершения авторизации")
        await self.page.wait_for_timeout(5000)

        logger.info("Шаг авторизации завершен")


if __name__ == "__main__":
    # Для запуска HHAuthStep напрямую нужно создать сессию
    import asyncio

    from src.config import Config
    from src.hh_session import HHSession
    from src.logger import logger

    async def main():
        logger.info("Запуск HHAuthStep напрямую")
        async with HHSession().create_session(headless=Config.HEADLESS) as session:
            auth_step = HHAuthStep(session)
            await auth_step.execute()
        logger.info("Завершение HHAuthStep")

    asyncio.run(main())
