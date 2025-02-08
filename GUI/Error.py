from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QWidget
from PySide6.QtCore import Qt  # Импортируем Qt для использования выравнивания
import sys
class CustomDialog(QDialog):
    def __init__(self, error):
        super().__init__()
        self.setWindowTitle("Ошибка")
        
        # Устанавливаем размеры окна
        self.resize(400, 200)  # Ширина 400, высота 200
        
        # Устанавливаем стиль с помощью CSS
        self.setStyleSheet("""
            QDialog {
                background-color: #f2f2f2;  /* Светлый фон */
                border: 2px solid #d9534f;   /* Красная рамка */
                border-radius: 10px;         /* Закругленные углы */
            }
            QLabel {
                font-size: 16px;              /* Размер шрифта */
                color: #d9534f;               /* Цвет текста */
                padding: 20px;                /* Отступы */
                text-align: center;           /* Центрирование текста */
            }
            QPushButton {
                background-color: #d9534f;    /* Цвет кнопки */
                color: white;                  /* Цвет текста кнопки */
                font-size: 14px;               /* Размер шрифта кнопки */
                border: none;                  /* Убираем рамку */
                border-radius: 5px;           /* Закругленные углы кнопки */
                padding: 10px;                 /* Отступы кнопки */
            }
            QPushButton:hover {
                background-color: #c9302c;    /* Цвет кнопки при наведении */
            }
        """)

        layout = QVBoxLayout()

        label = QLabel(f"Произошла ошибка:\n{error}")
        label.setAlignment(Qt.AlignCenter)  # Центрируем текст
        layout.addWidget(label)

        button = QPushButton("Ок")
        button.clicked.connect(self.accept)  # Закрывает диалог
        layout.addWidget(button)

        self.setLayout(layout)


if __name__ == '__main__':


    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Главное окно")

    layout = QVBoxLayout()
    button = QPushButton("Показать диалог")
    button.clicked.connect(lambda: CustomDialog('1231233123').exec())

    layout.addWidget(button)
    window.setLayout(layout)

    window.show()
    sys.exit(app.exec())