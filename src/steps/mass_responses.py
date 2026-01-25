from src.step import Step
from src.config import Config
from src.logger import logger


class MassResponsesStep(Step):
    """
    Шаг для массовых откликов на рекомендованные вакансии
    """

    def __init__(self, session):
        super().__init__(session)
        self.response_count = 0

    async def execute(self):
        """
        Выполнение шага массовых откликов
        """
        logger.info("Начало выполнения шага массовых откликов")

        if not self.page:
            error_msg = "Не удалось получить страницу"
            logger.error(error_msg)
            raise Exception(error_msg)

        current_page = 1

        while self.response_count < Config.MAX_RESPONSE:
            logger.info(f"Обработка страницы {current_page}, текущее количество откликов: {self.response_count}")

            # Находим все кнопки "Откликнуться" на текущей странице
            response_buttons = self.page.get_by_role('button', name='Откликнуться')
            count = await response_buttons.count()

            if count == 0:
                logger.info(f"На странице {current_page} не найдено кнопок 'Откликнуться', переход к следующей странице")

                # Проверяем, есть ли ссылка на следующую страницу
                next_page_link = self.page.get_by_role('link', name=str(current_page + 1), exact=True)
                next_page_exists = await next_page_link.count() > 0

                if next_page_exists:
                    current_page += 1
                    logger.info(f"Переход на страницу {current_page}")

                    # Клик по ссылке следующей страницы
                    await next_page_link.click()

                    # Ждем загрузки новой страницы
                    await self.page.wait_for_load_state('networkidle')
                else:
                    logger.info("Больше нет страниц для обработки")
                    break
            else:
                logger.info(f"Найдено {count} кнопок 'Откликнуться' на странице {current_page}")

                # Проходим по всем кнопкам "Откликнуться" на странице
                for i in range(count):
                    if self.response_count >= Config.MAX_RESPONSE:
                        logger.info(f"Достигнуто максимальное количество откликов: {Config.MAX_RESPONSE}")
                        return

                    # Получаем кнопку по индексу
                    button = response_buttons.nth(i)

                    # Прокручиваем до кнопки
                    await button.scroll_into_view_if_needed()

                    # Проверяем, видима ли кнопка и доступна ли для клика
                    is_visible = await button.is_visible()
                    is_enabled = await button.is_enabled()

                    if is_visible and is_enabled:
                        try:
                            if Config.FAKE:
                                # Имитация отклика
                                logger.info(f"Имитация отклика на вакансию (фейковый режим), отклик #{self.response_count + 1}")
                                self.response_count += 1
                            else:
                                # Настоящий отклик
                                # Сохраняем исходный текст кнопки для проверки результата
                                original_text = await button.text_content()

                                await button.click()

                                # Ждем изменения текста кнопки на "Вы откликнулись"
                                try:
                                    # Ждем, пока текст кнопки изменится
                                    await self.page.wait_for_timeout(3000)  # Небольшая задержка для обработки

                                    # Проверяем, изменился ли текст кнопки на "Вы откликнулись"
                                    new_text = await button.text_content()
                                    if "Вы откликнулись" in new_text or "Отклик отправлен" in new_text:
                                        logger.info(f"Успешно откликнулись на вакансию #{self.response_count + 1}")
                                        self.response_count += 1
                                    else:
                                        logger.warning(f"Не удалось подтвердить отклик на вакансию #{self.response_count + 1}")
                                        # Продолжаем, даже если не смогли подтвердить отклик
                                        self.response_count += 1
                                except:
                                    logger.warning(f"Не удалось подтвердить отклик на вакансию #{self.response_count + 1}")
                                    # Продолжаем, даже если не смогли подтвердить отклик
                                    self.response_count += 1

                            # Ждем немного между откликами
                            await self.page.wait_for_timeout(2000)

                        except Exception as e:
                            logger.error(f"Ошибка при отклике на вакансию: {e}")
                            continue
                    else:
                        logger.debug(f"Кнопка {i} не видима или недоступна, пропускаем")

        logger.info(f"Шаг массовых откликов завершен. Всего откликов: {self.response_count}")