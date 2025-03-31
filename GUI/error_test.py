import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QMessageBox
from Error import CustomDialog  # Импортируем диалог из другого файла
from PySide6.QtGui import QIcon
import os
from logger import log_error

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

def show_error_dialog(title, message):
    """
    Показывает пользователю диалог с сообщением об ошибке
    """
    log_error(f"Ошибка: {title} - {message}")
    error_dialog = QMessageBox()
    error_dialog.setWindowTitle(title)
    error_dialog.setText(message)
    
    # Устанавливаем иконку
    icon_path = get_icon_path("favicon.ico")
    error_dialog.setWindowIcon(QIcon(icon_path))
    
    error_dialog.setIcon(QMessageBox.Critical)
    error_dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Главное окно приложения
    window = QWidget()
    window.setWindowTitle("Главное окно")

    layout = QVBoxLayout()
    button = QPushButton("Показать диалог")
    button.clicked.connect(show_error_dialog)

    layout.addWidget(button)
    window.setLayout(layout)

    window.show()
    sys.exit(app.exec())
