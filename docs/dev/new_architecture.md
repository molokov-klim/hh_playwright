# Документация по новой архитектуре hh_auto_responder

## Обзор архитектуры

Проект hh_auto_responder теперь следует архитектуре с тремя уровнями абстракции:

1. **UI уровень (Page Objects)** - взаимодействие с элементами интерфейса
2. **Бизнес-логика** - логика выполнения конкретных задач
3. **Шаги/Сценарии** - высокоуровневые операции

## Структура проекта

```
hh_playwright/
├── src/
│   ├── pages/                 # Page Objects (нижний уровень)
│   │   ├── __init__.py
│   │   ├── base_page.py       # Базовый класс для всех страниц
│   │   ├── auth_page.py       # Страница авторизации
│   │   ├── main_page.py       # Главная страница
│   │   ├── resume_page.py     # Страница резюме
│   │   ├── vacancy_page.py    # Страница вакансий
│   │   └── application_page.py # Страница отправки откликов
│   ├── business_logic/        # Бизнес-логика (средний уровень)
│   │   ├── __init__.py
│   │   ├── auth_handler.py    # Обработчик авторизации
│   │   ├── resume_handler.py  # Обработчик резюме
│   │   ├── vacancy_handler.py # Обработчик вакансий
│   │   ├── application_handler.py # Обработчик откликов
│   │   └── session_manager.py # Менеджер сессии
│   ├── steps/                 # Шаги (верхний уровень)
│   │   ├── __init__.py
│   │   ├── auth_steps.py      # Шаги авторизации
│   │   ├── resume_steps.py    # Шаги работы с резюме
│   │   ├── vacancy_steps.py   # Шаги работы с вакансиями
│   │   ├── application_steps.py # Шаги отправки откликов
│   │   └── main_workflow.py   # Основной сценарий
│   ├── config.py              # Конфигурация
│   ├── browser_config.py      # Настройки браузера
│   ├── logger.py              # Логирование
│   └── error_handler.py       # Обработка ошибок
├── hh_auto_responder.py       # Основной скрипт
└── ...
```

## Подробное описание уровней

### 1. UI уровень (Page Objects)

Каждый Page Object отвечает за взаимодействие с конкретной страницей сайта hh.ru:

- `base_page.py` - базовый класс с общими методами для всех страниц
- `auth_page.py` - методы для работы со страницей авторизации
- `main_page.py` - методы для работы с главной страницей
- `resume_page.py` - методы для работы со страницей резюме
- `vacancy_page.py` - методы для работы со страницей вакансий
- `application_page.py` - методы для работы со страницей отправки откликов

### 2. Бизнес-логика

Классы бизнес-логики используют Page Objects для выполнения конкретных задач:

- `auth_handler.py` - логика авторизации
- `resume_handler.py` - логика работы с резюме
- `vacancy_handler.py` - логика обработки вакансий
- `application_handler.py` - логика отправки откликов
- `session_manager.py` - управление сессией браузера

### 3. Шаги/Сценарии

Высокоуровневые классы, использующие бизнес-логику для выполнения сценариев:

- `auth_steps.py` - шаги авторизации
- `resume_steps.py` - шаги работы с резюме
- `vacancy_steps.py` - шаги работы с вакансиями
- `application_steps.py` - шаги отправки откликов
- `main_workflow.py` - основной сценарий работы

## Использование

### Для выполнения полного сценария:

```python
from src.business_logic.session_manager import SessionManager
from src.steps.main_workflow import MainWorkflow
from src.config import get_config_from_env
from src.logger import setup_logger

async def main():
    logger = setup_logger("hh_auto_responder")
    config = get_config_from_env()
    
    session_manager = SessionManager(config, logger)
    await session_manager.start_session()
    
    page = session_manager.get_page()
    main_workflow = MainWorkflow(page, config, logger)
    
    success = await main_workflow.run_full_workflow(cover_letter="Текст сопроводительного письма")
    
    await session_manager.end_session()
```

### Для выполнения отдельных шагов:

```python
# Авторизация
auth_steps = AuthSteps(page, config, logger)
await auth_steps.login_to_hh()

# Работа с резюме
resume_steps = ResumeSteps(page, config, logger)
await resume_steps.navigate_to_my_resumes()
await resume_steps.select_first_resume()
await resume_steps.go_to_recommended_vacancies()

# Работа с вакансиями
vacancy_steps = VacancySteps(page, config, logger)
await vacancy_steps.wait_for_vacancies_loaded()
applicable_vacancies = await vacancy_steps.get_applicable_vacancies()

# Отправка откликов
application_steps = ApplicationSteps(page, config, logger)
for vacancy in applicable_vacancies:
    result = await application_steps.apply_to_vacancy(vacancy, cover_letter="Текст сопроводительного письма")
```

## Устаревшие модули

Старые модули (`auth.py`, `navigation.py`, `vacancy_processor.py`, `application_sender.py`) помечены как устаревшие и содержат предупреждения о необходимости использования новых классов. Они по-прежнему работают, но используют внутренне новую архитектуру.

## Преимущества новой архитектуры

- Четкое разделение ответственности
- Легкость в тестировании
- Повторное использование кода
- Простота поддержки и расширения
- Лучшая читаемость кода