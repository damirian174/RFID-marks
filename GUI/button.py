import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QLabel, QComboBox, QVBoxLayout, QWidget, QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal, QObject
from PySide6.QtGui import QImage, QPixmap, QIcon
import cv2
from pyzbar.pyzbar import decode
from menu import Ui_MainWindow as MenuUI
from Work import Ui_MainWindow as WorkUI
from Mark import Ui_MainWindow as MarkUI
from Test import Ui_MainWindow as TestsUI
from Packing import Ui_MainWindow as PackingUI
from admin import Ui_MainWindow as AdminUI
from database import database
from config import auth, work, mark
from detail_work import *
from COM import SerialListener
from error_test import show_error_dialog
import serial
import serial.tools.list_ports
import hashlib
from logger import *

class CameraWorker(QObject):
    image_ready = Signal(QPixmap)
    barcode_scanned = Signal(str)

    def __init__(self, camera_index):
        super().__init__()
        self.capture = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        self.running = True

    def run(self):
        while self.running:
            ret, frame = self.capture.read()
            if not ret:

                continue
            resized_frame = cv2.resize(frame, (300, 200))
            frame_rgb = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame_rgb.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.image_ready.emit(pixmap)

            decoded_objects = decode(frame)
            for obj in decoded_objects:
                try:
                    data = obj.data.decode("utf-8")
                    self.barcode_scanned.emit(data)
                except Exception as e:
                    log_error(f"Ошибка при декодировании штрихкода: {str(e)}")

        self.capture.release()

    def stop(self):
        self.running = False

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
        self.init_pages()
        self.connect_header_buttons()

        if mark == False:
            self.x = self.find_arduino()
            if self.x:
                log_event(f"Найден COM-порт: {self.x}")
                self.serial_listener = SerialListener(self.x, 9600)
                self.serial_listener.data_received.connect(self.handle_serial_data)
                self.serial_listener.start()
            else:
                log_error("Не найден подходящий COM-порт")


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
        self.mark_ui.setupUi(self.mark_page)

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

        # # Устанавливаем иконку для всех страниц
        # self.setWindowIcon(QIcon(icon_path))

        # ComboBox для выбора камеры
        self.combo = QComboBox(self.scan_page)
        self.combo.setGeometry(450, 80, 400, 40)
        self.combo.currentIndexChanged.connect(self.on_camera_selected)

        # Добавляем метку для отображения выбранной камеры
        self.camera_label = QLabel("Выбранная камера: ", self.scan_page)
        self.camera_label.setGeometry(450, 130, 400, 40)
        self.camera_label.setStyleSheet("font: 14px; color: black; background-color: #5F7ADB; border-radius: 5px; color: white; font: 25px; font-weight: 600")

        self.camera_feed = QLabel(self.scan_page)
        self.camera_feed.setGeometry(10, 10, 300, 200)
        self.camera_feed.setStyleSheet("border: 1px solid black; background-color: #5F7ADB")

        self.start_scan()


    def find_arduino(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "USB Serial Port" in port.description:
                return port.device
            
        return None

    def handle_serial_data(self, data):
        from detail_work import getDetail
        log_event(f"Получены данные из порта: {data}")
        getDetail(data)
        work = True
    
    def get_available_cameras(self):
        cameras = []
        for i in range(2):  # Пробуем камеры с индексами от 0 до 9
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cameras.append((i, f"Камера {i}"))
                cap.release()
        return cameras


    def start_scan(self):
        # Получаем список доступных камер
        self.available_cameras = self.get_available_cameras()

        if not self.available_cameras:
            log_error("Камеры не найдены")
            return

        # Добавляем камеры в ComboBox
        for camera in self.available_cameras:
            self.combo.addItem(f"Камера {camera[0]}: {camera[1]}")

        if self.available_cameras:
            self.on_camera_selected(0)  # Выбираем первую камеру по умолчанию

    def on_camera_selected(self, index):
        if index >= len(self.available_cameras):
            return

        # Получаем индекс камеры
        camera_index = self.available_cameras[index][0]
        camera_name = self.available_cameras[index][1]

        # Обновляем метку с именем камеры
        self.camera_label.setText(f"Выбранная камера: {camera_name}")

        # Останавливаем текущую камеру, если она была
        if hasattr(self, 'worker') and self.worker.running:
            self.worker.stop()
            self.thread.quit()
            self.thread.wait()

        # Запускаем новый поток с выбранной камерой
        self.worker = CameraWorker(camera_index)
        self.worker.image_ready.connect(self.update_camera_feed_display)
        self.worker.barcode_scanned.connect(self.handle_scanned_barcode)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.start()


    def update_camera_feed_display(self, pixmap):
        self.camera_feed.setPixmap(pixmap)

    def handle_scanned_barcode(self, barcode):
        log_event(f"Отсканированный штрихкод: {barcode}")
        self.uid = barcode
        self.verify()

    def verify(self):
        # Проверяем, прошел ли пользователь верификацию
        if self.is_verified:
            return  # Прерываем выполнение, если уже прошел верификацию

        data = {"type": "user", "uid": self.manual_input.text() or self.uid}
        log_event(f"Попытка аутентификации пользователя с UID: {data['uid']}")
        if self.is_verified == False:
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
                        

                        # Останавливаем камеру после успешного входа
                        if hasattr(self, 'worker') and self.worker.running:
                            self.worker.stop()
                            self.thread.quit()
                            self.thread.wait()

                        # Обновляем имя пользователя в разных страницах
                        self.work_ui.updateName(name=name)
                        self.tests_ui.updateName(name=name)
                        self.packing_ui.updateName(name=name)
                        self.mark_ui.updateName(name=name)

                        # Переходим на рабочую страницу
                        self.stacked_widget.setCurrentWidget(self.work_page)
                        log_event(f"Успешная аутентификация пользователя: {name}")
                        auth = True
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
        if mark == False:
            self.serial_listener.stop()
            self.serial_listener.wait()
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
        else:
            self.error_message.setText("Неверный логин или пароль")

    def connect_header_buttons(self):
        self.setup_buttons(self.work_ui, self.mark_page, self.tests_page, self.packing_page, self.login_page)
        self.setup_buttons(self.mark_ui, self.mark_page, self.tests_page, self.packing_page, self.login_page)
        self.setup_buttons(self.tests_ui, self.mark_page, self.tests_page, self.packing_page, self.login_page)
        self.setup_buttons(self.packing_ui, self.mark_page, self.tests_page, self.packing_page, self.login_page)
        self.setup_buttons(self.admin_ui, self.work_page, self.mark_page, self.tests_page, self.packing_page, self.login_page)

    def setup_buttons(self, ui, mark_page, tests_page, packing_page, login_page, admin_page=None):
        if hasattr(ui, 'pushButton_7'):
            ui.pushButton_7.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(mark_page))
        if hasattr(ui, 'pushButton_2'):
            ui.pushButton_2.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(tests_page))
        if hasattr(ui, 'pushButton_5'):
            ui.pushButton_5.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(packing_page))
        if hasattr(ui, 'pushButton_6'):
            ui.pushButton_6.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(login_page))
        if hasattr(ui, 'pushButton_8'):
            ui.pushButton_8.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.work_page))
        if admin_page:
            if hasattr(ui, 'pushButton_9'):
                ui.pushButton_9.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(admin_page))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
