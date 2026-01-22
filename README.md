# hh_auto_responder - Автоматизация откликов на hh.ru

Скрипт для автоматизации массовых откликов на hh.ru. Авторизуется на сайте под вашим аккаунтом, переходит к рекомендациям по вашему резюме и отправляет отклики на все предложенные вакансии.

## Особенности

- Использование Playwright для автоматизации браузера
- Поддержка headless режима для работы в CI/CD
- Обход простых анти-бот проверок
- Логирование всех действий
- Обработка ошибок и создание скриншотов при проблемах
- Совместимость с GitHub Actions

## Требования

- Python 3.10+
- `uv` для управления зависимостями

## Установка и настройка

1. Клонируйте репозиторий:

```bash
git clone <URL_репозитория>
cd hh_playwright
```

2. Создайте виртуальное окружение и установите зависимости:

```bash
uv venv
source .venv/bin/activate  # На Linux/Mac
# или
.venv\Scripts\activate  # На Windows

uv pip install -r requirements.txt
```

3. Установите браузеры Playwright:

```bash
uv run playwright install chromium
```

4. Установите переменные окружения:

Создайте файл `.env` или используйте переменные окружения:

```bash
export HH_LOGIN=ваш_email_или_телефон
export HH_PASSWORD=ваш_пароль
```

## Запуск скрипта

Для локального запуска:

```bash
uv run python hh_auto_responder.py
```

Для запуска в headed режиме (для отладки):

```bash
# Измените значение HEADLESS в конфигурации на False
```

## Запуск тестов

Для запуска всех тестов:

```bash
uv run python -m pytest
```

Для запуска только юнит-тестов:

```bash
uv run python -m pytest tests/unit/
```

Для запуска только интеграционных тестов:

```bash
uv run python -m pytest tests/integration/
```

Для получения детального вывода:

```bash
uv run python -m pytest -v
```

## Настройка GitHub Actions

В репозитории уже настроены следующие workflows:

1. `test.yml` - запускает тесты при пуше и пулл-реквестах
2. `run-hh-bot.yml` - запускает основной скрипт, может быть запущен вручную или по расписанию

Для настройки GitHub Actions:

1. В настройках репозитория создайте следующие секреты:
   - `HH_LOGIN` - ваш логин на hh.ru
   - `HH_PASSWORD` - ваш пароль на hh.ru

2. Запустите workflow вручную через вкладку Actions

## Архитектура

Проект состоит из следующих модулей:

- `src/config.py` - управление конфигурацией и переменными окружения
- `src/browser_config.py` - настройка опций браузера
- `src/auth.py` - авторизация на hh.ru
- `src/navigation.py` - навигация по сайту
- `src/vacancy_processor.py` - обработка вакансий
- `src/application_sender.py` - отправка откликов
- `src/error_handler.py` - обработка ошибок
- `src/logger.py` - логирование

## Безопасность

- Логин и пароль передаются через переменные окружения/секреты GitHub
- Никакие учетные данные не хранятся в коде
- Используется HTTPS для всех соединений

## Вклад в проект

1. Создайте fork репозитория
2. Создайте ветку для вашей функции: `git checkout -b feature/NewFeature`
3. Зафиксируйте изменения: `git commit -m 'Add some NewFeature'`
4. Отправьте ветку: `git push origin feature/NewFeature`
5. Создайте Pull Request
