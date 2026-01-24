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

    async def handle_region_dialog(self) -> bool:
        """
        Обработка диалогового окна выбора региона

        :return: True, если диалог успешно обработан или не найден
        """
        if self.logger:
            self.logger.info("Проверка наличия диалога выбора региона")

        try:
            # Проверяем наличие диалогового окна с регионом
            # Используем более общие селекторы, которые могут работать с разными вариантами текста
            region_dialog_selectors = [
                "text=Ваш регион",
                "text=регион",
                ".HH-RegionSelector-Hint",
                "[data-qa='region-selector-hint']",
                ".supernova-region-selector",
                "[data-qa='suggest-region-input']"
            ]

            dialog_found = False
            for selector in region_dialog_selectors:
                try:
                    element = self.page.locator(selector)
                    if await element.count() > 0:
                        if self.logger:
                            self.logger.info(f"Найден элемент диалога региона: {selector}")

                        # Проверяем, что элемент видим
                        if await element.is_visible():
                            dialog_found = True
                            break
                except:
                    continue  # Продолжаем поиск с другим селектором

            if dialog_found:
                if self.logger:
                    self.logger.info("Найдено диалоговое окно выбора региона")

                # Ищем кнопку "Нет, другой" или "Изменить регион" или "Другой регион"
                change_region_selectors = [
                    "text=Нет, другой",
                    "text=Изменить регион",
                    "text=Другой регион",
                    "text=Сменить регион",
                    ".HH-RegionSelector-ChangeButton",
                    "[data-qa='region-selector-change-button']"
                ]

                change_button_found = False
                for selector in change_region_selectors:
                    try:
                        button = self.page.locator(selector)
                        if await button.count() > 0 and await button.is_visible():
                            await button.click()
                            if self.logger:
                                self.logger.info(f"Нажата кнопка изменения региона: {selector}")
                            change_button_found = True
                            break
                    except:
                        continue

                if not change_button_found:
                    if self.logger:
                        self.logger.warning("Не найдена кнопка изменения региона")
                    return True  # Продолжаем выполнение, даже если не нашли кнопку

                # Ждем появление поля ввода региона
                region_input_selectors = [
                    "[data-qa='suggest-region-input']",
                    ".HH-SuggestRegion-Input",
                    "input[type='text'][placeholder*='регион' i]",
                    "input[placeholder*='регион' i]"
                ]

                input_found = False
                for selector in region_input_selectors:
                    try:
                        await self.page.wait_for_selector(selector, timeout=5000)
                        region_input = self.page.locator(selector)
                        if await region_input.is_visible():
                            # Вводим "Москва" в поле
                            await region_input.fill("Москва")

                            # Ждем появления списка с вариантами
                            await self.page.wait_for_timeout(1000)

                            # Выбираем "Москва" из выпадающего списка
                            moscow_option_selectors = [
                                "text=Москва",
                                "[data-qa*='moscow' i]",
                                ".HH-SuggestRegion-Option:has-text('Москва')",
                                "[data-qa='area-suggestion-1']"  # Moscow area ID is usually 1
                            ]

                            option_found = False
                            for option_selector in moscow_option_selectors:
                                try:
                                    option = self.page.locator(option_selector)
                                    if await option.count() > 0 and await option.is_visible():
                                        await option.click()
                                        if self.logger:
                                            self.logger.info(f"Выбран регион 'Москва' через селектор: {option_selector}")
                                        option_found = True
                                        break
                                except:
                                    continue

                            if not option_found:
                                if self.logger:
                                    self.logger.warning("Не найден элемент 'Москва' в списке регионов")
                                return True  # Продолжаем выполнение, даже если не нашли элемент

                            input_found = True
                            break
                    except:
                        continue

                if not input_found:
                    if self.logger:
                        self.logger.warning("Не найдено поле ввода региона")
                    return True  # Продолжаем выполнение, даже если не нашли поле

                # Ждем исчезновения диалогового окна (обычно происходит автоматически после выбора)
                try:
                    # Ждем, пока диалог региона исчезнет
                    await self.page.wait_for_selector(".supernova-region-selector, .HH-RegionSelector-Hint", state="detached", timeout=10000)
                    if self.logger:
                        self.logger.info("Диалоговое окно выбора региона закрыто")
                except:
                    if self.logger:
                        self.logger.info("Диалоговое окно выбора региона, возможно, уже закрыто")

                # Проверяем, что на странице отображается "Москва" как регион
                await self.page.wait_for_timeout(2000)  # Даем время для обновления

                # Проверяем, что регион сменился на Москву
                current_location_selectors = [
                    "text=Москва",
                    "[data-qa*='current-region' i]",
                    ".supernova-current-region",
                    ".HH-CurrentRegion"
                ]

                location_found = False
                for selector in current_location_selectors:
                    try:
                        current_location = self.page.locator(selector)
                        if await current_location.count() > 0:
                            if self.logger:
                                self.logger.info("Регион успешно изменен на Москву")
                            location_found = True
                            break
                    except:
                        continue

                if not location_found:
                    if self.logger:
                        self.logger.warning("Не удалось подтвердить, что регион изменен на Москву")

                return True
            else:
                if self.logger:
                    self.logger.info("Диалоговое окно выбора региона не найдено")
                return True

        except Exception as e:
            if self.logger:
                self.logger.error(f"Ошибка при обработке диалога выбора региона: {e}")
            # Ошибка обработки диалога не должна останавливать выполнение сценария
            return True

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
            # Шаг 0: Обработка диалога выбора региона
            if not await self.handle_region_dialog():
                if self.logger:
                    self.logger.warning("Не удалось обработать диалог выбора региона")
                # Продолжаем выполнение, даже если диалог не был обработан

            if self.logger:
                self.logger.info("Диалог выбора региона обработан")
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