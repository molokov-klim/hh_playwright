"""
Основной сценарий работы hh_auto_responder
"""
from ..steps.auth_steps import AuthSteps
from ..steps.resume_steps import ResumeSteps
from ..steps.vacancy_steps import VacancySteps
from ..steps.application_steps import ApplicationSteps
from ..decorators import async_log_info


class MainWorkflow:
    """Класс для основного сценария работы hh_auto_responder"""

    def __init__(self, page, config, logger):
        """
        Инициализация основного сценария

        :param page: Страница Playwright
        :param config: Объект конфигурации
        :param logger: Объект логгера
        """
        self.page = page
        self.config = config
        self.logger = logger

        # Инициализация всех шагов
        self.auth_steps = AuthSteps(page, config, logger)
        self.resume_steps = ResumeSteps(page, config, logger)
        self.vacancy_steps = VacancySteps(page, config, logger)
        self.application_steps = ApplicationSteps(page, config, logger)

    @async_log_info()
    async def run_full_workflow(self, cover_letter: str = "") -> tuple[bool, int, int]:
        """
        Запуск полного сценария работы

        :param cover_letter: Текст сопроводительного письма (опционально)
        :return: Кортеж (успех, количество успешных откликов, количество ошибок)
        """
        if self.logger:
            self.logger.info("Начало выполнения основного сценария")

        success_count = 0
        error_count = 0

        try:
            # Шаг 1: Авторизация
            if not await self.auth_steps.login_to_hh():
                if self.logger:
                    self.logger.error("Не удалось выполнить авторизацию")
                return False, success_count, error_count

            if self.logger:
                self.logger.info("Авторизация выполнена успешно")

            # Шаг 2: Навигация к разделу резюме
            if not await self.resume_steps.navigate_to_my_resumes():
                if self.logger:
                    self.logger.error("Не удалось перейти на страницу 'Мои резюме'")
                return False, success_count, error_count

            # Шаг 3: Выбор первого резюме
            if not await self.resume_steps.select_first_resume():
                if self.logger:
                    self.logger.error("Не удалось выбрать первое резюме")
                return False, success_count, error_count

            # Шаг 4: Переход к рекомендуемым вакансиям
            if not await self.resume_steps.go_to_recommended_vacancies():
                if self.logger:
                    self.logger.error("Не удалось перейти к рекомендуемым вакансиям")
                return False, success_count, error_count

            # Шаг 5: Ожидание загрузки вакансий
            if not await self.vacancy_steps.wait_for_vacancies_loaded():
                if self.logger:
                    self.logger.error("Не дождались загрузки вакансий")
                return False, success_count, error_count

            # Шаг 6: Получение вакансий, на которые можно откликнуться
            applicable_vacancies = await self.vacancy_steps.get_applicable_vacancies()
            if not applicable_vacancies:
                if self.logger:
                    self.logger.warning("Не найдено вакансий, на которые можно откликнуться")
                return True, success_count, error_count  # Не ошибка, просто нет подходящих вакансий

            if self.logger:
                self.logger.info(f"Найдено {len(applicable_vacancies)} вакансий, на которые можно откликнуться")

            # Шаг 7: Отправка откликов на все подходящие вакансии
            for i, vacancy in enumerate(applicable_vacancies):
                if self.logger:
                    self.logger.info(f"Отправка отклика {i+1} из {len(applicable_vacancies)}")

                result = await self.application_steps.apply_to_vacancy(vacancy, cover_letter)

                if self.logger:
                    self.logger.info(f"Результат отклика {i+1}: {result}")

                # Обновляем счетчики
                if result in ["Успешно", "Успешно (FAKE)"]:
                    success_count += 1
                else:
                    error_count += 1

            if self.logger:
                self.logger.info("Основной сценарий успешно завершен")

            return True, success_count, error_count

        except Exception as e:
            if self.logger:
                self.logger.error(f"Ошибка при выполнении основного сценария: {e}")
            error_count += 1
            return False, success_count, error_count