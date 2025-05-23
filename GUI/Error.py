from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
# --------------
from logger import log_event

class CustomDialog(QDialog):
    def __init__(self, error, type):
        super().__init__()
        self.setWindowTitle("Ошибка")
        
        # Устанавливаем размеры окна
        self.resize(400, 200)
        
        # Устанавливаем стиль с помощью CSS
        self.setStyleSheet("""
            QDialog {
                background-color: #f2f2f2;
                border: 2px solid #d9534f;
                border-radius: 10px;
            }
            QLabel {
                font-size: 16px;
                color: #d9534f;
                padding: 20px;
                text-align: center;
            }
            QPushButton {
                background-color: #d9534f;
                color: white;
                font-size: 14px;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #c9302c;
            }
        """)

        layout = QVBoxLayout()
        log_event("Вызванно окно ошибки")

        # Создаем элементы интерфейса
        label = QLabel(f"Произошла ошибка:\n{error}")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        if type == "choice":

            # Кнопки "Да" и "Нет"
            button_yes = QPushButton("Да")
            button_no = QPushButton("Нет")
            button_yes.clicked.connect(self.accept)
            button_no.clicked.connect(self.reject)

                    # Добавляем кнопки в макет
            layout.addWidget(button_yes)
            layout.addWidget(button_no)
        else:
            button_ok = QPushButton("Хорошо")
            button_ok.clicked.connect(self.accept)

            layout.addWidget(button_ok)



        self.setLayout(layout)
