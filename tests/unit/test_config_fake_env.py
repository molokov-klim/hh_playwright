"""
Тесты для проверки чтения переменной FAKE из .env файла
"""
import os
import tempfile
from src.config import get_config_from_env


def test_fake_variable_reads_from_env_file():
    """Тест, что переменная FAKE корректно читается из .env файла"""
    # Создаем временный .env файл
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.env') as f:
        env_content = """HH_LOGIN=test@example.com
HH_PASSWORD=password123
FAKE=true"""
        f.write(env_content)
        temp_env_path = f.name

    # Сохраняем оригинальные переменные окружения
    original_environ = dict(os.environ)

    try:
        # Очищаем переменные окружения
        os.environ.clear()

        # Загружаем переменные из временного файла
        with open(temp_env_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    # Удаляем кавычки из значения, если они есть
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]

                    os.environ[key] = value

        # Получаем конфигурацию
        config = get_config_from_env()

        # Проверяем, что переменная FAKE установлена в True
        assert config.FAKE is True

    finally:
        # Восстанавливаем оригинальные переменные окружения
        os.environ.clear()
        os.environ.update(original_environ)

        # Удаляем временный файл
        os.unlink(temp_env_path)


def test_fake_variable_false_by_default():
    """Тест, что переменная FAKE по умолчанию равна False"""
    # Создаем временный .env файл без переменной FAKE
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.env') as f:
        env_content = """HH_LOGIN=test@example.com
HH_PASSWORD=password123"""
        f.write(env_content)
        temp_env_path = f.name

    # Сохраняем оригинальные переменные окружения
    original_environ = dict(os.environ)

    try:
        # Очищаем переменные окружения
        os.environ.clear()

        # Загружаем переменные из временного файла
        with open(temp_env_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    # Удаляем кавычки из значения, если они есть
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]

                    os.environ[key] = value

        # Получаем конфигурацию
        config = get_config_from_env()

        # Проверяем, что переменная FAKE установлена в False по умолчанию
        assert config.FAKE is False

    finally:
        # Восстанавливаем оригинальные переменные окружения
        os.environ.clear()
        os.environ.update(original_environ)

        # Удаляем временный файл
        os.unlink(temp_env_path)


def test_fake_variable_various_values():
    """Тест, что переменная FAKE корректно обрабатывает различные значения"""
    test_cases = [
        ("true", True),
        ("True", True),
        ("1", True),
        ("yes", True),
        ("on", True),
        ("false", False),
        ("False", False),
        ("0", False),
        ("no", False),
        ("off", False),
        ("", False),
    ]

    for fake_value, expected in test_cases:
        # Создаем временный .env файл
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.env') as f:
            env_content = f"""HH_LOGIN=test@example.com
HH_PASSWORD=password123
FAKE={fake_value}"""
            f.write(env_content)
            temp_env_path = f.name

        # Сохраняем оригинальные переменные окружения
        original_environ = dict(os.environ)

        try:
            # Очищаем переменные окружения
            os.environ.clear()

            # Загружаем переменные из временного файла
            with open(temp_env_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()

                        # Удаляем кавычки из значения, если они есть
                        if (value.startswith('"') and value.endswith('"')) or \
                           (value.startswith("'") and value.endswith("'")):
                            value = value[1:-1]

                        os.environ[key] = value

            # Получаем конфигурацию
            config = get_config_from_env()

            # Проверяем, что переменная FAKE установлена правильно
            assert config.FAKE is expected, f"Для значения FAKE='{fake_value}' ожидалось {expected}, получено {config.FAKE}"

        finally:
            # Восстанавливаем оригинальные переменные окружения
            os.environ.clear()
            os.environ.update(original_environ)

            # Удаляем временный файл
            os.unlink(temp_env_path)