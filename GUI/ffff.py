from datetime import timedelta, datetime

utc = datetime.utcnow()
time_c = utc + timedelta(hours=5)

# Получаем только дату
date_part = time_c.date()


time_part = time_c.replace(microsecond=0).time()


print("Дата:", date_part)
print("Время:", time_part)



# from PySide6.QtWidgets import QApplication, QLabel
# from PySide6.QtCore import Qt
# import sys

# # Создание приложения
# app = QApplication(sys.argv)

# # Создание окна и метки с текстом
# label = QLabel("ХУЙ")
# label.setAlignment(Qt.AlignCenter)  # Центрирование текста

# # Настройка большого шрифта
# label.setStyleSheet("""
#     QLabel {
#         font-size: 150px;            /* Размер шрифта */
#         font-weight: bold;           /* Полужирный текст */
#         color: red;                  /* Цвет текста */
#         background-color: black;     /* Фон */
#     }
# """)

# # Открываем окно на весь экран
# label.showFullScreen()

# # Запуск приложения
# sys.exit(app.exec())
