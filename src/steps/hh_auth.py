from src.step import Step
from src.config import Config


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
        if not self.page:
            raise Exception("Не удалось получить страницу")

        # Переход на сайт Химки
        await self.page.goto(Config.HIMKI_URL)

        # Выбор города
        await self.page.get_by_role("button", name="Химки (Московская область)").click()
        await self.page.get_by_role("radio", name="Москва").nth(1).check()

        # Переход на основной сайт hh.ru
        await self.page.goto(f"{Config.BASE_URL}?customDomain=1&overRideDomainAreaId=1")

        # Клик по кнопке "Войти"
        await self.page.get_by_role("link", name="Войти").click()
        await self.page.get_by_role("button", name="Войти").click()

        # Ввод номера телефона
        await self.page.get_by_role("textbox").nth(1).fill(Config.PHONE_NUMBER)
        await self.page.get_by_role("button", name="Дальше").click()

        # Интерактивный ввод SMS-кода
        sms_code = input("Введите SMS-код: ")

        # Заполнение поля ввода кода
        await self.page.get_by_role("textbox", name="Введите код").fill(sms_code)

        # Завершение авторизации (при необходимости можно добавить дополнительные действия)

        # Ждем несколько секунд перед закрытием браузера
        await self.page.wait_for_timeout(5000)


if __name__ == "__main__":
    # Для запуска HHAuthStep напрямую нужно создать сессию
    import asyncio
    from src.hh_session import HHSession
    from src.config import Config

    async def main():
        async with HHSession().create_session(headless=Config.HEADLESS) as session:
            auth_step = HHAuthStep(session)
            await auth_step.execute()

    asyncio.run(main())
