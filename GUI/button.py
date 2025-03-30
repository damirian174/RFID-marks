import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QLabel, QComboBox, QVBoxLayout, QWidget, QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal, QObject
from PySide6.QtGui import QImage, QPixmap, QIcon
from menu import Ui_MainWindow as MenuUI
from Work import Ui_MainWindow as WorkUI
from Mark import Ui_MainWindow as MarkUI
from Test import Ui_MainWindow as TestsUI
from Packing import Ui_MainWindow as PackingUI
from admin import Ui_MainWindow as AdminUI
from database import database
import config
from detail_work import *
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
        self.port = self.find_arduino()
        self.serial_manager = SerialManager(self.port, 9600) if self.port else None  # Создаём сразу
        if not self.serial_manager:
            log_error("Не найден подходящий COM-порт")

        self.init_pages()  # Теперь сначала создаются страницы
        self.connect_header_buttons()  # А потом подключаем кнопки

        if self.serial_manager:
            self.serial_listener = SerialListener(self.serial_manager)
            self.serial_listener.data_received.connect(self.handle_serial_data)
            self.serial_listener.start()

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
        self.menu_ui.label.setText("Отсканируйте штрихкод")
        self.menu_ui.label.setAlignment(Qt.AlignCenter)

        self.manual_input = QLineEdit(self.scan_page)
        self.manual_input.setPlaceholderText("Введите штрихкод вручную")
        self.manual_input.setGeometry(450, 400, 400, 40)
        self.manual_input.returnPressed.connect(self.verify)

        manual_button = QPushButton("Подтвердить", self.scan_page)
        manual_button.setGeometry(550, 550, 200, 40)
        manual_button.clicked.connect(self.manual_entry)
        icon_path = "favicon.ico"  # Путь к вашей иконке



    def find_arduino(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "USB Serial Port" in port.description or "Устройство с последовательным интерфейсом" in port.description:
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





    def handle_scanned_barcode(self, barcode):
        log_event(f"Отсканированный штрихкод: {barcode}")
        self.uid = barcode
        self.verify()

    def verify(self):
        # Проверяем, прошел ли пользователь верификацию
        if self.is_verified:
            return  # Прерываем выполнение, если уже прошел верификацию
        if config.data:
            return

        data = {"type": "user", "uid": self.manual_input.text() or self.uid}
        log_event(f"Попытка аутентификации пользователя с UID: {data['uid']}")
        if self.is_verified == False and not config.data:
            try: 
                worker = database(data)
            
                if worker["status"] == "ok":
                    name = worker["surname"] + " " + worker["name"]

                    self.is_verified = True



                    reply = QMessageBox.question(self, 'Подтверждение',
                                                f'Вы {name}?',
                                                QMessageBox.Yes | QMessageBox.No,
                                                QMessageBox.No)

                    if reply == QMessageBox.Yes:
                        
                        config.data = True

                        # Останавливаем камеру после успешного входа
                        if hasattr(self, 'worker') and self.worker.running:
                            self.worker.stop()
                            self.thread.quit()
                            self.thread.wait()
                        # Обновляем имя пользователя в разных страницах
                        config.user = name
                        self.work_ui.updateName(name=name)
                        self.tests_ui.updateName(name=name)
                        self.packing_ui.updateName(name=name)
                        self.mark_ui.updateName(name=name)

                        # Переходим на рабочую страницу
                        self.stacked_widget.setCurrentWidget(self.work_page)
                        log_event(f"Успешная аутентификация пользователя: {name}")
                        config.auth = True
                        self.is_verified = False
                        self.work_ui.running = True
                        self.work_ui.start_timer()
                    else: 
                        self.is_verified = False
                        log_error("Пользователь не найден")
                        show_error_dialog('Пользователь не найден!', False)
                else:
                    show_error_dialog('Пользователь не найден!', False)
            except Exception as e:
                log_error(f"Ошибка при аутентификации: {str(e)}")



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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
