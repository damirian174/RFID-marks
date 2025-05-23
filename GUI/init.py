import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QLabel, QComboBox, QVBoxLayout, QWidget, QLineEdit, QPushButton, QMessageBox,
    QSplashScreen
)
from PySide6.QtCore import Qt, QThread, Signal, QObject, QTimer
from PySide6.QtGui import QImage, QPixmap, QIcon, QTransform, QPainter
from database import test_connection
from menu import Ui_MainWindow as MenuUI
from Work import Ui_MainWindow as WorkUI
from Mark import Ui_MainWindow as MarkUI
from Test import Ui_MainWindow as TestsUI
from Packing import Ui_MainWindow as PackingUI
from admin import Ui_MainWindow as AdminUI
import config
from detail_work import getDetail, start_work, end_work, pause_work, couintine_work, reset_session, update, getUI
from database import database
from COM import SerialManager, SerialListener  # Импорт нового менеджера
from error_test import show_error_dialog
import serial
import serial.tools.list_ports
import hashlib
from logger import *


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ао Метран")
        self.setGeometry(100, 100, 1300, 700)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        log_event("Главное окно приложения создано")

        self.correct_password_hash = self.hash_password("Метран")
        self.is_verified = False 
        self.data = None
        
        # Добавляем инициализацию переменных для имени
        self.first_name = ""
        self.last_name = ""
        self.full_name = ""
        self.connect_status = False

        self.port = self.find_metr()
        self.serial_manager = SerialManager(self.port, 9600) if self.port else None  # Создаём сразу
        if not self.serial_manager:
            log_error("Не найден подходящий COM-порт")

        self.init_pages()  # Теперь сначала создаются страницы
        self.connect_header_buttons()  # А потом подключаем кнопки

        if self.serial_manager:
            self.serial_listener = SerialListener(self.serial_manager)
            self.serial_listener.data_received.connect(self.handle_serial_data)
            self.serial_listener.connection_lost.connect(self.handle_connection_lost)
            self.serial_listener.start()
            
        # Запускаем мониторинг подключения
        self.setup_connection_monitor()

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def init_pages(self):
        self.scan_page = QMainWindow()
        self.menu_ui = MenuUI()
        self.menu_ui.setupUi(self.scan_page)
        self.menu_ui.label.setText("Введите штрихкод")

        self.work_page = QMainWindow()
        self.mark_page = QMainWindow()
        self.tests_page = QMainWindow()
        self.packing_page = QMainWindow()
        self.admin_page_ui = QMainWindow()
        self.login_page = QWidget()
        self.error_page = QMainWindow()
        icon_path = self.get_ico_path("favicon.ico")
        # Устанавливаем иконку для всех страниц
        self.scan_page.setWindowIcon(QIcon(icon_path))
        self.work_page.setWindowIcon(QIcon(icon_path))
        self.mark_page.setWindowIcon(QIcon(icon_path))
        self.tests_page.setWindowIcon(QIcon(icon_path))
        self.packing_page.setWindowIcon(QIcon(icon_path))
        self.admin_page_ui.setWindowIcon(QIcon(icon_path))
        self.setWindowIcon(QIcon(icon_path))  # Для главного окна




        self.work_ui = WorkUI()
        self.work_ui.setupUi(self.work_page)

        self.mark_ui = MarkUI()
        self.mark_ui.setupUi(self.mark_page, self.serial_manager)  # Передаём serial_manager



        self.tests_ui = TestsUI()
        self.tests_ui.setupUi(self.tests_page)

        self.packing_ui = PackingUI()
        self.packing_ui.setupUi(self.packing_page)

        self.admin_ui = AdminUI()
        self.admin_ui.setupUi(self.admin_page_ui)

        getUI(self.mark_ui, self.work_ui, self.packing_ui, self.tests_ui)

        self.uid = None
        self.init_login_page()

        self.stacked_widget.addWidget(self.scan_page)
        self.stacked_widget.addWidget(self.work_page)
        self.stacked_widget.addWidget(self.mark_page)
        self.stacked_widget.addWidget(self.tests_page)
        self.stacked_widget.addWidget(self.packing_page)
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.admin_page_ui)
        self.stacked_widget.addWidget(self.error_page)

        self.mark_ui.pushButton_9.clicked.connect(self.setup_scan_page)
        self.packing_ui.pushButton_9.clicked.connect(self.setup_scan_page)
        self.tests_ui.pushButton_9.clicked.connect(self.setup_scan_page)
        self.work_ui.pushButton_9.clicked.connect(self.setup_scan_page)

        self.setup_scan_page()

    def setup_scan_page(self):
        self.menu_ui.label.setText("Отсканируйте карточку")
        self.menu_ui.label.setAlignment(Qt.AlignCenter)

        # Получаем размер окна для адаптивных вычислений
        window_width = self.scan_page.width()
        window_height = self.scan_page.height()
        
        # Вычисляем базовый размер шрифта (2.5% от меньшей стороны окна)
        base_font_size = min(window_width, window_height) * 0.025
        input_size = max(14, int(base_font_size * 1.2))  # Размер шрифта для поля ввода
        button_size = max(14, int(base_font_size * 1.3))  # Размер шрифта для кнопки
        
        # Адаптивные размеры элементов
        input_width = min(max(350, int(window_width * 0.3)), 500)  # 30% ширины окна, мин. 350px, макс. 500px
        input_height = max(40, int(window_height * 0.06))          # 6% высоты окна, мин. 40px
        button_width = min(max(200, int(window_width * 0.15)), 300) # 15% ширины окна, мин. 200px, макс. 300px
        button_height = max(40, int(window_height * 0.06))          # 6% высоты окна, мин. 40px
        
        # Расположение элементов (центрирование)
        input_x = (window_width - input_width) // 2
        input_y = int(window_height * 0.55)  # Примерно 55% от высоты окна
        button_x = (window_width - button_width) // 2
        button_y = input_y + input_height + 20  # 20px под полем ввода
        
        # Настройка стилей
        input_style = f"""
            QLineEdit {{
                font-size: {input_size}px;
                padding: 8px 15px;
                border-radius: 10px;
                background-color: white;
                border: 1px solid #ced4da;
                color: #333;
            }}
            QLineEdit:focus {{
                border: 2px solid #5F7ADB;
                background-color: #f8f9fa;
            }}
        """
        
        button_style = f"""
            QPushButton {{
                font-size: {button_size}px;
                font-weight: bold;
                padding: 8px 20px;
                border-radius: 10px;
                background-color: #5F7ADB;
                color: white;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #4A6ED9;
            }}
            QPushButton:pressed {{
                background-color: #3A5EC9;
            }}
        """
        
        # Создаем и настраиваем поле ввода
        self.manual_input = QLineEdit(self.scan_page)
        self.manual_input.setPlaceholderText("Введите номер карточки или ID")
        self.manual_input.setGeometry(input_x, input_y, input_width, input_height)
        self.manual_input.setStyleSheet(input_style)
        self.manual_input.setAlignment(Qt.AlignCenter)
        self.manual_input.setClearButtonEnabled(True)
        self.manual_input.returnPressed.connect(self.verify)
        
        # Создаем и настраиваем кнопку
        manual_button = QPushButton("Подтвердить", self.scan_page)
        manual_button.setGeometry(button_x, button_y, button_width, button_height)
        manual_button.setStyleSheet(button_style)
        manual_button.setCursor(Qt.PointingHandCursor)
        manual_button.clicked.connect(self.manual_entry)
        
        # Подключаем обработчик изменения размера окна для адаптивности
        self.scan_page.resizeEvent = self.scan_page_resize_event
        
    def scan_page_resize_event(self, event):
        """Обработчик изменения размера окна для адаптивного обновления элементов"""
        # Только если у нас есть ссылки на элементы
        if hasattr(self, 'manual_input') and self.manual_input and hasattr(self, 'scan_page'):
            window_width = self.scan_page.width()
            window_height = self.scan_page.height()
            
            # Пересчитываем размеры элементов
            input_width = min(max(350, int(window_width * 0.3)), 500)
            input_height = max(40, int(window_height * 0.06))
            button_width = min(max(200, int(window_width * 0.15)), 300)
            button_height = max(40, int(window_height * 0.06))
            
            # Центрируем элементы
            input_x = (window_width - input_width) // 2
            input_y = int(window_height * 0.55)
            button_x = (window_width - button_width) // 2
            button_y = input_y + input_height + 20
            
            # Применяем новые размеры
            for child in self.scan_page.children():
                if isinstance(child, QLineEdit) and child.placeholderText() == "Введите номер карточки или ID":
                    child.setGeometry(input_x, input_y, input_width, input_height)
                elif isinstance(child, QPushButton) and child.text() == "Подтвердить":
                    child.setGeometry(button_x, button_y, button_width, button_height)
        
        # Вызываем оригинальный метод для завершения обработки события
        QMainWindow.resizeEvent(self.scan_page, event)

    def find_metr(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "USB Serial" in port.description or "Устройство с последовательным интерфейсом" in port.description:
                return port.device
            
        return None

    def handle_serial_data(self, data):
        if data is None:
            data = config.user

        if data == "READ_ERROR":
            self.packing_ui.change_color(1)
            self.tests_ui.change_color(1)
            self.work_ui.change_color(1)
            log_error("Error with read")
            return
        if isinstance(data, list) and len(data) > 0 and data[0] == "WRITE_ERROR":
            log_event("Ошибка при записи метки")
            if hasattr(self.mark_ui, "status_label"):
                self.mark_ui.status_label.setText("❌ Ошибка при записи метки. Попробуйте еще раз.")
                self.mark_ui.handle_write_result(True, False)
            from PySide6.QtCore import QTimer
            if hasattr(self.mark_ui, "write_dialog") and self.mark_ui.write_dialog:
                QTimer.singleShot(2000, self.mark_ui.write_dialog.close)
            return


        if isinstance(data, list) and len(data) > 0 and data[0] == "WAIT_CARD":
            log_event("Ожидание поднесения карты пользователем")
            if hasattr(self, "mark_ui") and hasattr(self.mark_ui, "status_label"):
                self.mark_ui.status_label.setText(data[1])
            return
        if isinstance(data, list) and len(data) > 0 and data[0] == "WRITE_SUCCESS":
            log_event("Метка успешно записана")
            if hasattr(self.mark_ui, "status_label"):
                self.mark_ui.status_label.setText("✅ Метка успешно записана")
                self.mark_ui.handle_write_result(True, False)
            from PySide6.QtCore import QTimer
            if hasattr(self.mark_ui, "write_dialog") and self.mark_ui.write_dialog:
                QTimer.singleShot(2000, self.mark_ui.write_dialog.close)
            return

        if not data or not isinstance(data, list):
            log_event(f"Ошибка: Данные пришли в неверном формате или пустые: {data}")
            return

        log_event(f"Данные перед очисткой: {data}")

        # Очистка данных и проверка
        cleaned_data = [item.strip(". \r\n") for item in data if isinstance(item, str) and item.strip()]
        
        log_event(f"Очищенные данные: {cleaned_data}")  

        if len(cleaned_data) < 2:
            log_event(f"Ошибка: Данные после очистки все еще неверные: {cleaned_data}")
            return
        
        

        if cleaned_data[1] == "detail":  
            if config.auth:
                from detail_work import getDetail
                log_event(f"Получены данные из порта: {cleaned_data[0]}")
                getDetail(cleaned_data[0])
                config.user = None
            else:
                config.user = None
                return
            
        elif cleaned_data[1] == "user":  
            log_event(f"Пользователь с UID: {cleaned_data[0]}")  
            self.uid = cleaned_data[0]
            self.verify()
            config.user = None
        else:
            log_event(f"Неизвестный формат данных: {cleaned_data}")


    def verify(self):
        # Проверяем, прошел ли пользователь верификацию
        if self.is_verified:
            return  # Прерываем выполнение, если уже прошел верификацию
        if config.data:
            return

        data = {"type": "user", "uid": self.manual_input.text() or self.uid}
        log_event(f"Попытка аутентификации пользователя с UID: {data['uid']}")
        if self.is_verified == False and not config.data:
            # Используем синхронный запрос
            worker = database(data)
            log_event(f"Ответ сервера: {worker}")
            
            if worker and worker["status"] == "ok":
                # Проверяем, в каком формате приходят данные
                if "data" in worker:
                    user_data = worker["data"]
                    log_event(f"Данные пользователя в поле data: {user_data}")
                else:
                    user_data = worker
                    log_event(f"Данные пользователя в корне ответа: {user_data}")
                
                # Проверяем наличие необходимых полей
                surname = user_data.get("surname", "")
                name = user_data.get("name", "")
                
                if not surname or not name:
                    log_error(f"Отсутствуют обязательные поля в ответе: {user_data}")
                    
                    error_msg = QMessageBox()
                    error_msg.setWindowTitle('Ошибка')
                    error_msg.setText('Не удалось получить данные пользователя. Попробуйте еще раз.')
                    error_msg.setStandardButtons(QMessageBox.Ok)
                    
                    # Установка иконки
                    icon_path = self.get_ico_path("favicon.ico")
                    error_msg.setWindowIcon(QIcon(icon_path))
                    
                    error_msg.exec()
                    return
                    
                full_name = f"{surname} {name}"
                self.is_verified = True

                reply = QMessageBox()
                reply.setWindowTitle('Подтверждение')
                reply.setText(f'Вы {full_name}?')
                reply.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                reply.setDefaultButton(QMessageBox.No)
                
                # Установка иконки
                icon_path = self.get_ico_path("favicon.ico")
                reply.setWindowIcon(QIcon(icon_path))
                
                result = reply.exec()

                if result == QMessageBox.Yes:
                    config.data = True
                    
                    # Останавливаем камеру после успешного входа
                    if hasattr(self, 'worker') and self.worker.running:
                        self.worker.stop()
                        self.thread.quit()
                        self.thread.wait()
                    # Обновляем имя пользователя в разных страницах
                    if config.connect_status:
                        data = {"type": "startSession", "name": name, "surname": surname, "work_description": "Без детали"}
                        log_event(f"Запрос на создание сессии: {data}")
                        worker = database(data)
                        log_event(f"Ответ на создание сессии: {worker}")
                        if worker and worker["status"] == "ok":
                            log_event(f"Сессия успешно начата: {full_name}")
                            config.session_on = True
                        else:
                            log_error(f"Не удалось начать сессию: {full_name}, ответ: {worker}")

                    log_event(f"Устанавливаем переменную config.user: {full_name}")
                    config.user = full_name
                    # Устанавливаем переменную Name в правильном формате
                    log_event(f"Устанавливаем переменную config.Name: {surname} {name}")
                    config.Name = f"{surname} {name}"
                    log_event(f"Установлено значение config.Name: {config.Name}")
                    
                    # Инициализируем переменные, необходимые для завершения сессии
                    self.last_name = surname
                    self.first_name = name
                    self.full_name = full_name
                    config.id = user_data["id"]
                    
                    self.work_ui.updateName(name=full_name)
                    self.tests_ui.updateName(name=full_name)
                    self.packing_ui.updateName(name=full_name)
                    self.mark_ui.updateName(name=full_name)
                    # update(name="МЕТРАН 150", serial="SN904")
                    getDetail

                    # Переходим на рабочую страницу
                    self.stacked_widget.setCurrentWidget(self.work_page)
                    log_event(f"Успешная аутентификация пользователя: {full_name}")
                    config.auth = True
                    self.is_verified = False
                    self.work_ui.running = True
                    self.work_ui.start_timer()
                else:
                    config.auth = False
                    config.data = None
                    config.user = None
                    self.is_verified = False
                    log_error(f"Не удалось аутентифицировать пользователя: {self.uid}")
            elif worker["status"] == "error" and worker["message"] and "У пользователя уже есть активная сессия" in worker["message"]:
                log_error(f"У пользователя уже есть активная сессия: {self.uid}")
                
                message = QMessageBox()
                message.setWindowTitle('Предупреждение')
                message.setText(f'У пользователя уже есть активная сессия')
                message.setIcon(QMessageBox.Warning)
                
                # Используем addButton вместо setButtonText для избежания предупреждений
                cancel_button = message.addButton("Отмена", QMessageBox.RejectRole)
                yes_button = message.addButton("Войти всё равно", QMessageBox.AcceptRole)
                message.setDefaultButton(cancel_button)
                
                # Установка иконки
                icon_path = self.get_ico_path("favicon.ico")
                message.setWindowIcon(QIcon(icon_path))
                
                message.exec()
                
                if message.clickedButton() == yes_button:
                    # Получаем данные о пользователе без создания новой сессии
                    data_user = {"type": "user", "uid": self.uid}
                    user_data_response = database(data_user)
                    
                    if user_data_response:
                        user_data = user_data_response.get("data", user_data_response)
                        surname = user_data.get("surname", "")
                        name = user_data.get("name", "")
                        
                        if surname and name:
                            full_name = f"{surname} {name}"
                            config.data = True
                            
                            # Устанавливаем необходимые переменные без отправки startSession
                            config.user = full_name
                            config.Name = f"{surname} {name}"
                            self.last_name = surname
                            self.first_name = name
                            self.full_name = full_name
                            config.id = user_data["id"]
                            config.session_on = True  # Считаем сессию активной
                            
                            # Обновляем имя пользователя в разных страницах
                            self.work_ui.updateName(name=full_name)
                            self.tests_ui.updateName(name=full_name)
                            self.packing_ui.updateName(name=full_name)
                            self.mark_ui.updateName(name=full_name)
                            
                            # Переходим на рабочую страницу
                            self.stacked_widget.setCurrentWidget(self.work_page)
                            log_event(f"Пользователь {full_name} вошел с существующей сессией")
                            config.auth = True
                            self.is_verified = False
                            self.work_ui.running = True
                            self.work_ui.start_timer()
                        else:
                            log_error(f"Не удалось получить данные пользователя: {user_data}")
                            QMessageBox.warning(self, "Ошибка", "Не удалось получить данные пользователя")
                    else:
                        log_error(f"Ошибка получения данных пользователя: {user_data_response}")
                        QMessageBox.warning(self, "Ошибка", "Ошибка получения данных пользователя")


    def get_ico_path(self, image_name):
        if getattr(sys, 'frozen', False):
            # Если приложение запущено как .exe
            base_path = sys._MEIPASS
        else:
            # Если в режиме разработки
            base_path = os.path.abspath(".")

        # Формируем полный путь к изображению
        image_path = os.path.join(base_path, image_name)
        return image_path


    def manual_entry(self):
        entered_code = self.manual_input.text()
        self.uid = entered_code
        self.verify()

    def closeEvent(self, event):
        log_event("Закрытие приложения button.py")
        if config.session_on:
            try:
                log_event(f"Завершаем сессию пользователя: {self.first_name} {self.last_name}")
                data = {"type": "endSession", "name": self.first_name, "surname": self.last_name}
                worker = database(data)
                if worker and worker["status"] == "ok":
                    log_event(f"Сессия успешно завершена: {self.first_name} {self.last_name}")
                    config.session_on = False
                else:
                    log_error(f"Не удалось завершить сессию: {self.first_name} {self.last_name}")
            except Exception as e:
                log_error(f"Ошибка при завершении сессии: {e}")
        if self.serial_listener:
            self.serial_listener.stop()
            self.serial_manager.close() 
        event.accept()

    def init_login_page(self):
        layout = QVBoxLayout()
        self.login_page.setLayout(layout)

        back_button = QPushButton("Назад")
        back_button.setStyleSheet("background-color: #5F7ADB; color: white; font: 16px; padding: 5px;")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.work_page))
        layout.addWidget(back_button)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите логин")
        self.login_input.setStyleSheet("font: 16px; padding: 10px; border: 2px solid gray; border-radius: 5px;")
        layout.addWidget(self.login_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setStyleSheet("font: 16px; padding: 10px; border: 2px solid gray; border-radius: 5px;")
        layout.addWidget(self.password_input)

        self.error_message = QLabel()
        self.error_message.setStyleSheet("color: red; font: 14px;")
        layout.addWidget(self.error_message)

        login_button = QPushButton("Войти")
        login_button.setStyleSheet("background-color: #5F7ADB; color: white; font: 16px; padding: 10px; border-radius: 5px;")
        login_button.clicked.connect(self.check_admin_credentials)
        layout.addWidget(login_button)

        layout.setSpacing(10)
        layout.setContentsMargins(50, 50, 50, 50)

    def check_admin_credentials(self):
        entered_login = self.login_input.text()
        entered_password = self.password_input.text()
        entered_password_hash = self.hash_password(entered_password)

        if entered_login == "ДЮТТ" and entered_password_hash == self.correct_password_hash:
            self.login_input.clear()
            self.password_input.clear()
            self.error_message.clear()
            self.stacked_widget.setCurrentWidget(self.admin_page_ui)
            log_event("Login to the admin panel")
        else:
            self.error_message.setText("Неверный логин или пароль")
            log_error("failed login attempt to Admin Panel")

    def connect_header_buttons(self):
        self.setup_buttons(self.work_ui, self.mark_page, self.tests_page, self.packing_page, self.login_page)
        self.setup_buttons(self.mark_ui, self.mark_page, self.tests_page, self.packing_page, self.login_page)
        self.setup_buttons(self.tests_ui, self.mark_page, self.tests_page, self.packing_page, self.login_page)
        self.setup_buttons(self.packing_ui, self.mark_page, self.tests_page, self.packing_page, self.login_page)
        self.setup_buttons(self.admin_ui, self.work_page, self.mark_page, self.tests_page, self.packing_page, self.login_page)
        
        # Подключаем кнопку "Завершить работу" к новой функции
        self.mark_ui.pushButton_9.clicked.connect(self.end_session)
        self.work_ui.pushButton_9.clicked.connect(self.end_session)
        self.tests_ui.pushButton_9.clicked.connect(self.end_session)
        self.packing_ui.pushButton_9.clicked.connect(self.end_session)

    def setup_buttons(self, ui, mark_page, tests_page, packing_page, login_page, admin_page=None):
        if hasattr(ui, 'pushButton_7'):
            log_event("Enter to mark")
            ui.pushButton_7.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(mark_page))
        if hasattr(ui, 'pushButton_2'):
            ui.pushButton_2.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(tests_page))
            log_event("Enter to Test")
        if hasattr(ui, 'pushButton_5'):
            log_event("Enter to Packing")
            ui.pushButton_5.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(packing_page))
        if hasattr(ui, 'pushButton_6'):
            log_event("Enter to Login page AA")
            ui.pushButton_6.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(login_page))
        if hasattr(ui, 'pushButton_8'):
            log_event("Enter to assembly")
            ui.pushButton_8.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.work_page))
        if admin_page:
            if hasattr(ui, 'pushButton_9'):
                log_event("Enter to admin_page")
                ui.pushButton_9.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(admin_page))
                
        # Связываем функции переподключения МЭТР если они есть
        if hasattr(ui, 'reconnect_metr'):
            # Заменяем локальные функции переподключения на нашу глобальную
            ui.reconnect_metr = self.reconnect_metr_global
            
    # Глобальная функция для переподключения МЭТР, которая обновит все интерфейсы
    def reconnect_metr_global(self):
        try:
            # Создаем информационное окно
            message_box = QMessageBox()
            message_box.setWindowTitle("Переподключение к МЭТР")
            message_box.setText("Выполняется переподключение к МЭТР...")
            message_box.setStandardButtons(QMessageBox.NoButton)
            message_box.setIcon(QMessageBox.Information)
            
            # Стилизуем окно, используя функцию из текущего интерфейса
            current_widget = self.stacked_widget.currentWidget()
            if hasattr(current_widget, 'ui') and hasattr(current_widget.ui, 'style_message_box'):
                current_widget.ui.style_message_box(message_box)
            
            # Показываем сообщение без блокировки
            message_box.show()
            QApplication.processEvents()
            
            # Даже если serial_manager существует, всегда закрываем старое соединение
            if hasattr(self, 'serial_listener') and self.serial_listener:
                try:
                    self.serial_listener.stop()
                    log_event("Остановлен текущий слушатель COM-порта")
                except Exception as e:
                    log_error(f"Ошибка при остановке слушателя: {e}")
                    
            # Закрываем текущее соединение с разрывом привязки
            if hasattr(self, 'serial_manager') and self.serial_manager:
                try:
                    self.serial_manager.close()
                    log_event("Закрыто текущее соединение с COM-портом")
                except Exception as e:
                    log_error(f"Ошибка при закрытии COM-порта: {e}")
                
            # Полностью сбрасываем singleton-экземпляр SerialManager
            SerialManager._instance = None
            
            # Находим МЭТР
            ports = serial.tools.list_ports.comports()
            metr_port = None
            for port in ports:
                if "USB Serial" in port.description or "Устройство с последовательным интерфейсом" in port.description:
                    metr_port = port.device
                    break
            
            if metr_port:
                # Создаем новый SerialManager с повышенным таймаутом
                try:
                    self.serial_manager = SerialManager(metr_port, 9600)
                    log_event(f"Создан новый SerialManager с портом {metr_port}")
                    
                    # Создаем и запускаем новый слушатель
                    self.serial_listener = SerialListener(self.serial_manager)
                    self.serial_listener.data_received.connect(self.handle_serial_data)
                    self.serial_listener.connection_lost.connect(self.handle_connection_lost)
                    self.serial_listener.start()
                    log_event("Запущен новый слушатель COM-порта")
                    
                    # Обновляем ссылки на serial_manager в каждом интерфейсе
                    for page_ui in [self.mark_ui, self.work_ui, self.tests_ui, self.packing_ui]:
                        if hasattr(page_ui, 'serial_manager'):
                            page_ui.serial_manager = self.serial_manager
                            log_event(f"Обновлена ссылка на SerialManager в {page_ui.__class__.__name__}")
                    
                    # Обновляем сообщение о успехе
                    message_box.setText(f"МЭТР успешно подключен через порт {metr_port}")
                    message_box.setIcon(QMessageBox.Information)
                    message_box.setStandardButtons(QMessageBox.Ok)
                    log_event("Глобальное переподключение к МЭТР выполнено успешно")
                    self.connect_status = True
                except serial.SerialException as e:
                    # Особый случай - порт найден, но занят или недоступен
                    message_box.setText(f"Ошибка доступа к порту {metr_port}: {str(e)}\nПопробуйте отключить и снова подключить устройство.")
                    message_box.setIcon(QMessageBox.Warning)
                    message_box.setStandardButtons(QMessageBox.Ok)
                    log_error(f"Ошибка доступа к порту {metr_port}: {e}")
                    self.connect_status = False
            else:
                # Обновляем результат при неудаче поиска порта
                message_box.setText("МЭТР не найден. Проверьте подключение")
                message_box.setIcon(QMessageBox.Warning)
                message_box.setStandardButtons(QMessageBox.Ok)
                log_error("МЭТР не найден при попытке глобального переподключения")
                self.connect_status = False
            
            # Показываем диалог с результатом
            message_box.exec_()
            
        except Exception as e:
            log_error(f"Ошибка при глобальном переподключении к МЭТР: {e}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка при переподключении: {e}")

    # Добавляем функцию для автоматического мониторинга состояния подключения
    def setup_connection_monitor(self):
        """Настраивает таймер для мониторинга подключения к МЭТР"""
        self.connection_timer = QTimer(self)
        self.connection_timer.timeout.connect(self.check_connection)
        self.connection_timer.start(10000)  # Проверка каждые 10 секунд
        log_event("Запущен мониторинг подключения к МЭТР")
    
    def check_connection(self):
        """Проверяет состояние подключения к МЭТР и пытается восстановить его при необходимости"""
        if not hasattr(self, 'serial_manager') or not self.serial_manager:
            return
            
        try:
            # Простая проверка - попытка получить текущий порт
            port = self.serial_manager.port
            # Проверяем, открыт ли порт
            if hasattr(self.serial_manager, 'serial') and self.serial_manager.serial:
                if not self.serial_manager.serial.is_open:
                    log_error("Обнаружен закрытый COM-порт, попытка переподключения")
                    self.reconnect_metr_global()
            else:
                log_error("Отсутствует объект порта, попытка переподключения")
                self.reconnect_metr_global()
        except Exception as e:
            log_error(f"Ошибка при проверке соединения: {e}")
            # Автоматическое переподключение при проблемах с устройством
            self.reconnect_metr_global()

    def handle_connection_lost(self):
        """Обработчик сигнала о потере соединения от SerialListener"""
        log_error("Получен сигнал о потере соединения с МЭТР")
        
        # Показываем уведомление пользователю без блокировки интерфейса
        message_box = QMessageBox()
        message_box.setWindowTitle("Потеря соединения")
        message_box.setText("Потеряно соединение с МЭТР.\nНачинается автоматическое переподключение...")
        message_box.setStandardButtons(QMessageBox.NoButton)
        message_box.setIcon(QMessageBox.Warning)
        
        # Стилизуем окно, используя функцию из текущего интерфейса
        current_widget = self.stacked_widget.currentWidget()
        if hasattr(current_widget, 'ui') and hasattr(current_widget.ui, 'style_message_box'):
            current_widget.ui.style_message_box(message_box)
        
        # Показываем сообщение без блокировки
        message_box.show()
        QApplication.processEvents()
        
        # Пытаемся переподключиться через 2 секунды
        QTimer.singleShot(2000, lambda: (message_box.close(), self.reconnect_metr_global()))

    # Функция для завершения сессии
    def end_session(self):
        # В зависимости от того, какая кнопка была нажата, вызываем соответствующее окно подтверждения
        # Сначала определяем, из какого интерфейса вызвана функция
        sender = self.sender()
        confirm = False
        
        # Используем соответствующие методы подтверждения в зависимости от вызывающего интерфейса
        if sender == self.work_ui.pushButton_9:
            # Если из Work.py - используем его метод confirm_end_session
            confirm = self.work_ui.confirm_end_session()
        elif sender == self.mark_ui.pushButton_9:
            # Если из Mark.py - используем его метод confirm_end_session
            confirm = self.mark_ui.confirm_end_session()
        elif sender == self.tests_ui.pushButton_9:
            # Если из Test.py - используем его метод confirm_end_session
            confirm = self.tests_ui.confirm_end_session()
        elif sender == self.packing_ui.pushButton_9:
            # Если из Packing.py - используем его метод confirm_end_session
            confirm = self.packing_ui.confirm_end_session()
        else:
            # Для других источников - стандартное окно подтверждения
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Подтверждение")
            msg_box.setText("Вы хотите закончить работу?")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.No)
            
            # Установка иконки
            icon_path = self.get_ico_path("favicon.ico")
            msg_box.setWindowIcon(QIcon(icon_path))
            
            confirm = msg_box.exec() == QMessageBox.Yes
        
        # Если пользователь подтвердил - завершаем сессию
        if confirm:
            # Вызываем функцию сброса сессии из модуля detail_work
            from detail_work import reset_session
            reset_session()
            
            # Сбрасываем состояние верификации
            config.auth = False
            config.data = None
            config.user = None
            self.is_verified = False
            
            # Останавливаем таймер, если он запущен
            if hasattr(self.work_ui, 'timer') and self.work_ui.running:
                self.work_ui.stop_timer()
                
            # Очищаем поле ввода штрихкода
            self.manual_input.clear()
            
            # Переходим на начальный экран
            self.menu_ui.label.setText("Отсканируйте штрихкод")
            self.stacked_widget.setCurrentWidget(self.scan_page)
            
            log_event("Сессия пользователя завершена")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Создаем загрузочный экран
    splash_pixmap = QPixmap("loading.png")
    # Уменьшаем изображение в 4 раза
    original_size = min(splash_pixmap.width(), splash_pixmap.height()) // 4
    splash_pixmap = splash_pixmap.scaled(original_size, original_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    
    # Создаем холст большего размера, чтобы изображение целиком помещалось при вращении
    # Размер по диагонали = размер стороны * √2 (приблизительно 1.5 для запаса)
    canvas_size = int(original_size * 1.5)
    splash_canvas = QPixmap(canvas_size, canvas_size)
    splash_canvas.fill(Qt.transparent)  # Прозрачный фон

    splash = QSplashScreen(splash_canvas, Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    
    # Вращение изображения
    angle = 0
    
    def rotate_splash():
        global angle
        angle = (angle + 5) % 360
        transform = QTransform().rotate(angle)
        rotated_pixmap = splash_pixmap.transformed(transform, Qt.SmoothTransformation)
        
        # Создаем новый прозрачный холст для каждого кадра
        temp_canvas = QPixmap(canvas_size, canvas_size)
        temp_canvas.fill(Qt.transparent)
        
        # Вычисляем позицию для центрирования повернутого изображения
        x = (canvas_size - rotated_pixmap.width()) // 2
        y = (canvas_size - rotated_pixmap.height()) // 2
        
        # Рисуем поворачиваемое изображение на холсте по центру
        painter = QPainter(temp_canvas)
        painter.drawPixmap(x, y, rotated_pixmap)
        painter.end()
        
        # Устанавливаем изображение
        splash.setPixmap(temp_canvas)
        if not hasattr(rotate_splash, 'window_shown') or not rotate_splash.window_shown:
            splash.show()
    
    # Таймер для вращения
    rotation_timer = QTimer()
    rotation_timer.timeout.connect(rotate_splash)
    rotation_timer.start(10)  # Обновление каждые 10 мс
    
    # Начальное вращение
    rotate_splash()
    
    def show_connection_error_dialog():
        """Показывает диалоговое окно при ошибке соединения с сервером"""
        # Остановим вращение загрузочного экрана
        rotation_timer.stop()
        splash.hide()
        
        # Создаём диалоговое окно
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Ошибка соединения")
        msg_box.setText("Нет соединения с сервером!\nПроверьте подключение к Wi-Fi или обратитесь к системному администратору.")
        
        # Устанавливаем иконку
        app = QApplication.instance()
        window = app.activeWindow()
        if window:
            ico_path = window.get_ico_path("favicon.ico") if hasattr(window, 'get_ico_path') else "favicon.ico"
        else:
            ico_path = "favicon.ico"
        msg_box.setWindowIcon(QIcon(ico_path))
        
        # Настраиваем стиль
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #f8f9fa;
                border: 2px solid #dc3545;
                border-radius: 10px;
                min-width: 500px;
                min-height: 250px;
                padding: 20px;
            }
            QLabel {
                color: #212529;
                font-size: 16px;
                font-weight: bold;
                min-width: 450px;
                margin: 20px;
                padding: 10px;
                line-height: 1.6;
                background-color: #ffffff;
                border-radius: 8px;
                border: 1px solid #dee2e6;
            }
            QPushButton {
                background-color: #0056b3;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 25px;
                font-weight: bold;
                font-size: 14px;
                min-width: 120px;
                margin: 15px;
            }
            QPushButton:hover {
                background-color: #0069d9;
            }
            QPushButton:pressed {
                background-color: #004494;
            }
        """)
        
        # Добавляем кнопки
        exit_button = msg_box.addButton("Выйти", QMessageBox.RejectRole)
        continue_button = msg_box.addButton("Продолжить", QMessageBox.AcceptRole)
        
        # Выполняем диалог
        result = msg_box.exec()
        
        # Проверяем результат
        if msg_box.clickedButton() == exit_button:
            log_event("Пользователь выбрал выход из программы")
            sys.exit(0)
        else:
            log_event("Пользователь выбрал продолжить без соединения")
            # Показываем главное окно
            config.connect_status = False
            show_main_window()
    
    # Запуск приложения с небольшой задержкой для отображения загрузочного экрана
    def show_main_window():
        window = MainApp()
        window.show()
        splash.finish(window)
        rotation_timer.stop()
        rotate_splash.window_shown = True
    
    # Проверка соединения с сервером
    def check_server_connection():
        # Используем синхронную проверку соединения
        if test_connection():
            # Сервер доступен, запускаем приложение
            log_event("Сервер доступен")
            config.connect_status = True
            show_main_window()
        else:
            log_error("Ошибка соединения с сервером")
            # Сервер недоступен, показываем диалог
            show_connection_error_dialog()
    
    # Сначала показываем загрузочный экран, а затем проверяем соединение
    QTimer.singleShot(1500, check_server_connection)  # 1.5 секунды на отображение сплеша
    
    sys.exit(app.exec())
