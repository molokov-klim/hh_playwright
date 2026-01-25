from src.logger import logger
from src.step import Step


class RecommendedVacanciesStep(Step):
    """
    Шаг для перехода в рекомендованные вакансии
    """

    def __init__(self, session):
        # Вызываем родительский конструктор, передавая session
        super().__init__(session)

    async def execute(self):
        """
        Выполнение шага перехода в рекомендованные вакансии
        """
        logger.info("Начало выполнения шага перехода в рекомендованные вакансии")

        if not self.page:
            error_msg = "Не удалось получить страницу"
            logger.error(error_msg)
            raise Exception(error_msg)

        # Клик по ссылке "Резюме и профиль"
        logger.info("Клик по ссылке 'Резюме и профиль'")
        await self.page.get_by_role("link", name="Резюме и профиль").click()

        # Прокрутка до кнопки "вакансии" и клик по ней
        logger.info("Прокрутка до кнопки 'вакансии'")
        vacancies_button = self.page.get_by_role("button", name="вакансии")
        await vacancies_button.scroll_into_view_if_needed()
        logger.info("Клик по кнопке 'вакансии'")
        await vacancies_button.click()

        logger.info("Шаг перехода в рекомендованные вакансии завершен")
