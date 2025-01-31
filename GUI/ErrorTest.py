import sys
import config
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QWidget
from PySide6.QtCore import QRect, QCoreApplication

from button import MainApp as init_login_page  # Окно аутентификации
from Mark import Ui_MainWindow  # Главное меню

class ErrorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("ErrorWindow")
        self.resize(1000, 800)
        self.setStyleSheet("background-color: rgb(235, 240, 255);")

        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        # Кнопка "Вернуться на главную" (Выход)
        self.pushButton = QPushButton(" < Вернуться на главную", self.centralwidget)
        self.pushButton.setGeometry(QRect(50, 30, 250, 60))
        self.pushButton.setStyleSheet(
            "background-color: #5F7ADB;"
            "color: rgb(255, 255, 255);"
            "font: 20px;"
            "font-weight: 600;"
            "border-radius: 15px;"
        )
        self.pushButton.clicked.connect(self.handle_exit)

        # Текст ошибки
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QRect(250, 300, 500, 200))
        self.label.setStyleSheet(
            "background-color: #5F7ADB;"
            "color: rgb(255, 255, 255);"
            "font: 20px;"
            "font-weight: 600;"
            "border-radius: 25px;"
        )

        self.label_2 = QLabel("Произошла ошибка!", self.centralwidget)
        self.label_2.setGeometry(QRect(400, 330, 200, 35))
        self.label_2.setStyleSheet("color: rgb(255, 255, 255); font: 20px; font-weight: 600;")

        self.label_3 = QLabel("Попробуйте заново запустить программу", self.centralwidget)
        self.label_3.setGeometry(QRect(300, 390, 400, 40))
        self.label_3.setStyleSheet("color: rgb(255, 255, 255); font: 20px; font-weight: 600;")

    def handle_exit(self):
        """ Закрывает текущее окно и открывает нужное в зависимости от config.auth """
        self.close()
        self.open_next_window()

    def open_next_window(self):
        """ Открывает главное меню или окно аутентификации """
        self.window = QMainWindow()
        self.ui = Ui_MainWindow() if config.auth else init_login_page()
        self.ui.setupUi(self.window)
        self.window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ErrorWindow()
    window.show()
    sys.exit(app.exec())

