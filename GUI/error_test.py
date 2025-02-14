import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget
from Error import CustomDialog  # Импортируем диалог из другого файла

def show_error_dialog(text, type):
    dialog = CustomDialog(text, type)
    if dialog.exec():  # Ждет ответа от пользователя
        return True
    else:
        return False

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
