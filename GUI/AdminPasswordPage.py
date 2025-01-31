from PySide6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Qt


class Ui_AdminPasswordPage:
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("Админ Панель")
        MainWindow.setGeometry(100, 100, 400, 200)

        # Центральный виджет
        self.central_widget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.central_widget)

        # Макет
        layout = QVBoxLayout(self.central_widget)

        # Кнопка "Назад"
        self.back_button = QPushButton("Назад")
        self.back_button.setStyleSheet("font: 16px; font-weight: bold;")
        self.back_button.setFixedSize(100, 40)
        layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        # Поле ввода пароля
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                font: 16px;
                padding: 8px;
                border: 2px solid #BDBDBD;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.password_input, alignment=Qt.AlignCenter)

        # Ошибка
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red; font: 14px;")
        self.error_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.error_label)

        # Кнопка "Подтвердить"
        self.confirm_button = QPushButton("Подтвердить")
        self.confirm_button.setStyleSheet("""
            QPushButton {
                font: 16px;
                font-weight: bold;
                background-color: #5F7ADB;
                color: white;
                border-radius: 8px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #4156a6;
            }
        """)
        layout.addWidget(self.confirm_button, alignment=Qt.AlignCenter)