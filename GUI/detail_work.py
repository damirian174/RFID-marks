from database import database
from error_test import show_error_dialog
import config
from datetime import datetime, timedelta
import time
from logger import *
import threading
from PySide6.QtWidgets import QMessageBox, QLabel, QVBoxLayout, QPushButton, QDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
import os
import sys


# Функция для получения пути к иконке
def get_icon_path(image_name):
    if getattr(sys, 'frozen', False):
        # Если приложение запущено как .exe
        base_path = sys._MEIPASS
    else:
        # Если в режиме разработки
        base_path = os.path.abspath(".")
    
    # Формируем полный путь к изображению
    image_path = os.path.join(base_path, image_name)
    return image_path

# Определение функции log_warning, если её нет в logger
def log_warning(message):
    """Логирование предупреждений (если в logger.py нет такой функции)"""
    try:
        # Пробуем импортировать из logger
        from logger import log_warning as logger_warning
        logger_warning(message)
    except ImportError:
        # Если нет, используем log_event с префиксом ПРЕДУПРЕЖДЕНИЕ
        log_event(f"ПРЕДУПРЕЖДЕНИЕ: {message}")

mark_ui_instance = None
work_ui_instance = None
packing_ui_instance = None
test_ui_instance = None

data_detail = None

time_start = None 
time_end = None 
detail_work = False

time_stage = None

def GetTime():
    utc = datetime.utcnow()
    time_c = utc + timedelta(hours=5)
    
    date_part = time_c.strftime("%Y-%m-%d") 
    time_part = time_c.strftime("%H:%M:%S")
    
    return {'date': date_part, 'time': time_part}

def getUI(mark_ui, work_ui, packing_ui, test_ui):
    global mark_ui_instance, work_ui_instance, packing_ui_instance, test_ui_instance
    mark_ui_instance = mark_ui
    work_ui_instance = work_ui
    packing_ui_instance = packing_ui
    test_ui_instance = test_ui
    


def start_work(ser, response):
    global time_start
    global detail_work

    # Проверяем, не ведется ли уже работа над деталью
    if detail_work:
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Предупреждение")
        msg_box.setText("Уже ведется работа над деталью.\nЗавершите текущую работу перед началом новой.")
        msg_box.setFixedSize(550, 300)
        msg_box.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        
        # Установка иконки
        icon_path = get_icon_path("favicon.ico")
        msg_box.setWindowIcon(QIcon(icon_path))
        
        msg_box.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                border-radius: 15px;
                border: 2px solid #0056b3;
            }
            QLabel {
                color: #212529;
                font-size: 16px;
                line-height: 1.6;
                margin-bottom: 10px;
            }
            QLabel#title_label {
                color: #0056b3;
                font-size: 24px;
                font-weight: bold;
            }
            QLabel#desc_label {
                color: #495057;
                font-size: 16px;
                background-color: #e9ecef;
                padding: 15px;
                border-radius: 8px;
            }
            QPushButton {
                background-color: #0056b3;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 6px;
                font-size: 15px;
                font-weight: bold;
                min-width: 140px;
            }
            QPushButton:hover {
                background-color: #0069d9;
            }
            QPushButton:pressed {
                background-color: #004494;
            }
        """)
        
        # Создаем и настраиваем метки
        title_label = QLabel("Внимание!")
        title_label.setObjectName("title_label")
        title_label.setFont(QFont("Arial", 22, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        
        desc_label = QLabel("Уже ведется работа над деталью.\nЗавершите текущую работу перед началом новой.")
        desc_label.setObjectName("desc_label")
        desc_label.setFont(QFont("Arial", 16))
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        
        # Создаем макет
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
        
        # Добавляем виджеты в макет
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addStretch()
        
        # Создаем кнопку закрытия
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(msg_box.close)
        layout.addWidget(close_button, alignment=Qt.AlignCenter)
        
        msg_box.setLayout(layout)
        msg_box.exec()
        return
    
    detail_work = True
    config.work = True
    config.detail = ser
    
    utc_time = datetime.utcnow()
    utc_plus_5 = utc_time + timedelta(hours=5)
    time_start = utc_plus_5.strftime('%Y-%m-%d %H:%M:%S')
    global mark_ui_instance, work_ui_instance, packing_ui_instance, test_ui_instance
    
    # Логируем начало работы и текущее значение Name
    log_event(f"Начало работы над деталью. Текущее значение Name: '{config.Name}'")
    
    # Получаем имя и фамилию из переменной Name
    first_name = "Неизвестно"
    last_name = "Неизвестно"
    
    # Проверяем, установлено ли значение Name в конфиге
    if not hasattr(config, 'Name'):
        log_error("Переменная Name отсутствует в модуле config")
        config.Name = ""
    
    # Проверяем и обрабатываем переменную Name
    if config.Name and isinstance(config.Name, str) and " " in config.Name:
        name_parts = config.Name.split()
        if len(name_parts) >= 2:
            last_name, first_name = name_parts[0], name_parts[1]
            log_event(f"Используем части имени из Name: фамилия='{last_name}', имя='{first_name}'")
        else:
            log_error(f"Некорректный формат имени: '{config.Name}' (имеет пробел, но недостаточно частей)")
    else:
        log_error(f"Имя не установлено или некорректно: '{config.Name}'")
        
    log_event(f"Будет использоваться: фамилия='{last_name}', имя='{first_name}'")
    
    if response:
        try:
            log_event(f"Данные детали: {response}")
            # Проверяем, есть ли у нас валидные данные пользователя для обновления сессии
            if first_name != "Неизвестно" and last_name != "Неизвестно":
                if response['stage'] == 'Маркировка':
                    data = {"type": "updateSessionDescription", "name": first_name, "surname": last_name, "new_description": f"Сборка {response['serial_number']}"}
                    log_event(f"Запрос обновления описания сессии: {data}")
                    log_event(f"Состояние сессии: auth={config.auth}, session_on={config.session_on}")
                    result = database(data)
                    log_event(f"Ответ на обновление описания сессии: {result}")
                    if result and result.get('status') != 'ok':
                        log_error(f"Ошибка обновления описания сессии: {result}")
                    work_ui_instance.detail(response)
                elif response['stage'] == 'Сборка':
                    data = {"type": "updateSessionDescription", "name": first_name, "surname": last_name, "new_description": f"Тестирование {response['serial_number']}"}
                    log_event(f"Запрос обновления описания сессии: {data}")
                    log_event(f"Состояние сессии: auth={config.auth}, session_on={config.session_on}")
                    result = database(data)
                    log_event(f"Ответ на обновление описания сессии: {result}")
                    if result and result.get('status') != 'ok':
                        log_error(f"Ошибка обновления описания сессии: {result}")
                    test_ui_instance.detail(response)
                elif response['stage'] == 'Тестирование':
                    data = {"type": "updateSessionDescription", "name": first_name, "surname": last_name, "new_description": f"Упаковка {response['serial_number']}"}
                    log_event(f"Запрос обновления описания сессии: {data}")
                    log_event(f"Состояние сессии: auth={config.auth}, session_on={config.session_on}")
                    result = database(data)
                    log_event(f"Ответ на обновление описания сессии: {result}")
                    if result and result.get('status') != 'ok':
                        log_error(f"Ошибка обновления описания сессии: {result}")
                    packing_ui_instance.detail(response)
                else:
                    work_ui_instance.detail(response)
                    test_ui_instance.detail(response)
                    packing_ui_instance.detail(response)
                    mark_ui_instance.detail(response)
                    data = {"type": "updateSessionDescription", "name": first_name, "surname": last_name, "new_description": f"смотрит информацию о {response['serial_number']}"}
                    result = database(data)
                    log_event(f"Ответ на обновление описания сессии: {result}")
                    if result and result.get('status') != 'ok':
                        log_error(f"Ошибка обновления описания сессии: {result}")
            else:
                # Если у нас нет валидных данных пользователя, просто переходим к отображению без обновления сессии
                log_warning("Невозможно обновить описание сессии: нет данных авторизованного пользователя")
                if response['stage'] == 'Маркировка':
                    work_ui_instance.detail(response)
                elif response['stage'] == 'Сборка':
                    test_ui_instance.detail(response)
                elif response['stage'] == 'Тестирование':
                    packing_ui_instance.detail(response)
                else:
                    work_ui_instance.detail(response)
                    test_ui_instance.detail(response)
                    packing_ui_instance.detail(response)
                    mark_ui_instance.detail(response)

        except Exception as e:
            log_error(f"Ошибка при обновлении описания сессии: {e}")
    # work_ui_instance.running = True  # Это должно теперь работать
    # work_ui_instance.start_timer()

def pause_work():
    work_ui_instance.pause_timer()

def couintine_work():
    work_ui_instance.resume_timer()




def end_work():
    global detail_work
    global time_end 
    global data_detail
    global time_stage
    global time_start
    detail_work = False
    config.data = False
    config.work = False
    config.detail = None 
    time_end = GetTime()
    
    global mark_ui_instance, work_ui_instance, packing_ui_instance, test_ui_instance
    mark_ui_instance.detail(False)
    work_ui_instance.detail(False)
    packing_ui_instance.detail(False)
    test_ui_instance.detail(False)
    
    # Обновляем статус пользователя на "Отдых" после окончания работы
    try:
        # Получаем имя и фамилию из переменной Name
        first_name = "Неизвестно"
        last_name = "Неизвестно"
        
        if config.Name and isinstance(config.Name, str) and " " in config.Name:
            name_parts = config.Name.split()
            if len(name_parts) >= 2:
                last_name, first_name = name_parts[0], name_parts[1]
                log_event(f"Получены части имени для указания отдыха: фамилия='{last_name}', имя='{first_name}'")
        
        if first_name != "Неизвестно" and last_name != "Неизвестно":
            data = {"type": "updateSessionDescription", "name": first_name, "surname": last_name, "new_description": "Отдых"}
            log_event(f"Запрос на обновление статуса на 'Отдых': {data}")
            result = database(data)
            log_event(f"Результат обновления статуса: {result}")
            if result and result.get('status') != 'ok':
                log_error(f"Ошибка обновления статуса на 'Отдых': {result}")
        else:
            log_warning("Не удалось обновить статус на 'Отдых': некорректные данные пользователя")
    except Exception as e:
        log_error(f"Ошибка при обновлении статуса на 'Отдых': {e}")
    
    # work_ui_instance.stop_timer()  # Остановка таймера
    # work_ui_instance.label.setText("00:00:00")  # Сброс отображаемого времени

    # if data_detail["stage"] == "Маркировка":
    #     # print(time_start)
    #     # print(time_end)
    #     # time_stage = {"stage": "Маркировка", "time_start": time_start, "time_end": time_end}
    #     # response_data = {'type': 'updatestage', 'stage': 'Маркировка', 'serial': data_detail["serial_number"], "time": time_stage}
    #     response_data = {'type': 'mark', 'name': '', 'serial': data_detail["serial_number"]}
    #     # print(response_data)
    #     response = database(response_data)

    
# Добавляем функцию для завершения сессии пользователя
def reset_session():
    """
    Завершает текущую сессию работы пользователя, сбрасывает состояние
    """
    # Отправляем запрос на сервер для закрытия сессии, если пользователь авторизован
    try:
        # Получаем имя и фамилию из переменной Name
        first_name = "Неизвестно"
        last_name = "Неизвестно"
        
        if config.Name and isinstance(config.Name, str) and " " in config.Name:
            name_parts = config.Name.split()
            if len(name_parts) >= 2:
                last_name, first_name = name_parts[0], name_parts[1]
                log_event(f"Получены части имени для завершения сессии: фамилия='{last_name}', имя='{first_name}'")
        
        # Создаем запрос на завершение сессии, аналогично button.py
        if first_name != "Неизвестно" and last_name != "Неизвестно" and config.session_on:
            log_event(f"Завершение сессии пользователя: {last_name} {first_name}")
            
            # Использовать конкретный запрос на endSession только для текущего пользователя
            end_session_data = {
                'type': 'endSession',
                'name': first_name,
                'surname': last_name
            }
            
            # Отправляем запрос на сервер
            from database import database
            response = database(end_session_data)
            
            # Логируем ответ сервера
            if response and response.get('status') == 'ok':
                log_event(f"Сессия пользователя {last_name} {first_name} успешно закрыта на сервере")
                config.session_on = False
            else:
                log_error(f"Ошибка при закрытии сессии на сервере: {response}")
        else:
            log_warning(f"Сессия не была закрыта. Имя={first_name}, Фамилия={last_name}, session_on={config.session_on}")
    except Exception as e:
        log_error(f"Ошибка при отправке запроса на завершение сессии: {e}")
    
    # Логируем событие завершения работы
    log_event("Пользователь завершил работу")
    
    # Сбрасываем состояние
    config.auth = False
    config.data = None
    config.user = None
    config.session_on = False

    global time_start
    time_start = None

    
    # Очищаем информацию о детали во всех интерфейсах
    if mark_ui_instance:
        mark_ui_instance.detail(False)
    if work_ui_instance:
        work_ui_instance.detail(False)
    if packing_ui_instance:
        packing_ui_instance.detail(False)
    if test_ui_instance:
        test_ui_instance.detail(False)
    
    return True

def update(name=None, serial=None):
    global time_start
    utc_time = datetime.utcnow()
    utc_plus_5 = utc_time + timedelta(hours=5)
    time_end = utc_plus_5.strftime('%Y-%m-%d %H:%M:%S')
    if name and serial:
        response_data = {'type': 'mark', "name": name, 'serial': serial, 'time': time_end}
        # МЕТРАН 150 SN904
        log_event(f"Маркировка вручную: {response_data}")
        response = database(response_data)
        log_event(f"Ответ от сервера: {response}")
        return

    global data_detail

    if data_detail:
        x = data_detail["data"]
        if x['stage'] == "Маркировка":
            response_data = {'type': 'updatestage', 'stage': 'Сборка', 'serial': x['serial_number'], 'start': time_start, 'end': time_end}
            response = database(response_data)
            if config.work:
                end_work()
        elif x['stage'] == "Сборка":
            response_data = {'type': 'updatestage', 'stage': 'Тестирование', 'serial': x['serial_number'], 'start': time_start, 'end': time_end}
            response = database(response_data)
            if config.work:
                end_work()
        elif x['stage'] == "Тестирование":
            response_data = {'type': 'updatestage', 'stage': 'Упаковка', 'serial': x['serial_number'], 'start': time_start, 'end': time_end}
            response = database(response_data)
            if config.work:
                end_work()

def getDetail(serial_number):
    data = {"type": "details", "serial": serial_number}
    global data_detail
    global mark_ui_instance, work_ui_instance
    
    log_event(f"Запрос данных о детали с серийным номером: {serial_number}")
    log_event(f"Текущее состояние: Name='{config.Name}', auth={config.auth}, session_on={config.session_on}")
    
    response = database(data)
    log_event(f"Ответ от сервера: {response}")
    
    if response and response.get('status') == 'ok' and 'data' in response:
        data_detail = response
        response_data = response['data']
        start_work(response_data["serial_number"], response_data)
    else:
        log_error(f"Ошибка получения данных о детали: {response}")
        show_error_dialog("Ошибка", "Не удалось получить данные о детали.")

def zakurit():
    global data_detail
    if data_detail:
        x = data_detail["data"]
        response = {"type": "kocak", "serial": x["serial_number"]}
        if database(response):
            end_work()
            data_detail = None
        else:
            # Добавляем иконку к диалогу ошибки
            icon_path = get_icon_path("favicon.ico")
            error_dialog = QMessageBox()
            error_dialog.setWindowIcon(QIcon(icon_path))
            error_dialog.setWindowTitle("Ошибка")
            error_dialog.setText("Нет доступа к серверу.")
            error_dialog.exec_()
        

            
# 0444390041824