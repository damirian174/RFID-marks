from PySide6.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QPushButton, QTextEdit, QScrollArea, QMessageBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QPixmap, QIcon
import sys
import config  # Импортируем конфиг
import database  # Импортируем модуль работы с базой данных
from datetime import datetime

# Глобальная переменная для хранения окна ожидания
wait_dialog_global = None
problem_dialog_global = None

def init_problem_input():
    dialog = QDialog()
    dialog.setWindowTitle("Отправка проблемы")
    dialog.setFixedSize(650, 500)  # Увеличиваем размер окна
    dialog.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)  # Устанавливаем флаги для независимого окна
    dialog.setStyleSheet("""
        QDialog {
            background-color: #f8f9fa;
            border-radius: 15px;
            border: 2px solid #0056b3;
        }
        QLabel {
            color: #212529;
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 10px;
        }
        QLabel#error_label {
            color: #dc3545;
            font-size: 14px;
            font-weight: bold;
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 4px;
            padding: 8px;
            margin-top: 5px;
        }
        QPushButton {
            background-color: #0056b3;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 6px;
            font-size: 15px;
            font-weight: bold;
            min-width: 140px;
        }
        QPushButton:hover {
            background-color: #0069d9;
        }
        QPushButton:pressed {
            background-color: #004494;
        }
        QTextEdit {
            border: 1px solid #ced4da;
            border-radius: 8px;
            padding: 15px;
            font-size: 15px;
            background-color: white;
            color: #212529;
            min-height: 240px;
            selection-background-color: #0056b3;
            selection-color: white;
        }
        QTextEdit:focus {
            border: 2px solid #0056b3;
        }
    """)
    
    layout = QVBoxLayout()
    layout.setContentsMargins(50, 50, 50, 50)
    layout.setSpacing(25)
    
    title_label = QLabel("Опишите вашу проблему")
    title_label.setFont(QFont("Arial", 20, QFont.Bold))
    title_label.setAlignment(Qt.AlignCenter)
    title_label.setWordWrap(True)
    
    problem_input = QTextEdit()
    problem_input.setPlaceholderText("Введите описание проблемы здесь...")
    problem_input.setMinimumHeight(240)
    
    # Добавляем метку для сообщения об ошибке
    error_label = QLabel("")
    error_label.setObjectName("error_label")
    error_label.setAlignment(Qt.AlignCenter)
    error_label.setVisible(False)  # Изначально скрыта
    error_label.setWordWrap(True)
    
    send_button = QPushButton("Отправить")
    send_button.clicked.connect(lambda: handle_problem_submission(dialog, problem_input.toPlainText(), error_label))
    
    # Скрываем сообщение об ошибке при вводе текста
    problem_input.textChanged.connect(lambda: error_label.setVisible(False))
    
    layout.addWidget(title_label)
    layout.addWidget(problem_input)
    layout.addWidget(error_label)  # Добавляем метку в макет
    layout.addWidget(send_button, alignment=Qt.AlignCenter)
    
    dialog.setLayout(layout)
    return dialog

def handle_problem_submission(input_dialog, problem_text, error_label):
    if problem_text.strip():
        global wait_dialog_global
        
        # Получаем текущее время
        current_time = datetime.now()
        time_str = current_time.strftime("%Y-%m-%d %H:%M")
        
        # Формируем данные для отправки в базу данных
        data = {
            "type": "report",  
            "text": problem_text,  
            "time": time_str,  
            "name": config.user if config.user else "Неизвестный пользователь"
        }
        
        # Отправляем данные синхронно
        result = database(data)
        if result:
            # Устанавливаем флаг проблемы в конфиге
            config.problem = True
            
            input_dialog.close()
            global wait_dialog_global
            wait_dialog_global = init_wait_dialog()
            wait_dialog_global.exec()  # Используем exec() вместо show() для блокирующего режима
        else:
            error_label.setText("Ошибка отправки: Не удалось отправить данные")
            error_label.setVisible(True)
    else:
        # Показываем предупреждение, что поле не может быть пустым
        error_label.setText("Поле не может быть пустым")
        error_label.setVisible(True)

def init_wait_dialog():
    dialog = QDialog()
    dialog.setWindowTitle("Ожидание")
    dialog.setFixedSize(550, 300)  # Увеличим размер окна
    dialog.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)  # Устанавливаем флаги для независимого окна
    dialog.setStyleSheet("""
        QDialog {
            background-color: #f8f9fa;
            border-radius: 15px;
            border: 2px solid #0056b3;
        }
        QLabel {
            color: #212529;
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 10px;
        }
        QLabel#title_label {
            color: #0056b3;
            font-size: 24px;
            font-weight: bold;
        }
        QLabel#desc_label {
            color: #495057;
            font-size: 16px;
            background-color: #e9ecef;
            padding: 15px;
            border-radius: 8px;
        }
        QPushButton {
            background-color: #0056b3;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 6px;
            font-size: 15px;
            font-weight: bold;
            min-width: 140px;
        }
        QPushButton:hover {
            background-color: #0069d9;
        }
        QPushButton:pressed {
            background-color: #004494;
        }
    """)
    
    layout = QVBoxLayout()
    layout.setContentsMargins(50, 50, 50, 50)
    layout.setSpacing(30)
    
    title_label = QLabel("Проблема отправлена")
    title_label.setObjectName("title_label")
    title_label.setFont(QFont("Arial", 22, QFont.Bold))
    title_label.setAlignment(Qt.AlignCenter)
    
    desc_label = QLabel("Ожидайте прихода администратора")
    desc_label.setObjectName("desc_label")
    desc_label.setFont(QFont("Arial", 16))
    desc_label.setAlignment(Qt.AlignCenter)
    desc_label.setWordWrap(True)  # Добавим перенос текста
    
    close_button = QPushButton("Закрыть")
    close_button.clicked.connect(dialog.close)
    
    layout.addWidget(title_label)
    layout.addWidget(desc_label)
    layout.addStretch()
    layout.addWidget(close_button, alignment=Qt.AlignCenter)
    
    dialog.setLayout(layout)
    return dialog

def init_problem():
    dialog = QDialog()
    dialog.setWindowTitle("Успешно")  
    dialog.setFixedSize(550, 380)  # Увеличим размер окна
    dialog.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)  # Устанавливаем флаги для независимого окна
    dialog.setStyleSheet("""
        QDialog {
            background-color: #f8f9fa;
            border-radius: 15px;
            border: 2px solid #0056b3;
        }
        QLabel {
            color: #212529;
            font-size: 16px;
            line-height: 1.6;
        }
        QLabel#title_label {
            color: #0056b3;
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 15px;
        }
        QLabel#desc_label {
            color: #495057;
            font-size: 16px;
            background-color: #e9ecef;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
        }
        QPushButton {
            background-color: #0056b3;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 6px;
            font-size: 15px;
            font-weight: bold;
            min-width: 140px;
        }
        QPushButton:hover {
            background-color: #0069d9;
        }
        QPushButton:pressed {
            background-color: #004494;
        }
    """)
    
    layout = QVBoxLayout()
    layout.setContentsMargins(50, 50, 50, 50)
    layout.setSpacing(30)
    
    icon_label = QLabel()
    success_icon = QIcon.fromTheme("dialog-ok")
    if not success_icon.isNull():
        icon_label.setPixmap(success_icon.pixmap(80, 80))
    else:
        # Создаем текстовый заменитель иконки если системная иконка недоступна
        icon_label.setText("✓")
        icon_label.setStyleSheet("font-size: 64px; color: #28a745;")
    icon_label.setAlignment(Qt.AlignCenter)
    
    title_label = QLabel("Ваша проблема успешно отправлена!")
    title_label.setObjectName("title_label")
    title_label.setFont(QFont("Arial", 20, QFont.Bold))
    title_label.setAlignment(Qt.AlignCenter)
    title_label.setWordWrap(True)  # Добавим перенос текста
    
    desc_label = QLabel("Ожидайте отклика администратора")
    desc_label.setObjectName("desc_label")
    desc_label.setFont(QFont("Arial", 16))
    desc_label.setAlignment(Qt.AlignCenter)
    desc_label.setWordWrap(True)  # Добавим перенос текста
    
    close_button = QPushButton("Закрыть")
    close_button.clicked.connect(dialog.close)
    
    layout.addWidget(icon_label)
    layout.addWidget(title_label)
    layout.addWidget(desc_label)
    layout.addStretch()
    layout.addWidget(close_button, alignment=Qt.AlignCenter)
    
    dialog.setLayout(layout)
    return dialog

# Функция для вызова из основного проекта
def show_problem_dialog(parent=None):
    """
    Функция для отображения окна отправки проблемы или окна ожидания.
    Вызывайте эту функцию при нажатии на кнопку "Сообщить о проблеме" в основном проекте.
    
    Args:
        parent: Родительское окно (не используется, оставлено для совместимости)
    """
    global problem_dialog_global, wait_dialog_global
    
    # Если уже есть активная проблема, показываем окно ожидания
    if config.problem:
        wait_dialog_global = init_wait_dialog()
        # Не устанавливаем родителя, чтобы окно было независимым
        wait_dialog_global.exec()
        return wait_dialog_global
    else:
        # Иначе показываем окно ввода проблемы
        problem_dialog_global = init_problem_input()
        # Не устанавливаем родителя, чтобы окно было независимым
        problem_dialog_global.show()
        return problem_dialog_global

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  
    
    # Проверяем, есть ли уже активная проблема
    if config.problem:
        dialog = init_wait_dialog()
    else:
        dialog = init_problem_input()
        
    dialog.show()
    
    sys.exit(app.exec()) 