import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

# Создаём корневой логгер
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)

# Удалим дублирующиеся обработчики, если они есть
if logger.hasHandlers():
    logger.handlers.clear()

# Консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Файл
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
file_handler = logging.FileHandler(os.path.join(log_dir, 'app2.log'))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)