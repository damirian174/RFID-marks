import config

config.work = 123
print(config.work)



from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import Qt
import sys

# Создание приложения
app = QApplication(sys.argv)

# Создание окна и метки с текстом
label = QLabel("ХУЙ")
label.setAlignment(Qt.AlignCenter)  # Центрирование текста

# Настройка большого шрифта
label.setStyleSheet("""
    QLabel {
        font-size: 150px;            /* Размер шрифта */
        font-weight: bold;           /* Полужирный текст */
        color: red;                  /* Цвет текста */
        background-color: black;     /* Фон */
    }
""")

# Открываем окно на весь экран
label.showFullScreen()

# Запуск приложения
sys.exit(app.exec())
