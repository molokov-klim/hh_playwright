import sys
from loguru import logger

# Удаляем стандартный обработчик
logger.remove()

# Добавляем новый обработчик с цветным выводом в консоль
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>",
    level="DEBUG"
)

# Добавляем обработчик для записи логов в файл
logger.add(
    "logs/hh_bot_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="7 days",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO"
)

__all__ = ["logger"]