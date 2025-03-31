from database import database
from error_test import show_error_dialog
from config import work, detail, auth, data
from datetime import datetime, timedelta
import time
from logger import *
import threading
from PySide6.QtWidgets import QMessageBox, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

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
    global work
    global detail
    global detail_work

    # Проверяем, не ведется ли уже работа над деталью
    if detail_work:
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Предупреждение")
        msg_box.setText("Уже ведется работа над деталью.\nЗавершите текущую работу перед началом новой.")
        msg_box.setFixedSize(550, 300)
        msg_box.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
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
    work = True
    detail = ser
    time_start = GetTime()
    global mark_ui_instance, work_ui_instance, packing_ui_instance, test_ui_instance
    if response:
        if response['stage'] == 'Маркировка':
            work_ui_instance.detail(response)
        elif response['stage'] == 'Сборка':
            test_ui_instance.detail(response)
        elif response['stage'] == 'Тестирование':
            packing_ui_instance.detail(response)
    # work_ui_instance.running = True  # Это должно теперь работать
    # work_ui_instance.start_timer()

def pause_work():
    work_ui_instance.pause_timer()

def couintine_work():
    work_ui_instance.resume_timer()




def end_work():
    global work
    global detail
    global time_end 
    global data_detail
    global time_stage
    global time_start
    global detail_work
    detail_work = False
    data = False
    work = False
    detail = None 
    time_end = GetTime()
    
    global mark_ui_instance, work_ui_instance, packing_ui_instance, test_ui_instance
    mark_ui_instance.detail(False)
    work_ui_instance.detail(False)
    packing_ui_instance.detail(False)
    test_ui_instance.detail(False)
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
    global auth
    global data
    global user
    global time_start
    
    # Логируем событие завершения работы
    log_event("Пользователь завершил работу")
    
    # Сбрасываем состояние
    auth = False
    data = None
    user = None
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
    global work
    global data_detail
    if name and serial:
        response_data = {'type': 'mark', "name": name, 'serial': serial}
        log_event(f"Маркировка вручную: {response_data}")
        response = database(response_data)
        log_event(f"Ответ от сервера: {response}")
        return

    if data_detail:
        x = data_detail["data"]
        if x['stage'] == "Маркировка":
            response_data = {'type': 'updatestage', 'stage': 'Сборка', 'serial': x['serial_number']}
            response = database(response_data)
            if work:
                end_work()
        elif x['stage'] == "Сборка":
            response_data = {'type': 'updatestage', 'stage': 'Тестирование', 'serial': x['serial_number']}
            response = database(response_data)
            if work:
                end_work()
        elif x['stage'] == "Тестирование":
            response_data = {'type': 'updatestage', 'stage': 'Упаковка', 'serial': x['serial_number']}
            response = database(response_data)
            if work:
                end_work()

def getDetail(serial_number):
    data = {"type": "details", "serial": serial_number}
    global data_detail
    global mark_ui_instance, work_ui_instance
    # data2 = {'name': 'МЕТРАН 150','serial_number': serial_number,'defective':'Да','stage':'Маркировка','sector':'аааа'}

    # mark_ui_instance.detail(data2)
    
    response = database(data)
    data_detail = response
    response = response['data']
    start_work(response["serial_number"], response)
    # if response:
    #     # Вызываем метод detail через экземпляр интерфейса
    #     start_work(serial_number, response)


def zakurit():
    global data_detail
    if data_detail:
        x = data_detail["data"]
        response = {"type": "kocak", "serial": x["serial_number"]}
        if database(response):
            end_work()
            data_detail = None
        else:
            show_error_dialog("Нет доступа к серверу.", "hgfd")
        

            
# 0444390041824