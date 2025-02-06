import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QLabel, QPushButton,
    QVBoxLayout, QWidget, QLineEdit, QMessageBox, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from menu import Ui_MainWindow as MenuUI
from Work import Ui_MainWindow as WorkUI
from Mark import Ui_MainWindow as MarkUI
from Test import Ui_MainWindow as TestsUI
from Packing import Ui_MainWindow as PackingUI
from admin import Ui_MainWindow as AdminUI
import cv2
import hashlib
import threading
from pyzbar.pyzbar import decode, ZBarSymbol
from database import database
from config import auth, work

from COM import SerialListener


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Метран - Сканирование")
        self.setGeometry(100, 100, 1000, 800)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.correct_password_hash = self.hash_password("Метран")

        self.init_pages()
        self.connect_header_buttons()
        # self.serial_listener = SerialListener("COM8", 9600)
        # self.serial_listener.data_received.connect(self.handle_serial_data)
        # self.serial_listener.start()

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def init_pages(self):
        self.scan_page = QMainWindow()
        self.menu_ui = MenuUI()
        self.menu_ui.setupUi(self.scan_page)
        self.menu_ui.label.setText("Отсканируйте штрихкод или введите его вручную")

        self.work_page = QMainWindow()
        self.mark_page = QMainWindow()
        self.tests_page = QMainWindow()
        self.packing_page = QMainWindow()
        self.admin_page_ui = QMainWindow()
        self.login_page = QWidget()
        self.error_page = QMainWindow()

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


        self.init_login_page()

        self.stacked_widget.addWidget(self.scan_page)
        self.stacked_widget.addWidget(self.work_page)
        self.stacked_widget.addWidget(self.mark_page)
        self.stacked_widget.addWidget(self.tests_page)
        self.stacked_widget.addWidget(self.packing_page)
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.admin_page_ui)
        self.stacked_widget.addWidget(self.error_page)

        self.setup_scan_page()

    def handle_serial_data(self, data):
        from GetDetail import getDetail
        print(f"Получены данные из порта: {data}")
        getDetail(data, self.mark_ui)
        work = True

    def closeEvent(self, event):
        self.serial_listener.stop()
        self.serial_listener.wait()
        event.accept()

    def setup_scan_page(self):
        self.menu_ui.label.setText("Сканирование штрихкода активно")
        self.menu_ui.label.setAlignment(Qt.AlignCenter)

        self.manual_input = QLineEdit(self.scan_page)
        self.manual_input.setPlaceholderText("Введите штрихкод вручную")
        self.manual_input.setGeometry(300, 400, 400, 40)

        manual_button = QPushButton("Подтвердить", self.scan_page)
        manual_button.setGeometry(400, 450, 200, 40)
        manual_button.clicked.connect(self.manual_entry)

        # Add a QLabel for displaying the camera feed
        self.camera_feed = QLabel(self.scan_page)
        self.camera_feed.setGeometry(10, 10, 300, 200)
        self.camera_feed.setStyleSheet("border: 1px solid black;")

        # Start scanning immediately
        self.start_scan()

    def verify(self, user):
        data = {
            "type": "user",
            "uid": user
        }
        worker = database(data)
        if worker["status"] == "ok":
            name = worker["surname"] + " " + worker["name"]
            
            # Окно подтверждения
            reply = QMessageBox.question(self, 'Подтверждение',
                                          f'Вы {name}?',
                                          QMessageBox.Yes | QMessageBox.No,
                                          QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.work_ui.updateName(name=name)
                self.tests_ui.updateName(name=name)
                self.packing_ui.updateName(name=name)
                self.mark_ui.updateName(name=name)
                self.stacked_widget.setCurrentWidget(self.work_page)
                auth = True                                                  # Возвращаем пользователя на страницу регистрации

    def manual_entry(self):
        entered_code = self.manual_input.text()
        print(f"Штрихкод введен вручную: {entered_code}")
        self.verify(entered_code)

    def start_scan(self):
        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.capture.isOpened():
            self.menu_ui.label.setText("Ошибка: камера не доступна")
            return

        self.running = True
        self.thread = threading.Thread(target=self.update_camera_feed)
        self.thread.start()

    def update_camera_feed(self):
        try:
            while self.running:
                if not self.capture.isOpened():
                    break

                ret, frame = self.capture.read()
                if not ret or frame is None:
                    continue

                # Resize the frame for display
                resized_frame = cv2.resize(frame, (300, 200))
                frame_rgb = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
                height, width, channel = frame_rgb.shape
                bytes_per_line = 3 * width
                q_image = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)

                self.camera_feed.setPixmap(QPixmap.fromImage(q_image))

                # Detect barcodes using pyzbar, excluding PDF417
                decoded_objects = decode(frame, symbols=[ZBarSymbol.CODE128, ZBarSymbol.QRCODE])
                for obj in decoded_objects:
                    try:
                        data = obj.data.decode("utf-8")
                        print(f"Штрихкод: {data}")
                        self.verify(data)
                    except Exception as e:
                        print(f"Ошибка при декодировании: {e}")

        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            if self.capture.isOpened():
                self.capture.release()

    def init_login_page(self):
        layout = QVBoxLayout()
        self.login_page = QWidget()  # Ensure the login_page is initialized
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
            self.password_input.setStyleSheet("font: 16px; padding: 10px; border: 2px solid red; border-radius: 5px;")
            self.error_message.setText("Неверный логин или пароль")

    def connect_header_buttons(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
