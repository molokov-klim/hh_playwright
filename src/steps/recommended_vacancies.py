from src.step import Step
from src.logger import logger


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
        await self.page.get_by_role('link', name='Резюме и профиль').click()

        # Клик по кнопке "вакансии"
        logger.info("Клик по кнопке 'вакансии'")
        await self.page.get_by_role('button', name='вакансии').click()

        logger.info("Шаг перехода в рекомендованные вакансии завершен")