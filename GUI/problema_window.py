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
    dialog.setFixedSize(500, 400)
    dialog.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)  # Устанавливаем флаги для независимого окна
    dialog.setStyleSheet("""
        QDialog {
            background-color: #f5f7fa;
            border-radius: 12px;
        }
        QLabel {
            color: black;
            font-size: 16px;
        }
        QLabel#error_label {
            color: red;
            font-size: 14px;
        }
        QPushButton {
            background-color: #4e9af1;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-size: 14px;
            min-width: 100px;
        }
        QPushButton:hover {
            background-color: #3a85d8;
        }
        QTextEdit {
            border: 1px solid #bdc3c7;
            border-radius: 6px;
            padding: 10px;
            font-size: 14px;
            background-color: white;
            color: black;
        }
    """)
    
    layout = QVBoxLayout()
    layout.setContentsMargins(30, 30, 30, 30)
    layout.setSpacing(20)
    
    title_label = QLabel("Опишите вашу проблему")
    title_label.setFont(QFont("Arial", 16, QFont.Bold))
    title_label.setAlignment(Qt.AlignCenter)
    
    problem_input = QTextEdit()
    problem_input.setPlaceholderText("Введите описание проблемы здесь...")
    problem_input.setMinimumHeight(200)
    
    # Добавляем метку для сообщения об ошибке
    error_label = QLabel("")
    error_label.setObjectName("error_label")
    error_label.setAlignment(Qt.AlignCenter)
    error_label.setVisible(False)  # Изначально скрыта
    
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
        
        # Отправляем данные в базу
        if database.database(data):
            # Устанавливаем флаг проблемы в конфиге
            config.problem = True
            
            input_dialog.close()
            wait_dialog_global = init_wait_dialog()
            wait_dialog_global.exec()  # Используем exec() вместо show() для блокирующего режима
        else:
            # Если возникла ошибка при отправке в базу данных
            error_label.setText("Ошибка отправки. Попробуйте еще раз.")
            error_label.setVisible(True)
    else:
        # Показываем предупреждение, что поле не может быть пустым
        error_label.setText("Поле не может быть пустым")
        error_label.setVisible(True)

def init_wait_dialog():
    dialog = QDialog()
    dialog.setWindowTitle("Ожидание")
    dialog.setFixedSize(400, 200)
    dialog.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)  # Устанавливаем флаги для независимого окна
    dialog.setStyleSheet("""
        QDialog {
            background-color: #f5f7fa;
            border-radius: 12px;
        }
        QLabel {
            color: black;
            font-size: 16px;
        }
        QPushButton {
            background-color: #4e9af1;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-size: 14px;
            min-width: 100px;
        }
        QPushButton:hover {
            background-color: #3a85d8;
        }
    """)
    
    layout = QVBoxLayout()
    layout.setContentsMargins(30, 30, 30, 30)
    layout.setSpacing(20)
    
    title_label = QLabel("Проблема отправлена")
    title_label.setFont(QFont("Arial", 16, QFont.Bold))
    title_label.setAlignment(Qt.AlignCenter)
    
    desc_label = QLabel("Ожидайте прихода администратора")
    desc_label.setFont(QFont("Arial", 12))
    desc_label.setAlignment(Qt.AlignCenter)
    desc_label.setWordWrap(True)
    
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
    dialog.setFixedSize(400, 300)
    dialog.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)  # Устанавливаем флаги для независимого окна
    dialog.setStyleSheet("""
        QDialog {
            background-color: #f5f7fa;
            border-radius: 12px;
        }
        QLabel {
            color: black;
            font-size: 16px;
        }
        QPushButton {
            background-color: #4e9af1;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-size: 14px;
            min-width: 100px;
        }
        QPushButton:hover {
            background-color: #3a85d8;
        }
    """)
    
    layout = QVBoxLayout()
    layout.setContentsMargins(30, 30, 30, 30)
    layout.setSpacing(25)
    
    icon_label = QLabel()
    icon_label.setPixmap(QIcon.fromTheme("dialog-ok").pixmap(64, 64))
    icon_label.setAlignment(Qt.AlignCenter)
    
    title_label = QLabel("Ваша проблема успешно отправлена!")
    title_label.setFont(QFont("Arial", 16, QFont.Bold))
    title_label.setAlignment(Qt.AlignCenter)
    
    desc_label = QLabel("Ожидайте отклика администратора")
    desc_label.setFont(QFont("Arial", 12))
    desc_label.setAlignment(Qt.AlignCenter)
    
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