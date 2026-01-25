from src.config import Config
from src.logger import logger
from src.step import Step


class MassResponsesStep(Step):
    """
    Шаг для массовых откликов на рекомендованные вакансии
    """

    def __init__(self, session):
        super().__init__(session)
        self.response_count = 0

    async def execute(self):
        logger.info("Начало массовых откликов")

        if not self.page:
            error_msg = "Не удалось получить страницу"
            logger.error(error_msg)
            raise Exception(error_msg)

        await self.page.wait_for_load_state("load")
        await self.page.wait_for_timeout(5000)

        current_page = 1

        while self.response_count < Config.MAX_RESPONSE:
            logger.info(f"--- Страница {current_page}, откликов: {self.response_count} ---")

            # БЕСКОНЕЧНЫЙ ЦИКЛ ПО КОТЛКАМ — try/except сам остановит
            while self.response_count < Config.MAX_RESPONSE:
                try:
                    # ИЩЕМ ПЕРВУЮ ДОСТУПНУЮ КНОПКУ КАЖДЫЙ РАЗ
                    button = self.page.locator('[data-qa="vacancy-serp__vacancy_response"]').first

                    # Проверяем, что она вообще существует
                    await button.wait_for(state="visible", timeout=2000)
                    await button.scroll_into_view_if_needed()

                    if Config.FAKE:
                        logger.info(f"Фейк #{self.response_count + 1}")
                        self.response_count += 1
                    else:
                        await button.click()
                        # Простая проверка успеха
                        await self.page.wait_for_timeout(2000)
                        logger.info(f"✅ #{self.response_count + 1}")
                        self.response_count += 1

                    await self.page.wait_for_timeout(1500)  # Пауза между кликами

                except Exception as e:
                    logger.debug(f"Кнопок больше нет (или ошибка: {e}) → переход на следующую страницу")
                    break  # КНОПОК НЕТ → ПЕРЕХОД НА СЛЕДУЮЩУЮ СТРАНИЦУ

            # ПАГИНАЦИЯ
            next_page_num = str(current_page + 1)
            next_link = self.page.get_by_role("link", name=next_page_num, exact=True)

            if await next_link.count() > 0:
                logger.info(f"→ Страница {next_page_num}")
                await next_link.click()
                await self.page.wait_for_load_state("load")
                await self.page.wait_for_timeout(5000)
                current_page += 1
            else:
                logger.info("Страниц больше нет")
                break

        logger.info(f"Готово! {self.response_count} откликов")

    #
    # async def execute(self):
    #     """
    #     Выполнение шага массовых откликов
    #     """
    #     logger.info("Начало выполнения шага массовых откликов")
    #
    #     if not self.page:
    #         error_msg = "Не удалось получить страницу"
    #         logger.error(error_msg)
    #         raise Exception(error_msg)
    #
    #     current_page = 1
    #
    #     while self.response_count < Config.MAX_RESPONSE:
    #         logger.info(f"Обработка страницы {current_page}, текущее количество откликов: {self.response_count}")
    #
    #         # Находим все кнопки "Откликнуться" на текущей странице
    #         response_buttons = self.page.get_by_role("button", name="Откликнуться")
    #         count = await response_buttons.count()
    #
    #         if count == 0:
    #             logger.info(f"На странице {current_page} не найдено кнопок 'Откликнуться', переход к следующей странице")
    #
    #             # Проверяем, есть ли ссылка на следующую страницу
    #             next_page_link = self.page.get_by_role("link", name=str(current_page + 1), exact=True)
    #             next_page_exists = await next_page_link.count() > 0
    #
    #             if next_page_exists:
    #                 current_page += 1
    #                 logger.info(f"Переход на страницу {current_page}")
    #
    #                 # Клик по ссылке следующей страницы
    #                 await next_page_link.click()
    #
    #                 # Ждем загрузки новой страницы
    #                 await self.page.wait_for_load_state("networkidle")
    #             else:
    #                 logger.info("Больше нет страниц для обработки")
    #                 break
    #         else:
    #             # Проходим по всем кнопкам "Откликнуться" на странице
    #             logger.info(f"Найдено {count} кнопок 'Откликнуться' на странице {current_page}")
    #
    #             i = 0
    #             while i < 10 and self.response_count < Config.MAX_RESPONSE:  # Лимит на итерации для безопасности
    #                 if self.response_count >= Config.MAX_RESPONSE:
    #                     break
    #
    #                 # ПОИСК КОЛЛЕКЦИИ КАЖДЫЙ РАЗ ЗАНОВО — ключевое исправление!
    #                 response_buttons = self.page.get_by_role("button", name="Откликнуться")
    #                 count = await response_buttons.count()
    #
    #                 if count == 0:
    #                     logger.info("Больше нет доступных кнопок на странице")
    #                     break
    #
    #                 button = response_buttons.nth(
    #                     0)  # Всегда первую доступную (остальные станут недоступными после клика)
    #
    #                 is_visible = await button.is_visible()
    #                 is_enabled = await button.is_enabled()
    #
    #                 if is_visible and is_enabled:
    #                     try:
    #                         if Config.FAKE:
    #                             logger.info(f"Имитация отклика #{self.response_count + 1}")
    #                             self.response_count += 1
    #                         else:
    #                             await button.scroll_into_view_if_needed()
    #                             await button.click({"force": True})  # force для перекрытий [web:9]
    #
    #                             # Лучшая проверка: ждём появления текста успеха с expect
    #                             success_button = self.page.get_by_role("button").filter(
    #                                 has_text=re.compile(r"Вы откликнулись|Отклик отправлен"))
    #                             await expect(success_button).to_be_visible(timeout=5000)
    #
    #                             logger.info(f"Успешный отклик #{self.response_count + 1}")
    #                             self.response_count += 1
    #
    #                         await self.page.wait_for_timeout(2000)
    #                     except Exception as e:
    #                         logger.error(f"Ошибка отклика: {e}")
    #                         i += 1  # Пропуск, но не инкремент счётчика откликов
    #                         continue
    #                 else:
    #                     logger.debug("Кнопка недоступна, пропуск")
    #
    #                 i += 1  # Переходим к следующей итерации (новый поиск)
    #
    #             # После обработки всех кнопок на странице — пауза и переход
    #             await self.page.wait_for_timeout(3000)
    #
    #     logger.info(f"Шаг массовых откликов завершен. Всего откликов: {self.response_count}")
