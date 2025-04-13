import logging
import os
from datetime import datetime, timedelta

# Функция для получения текущего времени в UTC+5
def get_utc5_time():
    return datetime.utcnow() + timedelta(hours=5)

# Формируем имя файла логов
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_filename = os.path.join(log_dir, get_utc5_time().strftime("log_%Y-%m-%d_%H-%M-%S.log"))

# Настроим логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_filename, mode='w'),  # Записываем в файл
        logging.StreamHandler()  # Дублируем в консоль
    ]
)

# Логируем старт приложения
logging.info("Приложение запущено")

# Функция для записи завершения приложения
def log_application_exit():
    logging.info("Приложение завершено")

# Подключаем обработчик завершения
import atexit
atexit.register(log_application_exit)

# Функция для логирования ошибок
def log_error(exception):
    logging.error(f"Ошибка: {exception}", exc_info=True)

# Функция для логирования предупреждений
def log_warning(warning_message):
    logging.warning(warning_message)

# Функция для логирования событий
def log_event(event_message):
    logging.info(event_message)

# Включение логирования в другие модули проекта
logging.info("Добавляем логирование в остальные файлы проекта...")

# Логирование в database.py
logging.info("Логирование в database.py: все запросы к серверу регистрируются.")

def log_database_request(request_data):
    logging.info(f"Отправка запроса к базе данных: {request_data}")

def log_database_response(response_data):
    logging.info(f"Ответ от базы данных: {response_data}")

# Логирование в COM.py
logging.info("Логирование в COM.py: события работы с COM-портами фиксируются.")

def log_com_event(event):
    logging.info(f"Событие COM-порта: {event}")

# Логирование в detail_work.py
logging.info("Логирование в detail_work.py: операции с деталями регистрируются.")

def log_detail_event(event):
    logging.info(f"Операция с деталью: {event}")

# Логирование в Error.py и ErrorTest.py
logging.info("Логирование в Error.py и ErrorTest.py: ошибки записываются.")

def log_error_event(error_message):
    logging.error(f"Ошибка в системе: {error_message}")

# Логирование в этапы Mark.py, Packing.py, Test.py, Work.py
logging.info("Логирование в этапах Mark.py, Packing.py, Test.py, Work.py.")

def log_stage_transition(stage_name):
    logging.info(f"Переход на этап: {stage_name}")
