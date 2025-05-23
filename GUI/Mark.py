# -*- coding: utf-8 -*-
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QLayout,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget, QMessageBox, QDialog, QProgressBar, QHBoxLayout, QDialogButtonBox, QTextEdit, )
from detail_work import end_work, pause_work, couintine_work, update, zakurit
import serial
from PySide6.QtCore import QThread, Signal, QTimer
import time
import sys
import os
import serial
import serial.tools.list_ports
# import button
import database
from datetime import datetime
from logger import log_event, log_error
from COM import *
from problema_window import show_problem_dialog  # Импорт функции для показа окна проблемы


class SerialWorker(QThread):
    finished = Signal(bool, str)
    status_update = Signal(str)
    
    def __init__(self, text, serial_manager):
        super().__init__()
        self.text = text.ljust(16)[:16]
        self.serial_manager = serial_manager
        self.ser = serial_manager.get_serial()
        self.timeout = 20

    def run(self):
        try:
            self.status_update.emit(f"Отправляю данные...")
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            
            data_to_send = f"w{self.text.strip()}_detail..............\n"
            log_event(f"Send to write {data_to_send.strip()}")
            self.status_update.emit(f"Отправляю: '{data_to_send.strip()}'")

            self.ser.write(data_to_send.encode('utf-8'))
            self.ser.flush()  

            start_time = time.time()
            while time.time() - start_time < self.timeout:
                if self.ser.in_waiting:
                    line = self.ser.readline().decode('utf-8').strip()
                    self.status_update.emit(f"Получено: '{line}'")
                    if "Поднесите карту для записи данных" in line:
                        self.status_update.emit(line)
                        log_event("Ожидание карты подтверждено")
                        continue
                    if "WRITE_SUCCESS" in line:
                        self.finished.emit(True, "Успех!")
                        log_event("Успешная запись на метку")
                        return
                    elif "WRITE_ERROR" in line:
                        self.finished.emit(False, "Ошибка МЭТР")
                        log_error("Ошибка МЭТР")
                        return
                time.sleep(0.1)

            self.finished.emit(False, "Таймаут ответа")

        except serial.SerialException as e:
            self.finished.emit(False, f"Ошибка порта: {str(e)}")
            log_error(f"Ошибка при работе с COM портом: {e}")
        except Exception as e:
            self.finished.emit(False, f"Неизвестная ошибка: {str(e)}")
            log_error(f"Неизвестная ошибка: {str(e)}")


class AdaptiveMark(QMainWindow):
    """
    Расширенное главное окно с поддержкой адаптивных элементов
    и шрифтов, которые изменяются в зависимости от размера окна.
    """
    def __init__(self, serial_manager=None):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, serial_manager)
        self.adjustFontSizes()  # Начальное применение размеров шрифтов
        
    def resizeEvent(self, event):
        """Обрабатываем изменение размера окна"""
        super().resizeEvent(event)
        self.adjustFontSizes()
        
    def adjustFontSizes(self):
        """Устанавливаем размеры шрифтов в зависимости от размера окна"""
        window_width = self.width()
        window_height = self.height()
        
        # Вычисляем базовый размер шрифта (2.5% от меньшей стороны окна)
        base_font_size = min(window_width, window_height) * 0.025
        
        # Устанавливаем размеры для разных типов текста
        header_size = max(18, int(base_font_size * 1.8))  # Шапка
        title_size = max(16, int(base_font_size * 1.6))   # Заголовки
        normal_size = max(14, int(base_font_size * 1.2))  # Обычный текст
        button_size = max(14, int(base_font_size * 1.1))  # Кнопки
        
        # Применяем шрифты к элементам интерфейса
        # Кнопки шапки
        header_font = QFont()
        header_font.setPointSize(header_size)
        header_font.setBold(True)
        
        button_font = QFont()
        button_font.setPointSize(button_size)
        button_font.setBold(True)
        
        title_font = QFont()
        title_font.setPointSize(title_size)
        title_font.setBold(True)
        
        normal_font = QFont()
        normal_font.setPointSize(normal_size)
        
        # Применяем шрифты к элементам UI
        # Шапка и кнопки навигации
        for btn in [self.ui.pushButton_2, self.ui.pushButton_5, self.ui.pushButton_6,
                   self.ui.pushButton_7, self.ui.pushButton_8]:
            btn.setFont(header_font)
            btn.setStyleSheet(f"""
            QPushButton {{
                color: #FFFFFF;
                font-size: {header_size}px;
                background-color: #004B8D;
                font-weight: 700;
            }}
            QPushButton:hover {{
                background-color: #4A6ED9;
            }}
            """)
        
        # Заголовки секций
        for label in [self.ui.label_2]:
            if hasattr(self.ui, 'label_2'):
                label.setFont(title_font)
                label.setStyleSheet(f"font-size: {title_size}px; font-weight: 600; color: black;")
        
        # Инфо метки
        for label in [self.ui.name, self.ui.label_4, self.ui.label_5,
                      self.ui.label_6, self.ui.label_7, self.ui.label_8]:
            if hasattr(self.ui, label.objectName()):
                label.setFont(normal_font)
                style = label.styleSheet()
                style = style.replace("font-size: 18px;", f"font-size: {normal_size}px;")
                label.setStyleSheet(style)
        
        # Кнопки действий
        for btn in [self.ui.pushButton, self.ui.pushButton_3, 
                    self.ui.pushButton_4, self.ui.pushButton_9]:
            if hasattr(self.ui, btn.objectName()):
                btn.setFont(button_font)
                style = btn.styleSheet()
                style = style.replace("font-size: 18px;", f"font-size: {button_size}px;")
                btn.setStyleSheet(style)
        
        # Логирование изменений
        log_event(f"Mark: размер окна изменен: {window_width}x{window_height}, шрифты: {header_size}/{title_size}/{normal_size}px")


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, serial_manager=None):
        self.serial_manager = serial_manager
        if self.serial_manager is None:
            log_error("SerialManager не передан! COM-порт не будет работать.")
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")

        MainWindow.resize(1300, 750)
        MainWindow.setStyleSheet(u"background-color:rgb(255, 255, 255)")
        # Центральный виджет
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        # Основной вертикальный макет
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setFixedHeight(50)  # Фиксированная высота шапки
        self.widget.setStyleSheet(u"""
        color: #FFFFFF;
        font: 20px;
        background-color: #004B8D;
        font-weight: 700;
        """)

        # Горизонтальный макет для шапки
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы
        self.horizontalLayout.setSpacing(0)  # Убираем промежутки между элементами

        # Логотип (фиксированный размер)
        self.widget_7 = QWidget(self.widget)
        self.widget_7.setObjectName(u"widget_7")
        self.widget_7.setFixedSize(210, 50)  # Фиксированный размер логотипа
        self.label_9 = QLabel(self.widget_7)
        self.label_9.setObjectName(u"label_9")
        image_path = self.get_image_path("new_logo.jpg")
        self.label_9.setPixmap(QPixmap(image_path))
        self.horizontalLayout.addWidget(self.widget_7)

        # Кнопки шапки (адаптируются по ширине)
        self.pushButton_7 = QPushButton(self.widget)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setText(u"Маркировка")
        self.pushButton_7.setFixedHeight(50)
        self.pushButton_7.setStyleSheet(u"""
        QPushButton {
                color: #FFFFFF;\n"
"font: 20px;\n"
"background-color: #004B8D;\n"
"font-weight: 700;\n"
        }
        """)
        self.horizontalLayout.addWidget(self.pushButton_7)

        self.pushButton_8 = QPushButton(self.widget)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setText(u"Сборка")
        self.pushButton_8.setFixedHeight(50)
        self.pushButton_8.setStyleSheet(u"""
        QPushButton {
                color: #FFFFFF;\n"
"font: 20px;\n"
"background-color: #004B8D;\n"
"font-weight: 700;\n"
        }
        """)
        self.horizontalLayout.addWidget(self.pushButton_8)

        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setText(u"Тестирование")
        self.pushButton_2.setFixedHeight(50)
        self.pushButton_2.setStyleSheet(u"""
        QPushButton {
                color: #FFFFFF;\n"
"font: 20px;\n"
"background-color: #004B8D;\n"
"font-weight: 700;\n"
        }
        """)
        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton_5 = QPushButton(self.widget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setText(u"Упаковка")
        self.pushButton_5.setFixedHeight(50)
        self.pushButton_5.setStyleSheet(u"""
        QPushButton {
                color: #FFFFFF;\n"
"font: 20px;\n"
"background-color: #004B8D;\n"
"font-weight: 700;\n"
}
        """)
        self.horizontalLayout.addWidget(self.pushButton_5)

        self.pushButton_6 = QPushButton(self.widget)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setText(u"Админ панель")
        self.pushButton_6.setFixedHeight(50)
        self.pushButton_6.setStyleSheet(u"""
                QPushButton {
                color: #FFFFFF;\n"
"font: 20px;\n"
"background-color: #004B8D;\n"
"font-weight: 700;\n"
}
        """)
        self.horizontalLayout.addWidget(self.pushButton_6)

        # Добавляем шапку в основной макет
        self.verticalLayout.addWidget(self.widget)

        # Основной контент (горизонтальный макет)
        self.horizontalLayoutMain = QHBoxLayout()
        self.horizontalLayoutMain.setSpacing(0)

        # Левая панель (Ввод данных)
        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setStyleSheet(u"background-color: rgb(235, 240, 255);")
        self.verticalLayoutLeft = QVBoxLayout(self.widget_2)
        self.verticalLayoutLeft.setContentsMargins(20, 20, 20, 20)
        self.verticalLayoutLeft.setSpacing(15)

        # Добавляем label_2 в верхнюю часть левой панели
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setText(u"Василий Пупкин")
        self.label_2.setFixedHeight(45)
        self.label_2.setStyleSheet(u"""
            font: 30px;
            font-weight: 600;
            color: black;
        """)
        self.label_2.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Выравнивание по левому краю
        self.verticalLayoutLeft.addWidget(self.label_2)

        # Остальные элементы левой панели
        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font-size: 18px; font-weight: 600;")
        self.label.setText(u"Введите категорию детали:")
        self.verticalLayoutLeft.addWidget(self.label)

        self.lineEdit = QLineEdit(self.widget_2)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setStyleSheet(u"""
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border-radius: 10px;
                border: 1px solid #ccc;
            }
        """)
        self.verticalLayoutLeft.addWidget(self.lineEdit)

        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"font-size: 18px; font-weight: 600;")
        self.label_3.setText(u"Введите маркировку товара:")
        self.verticalLayoutLeft.addWidget(self.label_3)

        self.comboBox = QComboBox(self.widget_2)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.addItems(["МЕТРАН 150", "МЕТРАН 75", "МЕТРАН 55"])
        self.comboBox.setStyleSheet(u"""
            QComboBox {
                font-size: 16px;
                padding: 10px;
                border-radius: 10px;
                border: 1px solid #ccc;
            }
        """)
        self.verticalLayoutLeft.addWidget(self.comboBox)

        self.label_4 = QLabel(self.widget_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"font-size: 18px; font-weight: 600;")
        self.label_4.setText(u"Метка детали:")
        self.verticalLayoutLeft.addWidget(self.label_4)

        self.lineEdit_3 = QLineEdit(self.widget_2)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setStyleSheet(u"""
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border-radius: 10px;
                border: 1px solid #ccc;
            }
        """)
        self.verticalLayoutLeft.addWidget(self.lineEdit_3)

        self.pushButton = QPushButton(self.widget_2)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"""
            QPushButton {
                background-color: #5F7ADB;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 15px;
                padding: 10px 20px;
            }
        """)
        self.pushButton.setText(u"Внести деталь")
        self.pushButton.clicked.connect(self.open_confirmation_window)
        self.verticalLayoutLeft.addWidget(self.pushButton, alignment=Qt.AlignCenter)

        # Добавляем левую панель в основной макет
        self.horizontalLayoutMain.addWidget(self.widget_2, stretch=15)
        # Центральная панель (Действия)
        self.widget_3 = QWidget(self.centralwidget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setStyleSheet(u"background-color: rgb(235, 240, 255);")
        self.verticalLayoutCenter = QVBoxLayout(self.widget_3)
        self.verticalLayoutCenter.setContentsMargins(20, 20, 20, 20)
        self.verticalLayoutCenter.setSpacing(15)

        self.pushButton_4 = QPushButton(self.widget_3)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setStyleSheet(u"""
            QPushButton {
                background-color: #2E3239;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 15px;
                padding: 10px 20px;
            }
        """)
        self.pushButton_4.setText(u"Сообщить о проблеме")
        self.verticalLayoutCenter.addWidget(self.pushButton_4)

        self.pushButton_3 = QPushButton(self.widget_3)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setStyleSheet(u"""
            QPushButton {
                background-color: #2E3239;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 15px;
                padding: 10px 20px;
            }
        """)
        self.pushButton_3.setText(u"Сообщить о браке")
        self.verticalLayoutCenter.addWidget(self.pushButton_3)
        self.pushButton_3.clicked.connect(self.kocak)

        self.pushButton_9 = QPushButton(self.widget_3)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setStyleSheet(u"""
            QPushButton {
                background-color: #2E3239;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 15px;
                padding: 10px 20px;
            }
        """)
        self.pushButton_9.setText(u"Завершить работу")
        self.verticalLayoutCenter.addWidget(self.pushButton_9)

        self.pushButton_15 = QPushButton(self.widget_3)
        self.pushButton_15.setObjectName(u"pushButton_15")
        self.pushButton_15.setStyleSheet(u"""
            QPushButton {
                background-color: #2E3239;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 15px;
                padding: 10px 20px;
            }
        """)
        self.pushButton_15.setText(u"Отойти")
        self.pushButton_15.clicked.connect(self.away)
        self.verticalLayoutCenter.addWidget(self.pushButton_15)

        self.horizontalLayoutMain.addWidget(self.widget_3, stretch=10)

        # Правая панель (Информация о детали)
        self.widget_5 = QWidget(self.centralwidget)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setStyleSheet(u"background-color: rgb(235, 240, 255);")
        self.verticalLayoutRight = QVBoxLayout(self.widget_5)
        self.verticalLayoutRight.setContentsMargins(20, 20, 20, 20)
        self.verticalLayoutRight.setSpacing(15)

        self.name = QLabel(self.widget_5)
        self.name.setObjectName(u"name")
        self.name.setStyleSheet(u"""
            background-color: #5F7ADB;
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 15px;
            padding: 10px;
        """)
        self.name.setAlignment(Qt.AlignCenter)
        self.name.setText(u"Отсканируй деталь")
        self.verticalLayoutRight.addWidget(self.name)

        self.serial = QLabel(self.widget_5)
        self.serial.setObjectName(u"serial")
        self.serial.setStyleSheet(u"""
            background-color: #5F7ADB;
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 15px;
            padding: 10px;
        """)
        self.serial.setAlignment(Qt.AlignCenter)
        self.serial.setText(u"Отсканируй деталь")
        self.verticalLayoutRight.addWidget(self.serial)

        self.defective = QLabel(self.widget_5)
        self.defective.setObjectName(u"defective")
        self.defective.setStyleSheet(u"""
            background-color: #5F7ADB;
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 15px;
            padding: 10px;
        """)
        self.defective.setAlignment(Qt.AlignCenter)
        self.defective.setText(u"Отсканируй деталь")
        self.verticalLayoutRight.addWidget(self.defective)

        self.stage = QLabel(self.widget_5)
        self.stage.setObjectName(u"stage")
        self.stage.setStyleSheet(u"""
            background-color: #5F7ADB;
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 15px;
            padding: 10px;
        """)
        self.stage.setAlignment(Qt.AlignCenter)
        self.stage.setText(u"Отсканируй деталь")
        self.verticalLayoutRight.addWidget(self.stage)

        self.sector = QLabel(self.widget_5)
        self.sector.setObjectName(u"sector")
        self.sector.setStyleSheet(u"""
            background-color: #5F7ADB;
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 15px;
            padding: 10px;
        """)
        self.sector.setAlignment(Qt.AlignCenter)
        self.sector.setText(u"Отсканируй деталь")
        self.verticalLayoutRight.addWidget(self.sector)

        self.horizontalLayoutMain.addWidget(self.widget_5, stretch=10)

        self.verticalLayout.addLayout(self.horizontalLayoutMain)
        # self.pushButton_9.clicked.connect(button.MainApp.setup_scan_page)
        self.pushButton_4.clicked.connect(self.init_problem)
        self.pushButton_3.clicked.connect(self.kocak)

        # Добавляем кнопку переподключения к МЭТР
        self.reconnect_btn = QPushButton("Переподключить МЭТР")
        self.reconnect_btn.setStyleSheet("""
            QPushButton {
                background-color: #004B8D;
                color: white;
                font-size: 14px;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #4A6ED9;
            }
        """)
        self.reconnect_btn.clicked.connect(self.reconnect_metr)
        
        # Добавляем в конец основной разметки
        self.verticalLayout.addWidget(self.reconnect_btn)
        
        # Подключение слотов
        QMetaObject.connectSlotsByName(MainWindow)

    def init_problem(self):
        # Вместо создания собственного диалога вызываем функцию из problema_window
        show_problem_dialog(self.centralwidget)

    def get_image_path(self, image_name):
        """
        Получение правильного пути к изображению в зависимости от того,
        запущено ли приложение как .exe или как скрипт.
        """
        if getattr(sys, 'frozen', False):
            # Если приложение запущено как .exe
            base_path = sys._MEIPASS
        else:
            # Если в режиме разработки
            base_path = os.path.abspath(".")

        # Формируем полный путь к изображению
        image_path = os.path.join(base_path, image_name)
        return image_path
    def find_metr(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "USB Serial Port" in port.description:
                return port.device
        return None
        
    def open_confirmation_window(self):
        # Создание окна подтверждения
        self.confirmation_window = QWidget()
        self.confirmation_window.setWindowTitle("Подтверждение данных")
        self.confirmation_window.setGeometry(375, 150, 250, 500)
        self.confirmation_window.setStyleSheet("background-color: #F0F0F0;")

        layout = QVBoxLayout(self.confirmation_window)
        layout.addWidget(QLabel(f"Категория детали: {self.lineEdit.text()}"))
        layout.addWidget(QLabel(f"Маркировка товара: {self.comboBox.currentText()}"))
        layout.addWidget(QLabel(f"Серийный номер: {self.lineEdit_3.text()}"))

        button_confirm = QPushButton("Данные верны")
        button_confirm.clicked.connect(self.confirm_data)
        layout.addWidget(button_confirm)

        button_edit = QPushButton("Изменить данные")
        button_edit.clicked.connect(self.edit_data)
        layout.addWidget(button_edit)
        log_event("окно подтверждения открыто")

        self.confirmation_window.show()
    

    def confirm_data(self):
        # Получаем данные из полей ввода
        category = self.lineEdit.text()
        marking = self.comboBox.currentText()
        serial_number = self.lineEdit_3.text()
        
        # Формируем текст для записи (пример формата)
        text_to_write = f"{serial_number}"
        log_event("Данные маркировки подтверждены")
        
        # Вызываем функцию записи
        self.write(text_to_write)
        
        # Очищаем поля и закрываем окно
        self.lineEdit.clear()
        self.lineEdit_3.clear()
        self.confirmation_window.close()

    def edit_data(self):
        self.confirmation_window.close()

    # Добавляем функцию для стилизации MessageBox
    def style_message_box(self, msg_box):
        """
        Применяет стилизацию к диалоговому окну с улучшенным дизайном
        """
        # Установим минимальную ширину и высоту для диалога
        msg_box.setMinimumWidth(500)
        msg_box.setMinimumHeight(250)
        
        # Найдем текстовую метку внутри диалога и установим перенос слов
        for child in msg_box.children():
            if isinstance(child, QLabel):
                child.setWordWrap(True)
                child.setMinimumWidth(450)
                child.setMinimumHeight(100)
                child.setTextFormat(Qt.PlainText)  # Использовать обычный текст без HTML
        
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #f8f9fa;
                border: 2px solid #0056b3;
                border-radius: 10px;
                min-width: 500px;
                min-height: 250px;
                padding: 20px;
            }
            QLabel {
                color: #212529;
                font-size: 16px;
                font-weight: bold;
                min-width: 450px;
                margin: 20px;
                padding: 10px;
                line-height: 1.6;
                background-color: #ffffff;
                border-radius: 8px;
                border: 1px solid #dee2e6;
            }
            QPushButton {
                background-color: #0056b3;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 25px;
                font-weight: bold;
                font-size: 14px;
                min-width: 120px;
                margin: 15px;
            }
            QPushButton:hover {
                background-color: #0069d9;
            }
            QPushButton:pressed {
                background-color: #004494;
            }
            QMessageBox QLabel#qt_msgbox_informativelabel {
                font-size: 14px;
                font-weight: normal;
                background-color: transparent;
                border: none;
                color: #495057;
                margin-top: 0;
            }
        """)
        return msg_box

    def away(self):
        self.centralwidget.setEnabled(False)
        pause_work()
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Отошел")
        msg_box.setText("Нажми, чтобы продолжить работать")
        msg_box.setStandardButtons(QMessageBox.Ok)
        self.style_message_box(msg_box)
        msg_box.buttonClicked.connect(self.countine)
        msg_box.exec()

    def countine(self):
        self.centralwidget.setEnabled(True)
        couintine_work()

    def detail(self, data=None):
        # Заполняем поля данными
        self.name.setText("")
        self.serial.setText("")
        self.defective.setText("")
        self.stage.setText("")
        self.sector.setText("")
        
        # Обработка данных без вызова getDetail
        if data:
            # Проверяем, пришел ли к нам объект data или False
            if data is not False:
                # Извлекаем данные напрямую из объекта
                name = data.get('name', '')
                serial = data.get('serial_number', '')
                defective = "Да" if data.get('defective', False) else "Нет"
                stage = data.get('stage', '')
                sector = data.get('sector', '')
                
                self.name.setText(str(name))
                self.serial.setText(str(serial))
                self.defective.setText(str(defective))
                self.stage.setText(str(stage))
                self.sector.setText(str(sector))
                self.change_color(2)
        else:
            # Если data = None или False, устанавливаем стандартный текст
            self.name.setText("Отсканируй деталь")
            self.serial.setText("Отсканируй деталь")
            self.defective.setText("Отсканируй деталь")
            self.stage.setText("Отсканируй деталь")
            self.sector.setText("Отсканируй деталь")
            
            # Напрямую устанавливаем стандартный синий цвет вместо вызова revert_color
            default_color = "#5F7ADB"
            style = f"background-color: {default_color}; color: white; font-size: 18px; font-weight: bold; border-radius: 15px; padding: 10px;"
            self.name.setStyleSheet(style)
            self.serial.setStyleSheet(style)
            self.defective.setStyleSheet(style)
            self.stage.setStyleSheet(style)
            self.sector.setStyleSheet(style)
        
        # Удаляем создание кнопки, так как она теперь создается в setupUi

    def change_color(self, status):
        if status == 2:
            # Зеленый фон – успешное состояние
            color = "#4CAF50"  # зеленый
        elif status == 1:
            # Красный фон – ошибка
            color = "#F44336"  # красный
        else:
            # Стандартный синий фон
            color = "#5F7ADB"
        style = f"background-color: {color}; color: white; font-size: 18px; font-weight: bold; border-radius: 15px; padding: 10px;"
        self.name.setStyleSheet(style)
        self.serial.setStyleSheet(style)
        self.defective.setStyleSheet(style)
        self.stage.setStyleSheet(style)
        self.sector.setStyleSheet(style)
        # Через 7 секунд вернуть стандартный цвет - используем полный путь
        QTimer.singleShot(7000, self.revert_color)

    def revert_color(self):
        # Стандартный синий фон
        default_color = "#5F7ADB"
        style = f"background-color: {default_color}; color: white; font-size: 18px; font-weight: bold; border-radius: 15px; padding: 10px;"
        self.name.setStyleSheet(style)
        self.serial.setStyleSheet(style)
        self.defective.setStyleSheet(style)
        self.stage.setStyleSheet(style)
        self.sector.setStyleSheet(style)

    def write(self, text):
        self.write_dialog = QDialog()
        self.write_dialog.setWindowTitle("Запись на метку")
        self.write_dialog.setGeometry(375, 150, 400, 200)  # Увеличено окно
        layout = QVBoxLayout()
        
        self.status_label = QLabel("Идет запись...")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Добавляем прогресс-бар
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)  # Индикатор процесса
        layout.addWidget(self.progress)
        
        self.write_dialog.setLayout(layout)
        self.write_dialog.setWindowModality(Qt.ApplicationModal)
        
        # Используем `serial_manager`, а не `find_metr()`
        self.serial_thread = SerialWorker(text, self.serial_manager)
        self.serial_thread.finished.connect(self.handle_write_result)
        self.serial_thread.status_update.connect(self.update_status)
        self.serial_thread.start()
        
        self.write_dialog.exec_()

    def update_status(self, message):
        self.status_label.setText(message)
        if "Поднесите карту" in message:
            self.progress.setRange(0, 0)  # Индикатор бесконечного ожидания
        elif "WRITE_SUCCESS" in message:
            self.progress.setRange(0, 1)
            self.progress.setValue(1)

    def handle_write_result(self, success, message):
        if success:
                self.status_label.setText("Успешная запись!")
                update(self.comboBox.currentText(), self.lineEdit_3.text())
                QTimer.singleShot(2000, self.write_dialog.close)
                self.lineEdit_3.clear()
                self.lineEdit.clear()

        else:
                self.status_label.setText(f"Ошибка: {message}")
                retry_button = QPushButton("Повторить")
                retry_button.clicked.connect(lambda: self.retry_write(self.serial_thread.text))
                close_button = QPushButton("Закрыть")
                close_button.clicked.connect(self.write_dialog.close)
                self.write_dialog.layout().addWidget(retry_button)
                self.write_dialog.layout().addWidget(close_button)

    def retry_write(self, text):
        # Очистка предыдущих кнопок
        for i in reversed(range(self.write_dialog.layout().count())):
                widget = self.write_dialog.layout().itemAt(i).widget()
                if isinstance(widget, QPushButton):
                        widget.deleteLater()
        self.status_label.setText("Идет запись на метку...")
        self.serial_thread = SerialWorker(text, self.find_metr())
        self.serial_thread.finished.connect(self.handle_write_result)
        self.serial_thread.start()
            
    def updateName(self, name):
        self.label_2.setText(name)
            
    def kocak(self):
        # Получаем информацию о детали из меток
        serial_number = self.serial.text()
        
        if serial_number == "Отсканируй деталь":
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Предупреждение")
            msg_box.setText("Сначала необходимо отсканировать деталь")
            msg_box.setStandardButtons(QMessageBox.Ok)
            self.style_message_box(msg_box)
            msg_box.exec()
            return
        
        # Показываем диалог подтверждения
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Подтверждение")
        formatted_text = f"Вы уверены, что хотите сообщить о браке\nдля детали с серийным номером\n\n{serial_number}?"
        msg_box.setText(formatted_text)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        self.style_message_box(msg_box)
        
        # Если пользователь подтвердил действие
        if msg_box.exec() == QMessageBox.Yes:
            print("Браковать:", serial_number)
            self.init_problem()

    def update2(self):
        # Получаем информацию о детали из меток
        serial_number = self.serial.text()
        
        if serial_number == "Отсканируй деталь":
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Предупреждение")
            msg_box.setText("Сначала необходимо отсканировать деталь")
            msg_box.setStandardButtons(QMessageBox.Ok)
            self.style_message_box(msg_box)
            msg_box.exec()
            return
        
        # Показываем диалог подтверждения
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Подтверждение")
        formatted_text = f"Вы выполнили все действия над деталью\nс серийным номером\n\n{serial_number}?"
        msg_box.setText(formatted_text)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        self.style_message_box(msg_box)
        
        # Если пользователь подтвердил действие
        if msg_box.exec() == QMessageBox.Yes:
            log_event("Работа над деталью закончена")
            update()
            
    # Добавляем функцию подтверждения для кнопки "Завершить работу"
    def confirm_end_session(self):
        # Создаем окно подтверждения
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Подтверждение")
        msg_box.setText("Вы хотите закончить работу?\nНесохраненные данные будут потеряны!")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        self.style_message_box(msg_box)
        
        # Возвращаем результат диалога
        return msg_box.exec() == QMessageBox.Yes

    # Функция для переподключения к МЭТР
    def reconnect_metr(self):
        """Функция переподключения к МЭТР"""
        try:
            # Пытаемся закрыть существующее соединение
            if hasattr(self, 'serial_manager') and self.serial_manager:
                self.serial_manager.close()
            
            # Находим МЭТР
            ports = serial.tools.list_ports.comports()
            metr_port = None
            for port in ports:
                if "USB Serial" in port.description or "Устройство с последовательным интерфейсом" in port.description:
                    metr_port = port.device
                    break
            
            if metr_port:
                try:
                    self.serial_manager = SerialManager(metr_port, 9600)
                    QMessageBox.information(None, "Подключение", f"МЭТР успешно подключен через порт {metr_port}")
                    return True
                except Exception as e:
                    QMessageBox.critical(None, "Ошибка", f"Ошибка при подключении к МЭТР: {e}")
            else:
                QMessageBox.warning(None, "Предупреждение", "МЭТР не найден. Проверьте подключение")
            
            return False
        except Exception as e:
            QMessageBox.critical(None, "Ошибка", f"Ошибка при переподключении к МЭТР: {e}")
            return False

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    def find_metr():
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "USB Serial Port" in port.description:
                return port.device
        return None

    port = find_metr()
    if not port:
        log_error("Не найден COM-порт")
        sys.exit(1)

    serial_manager = SerialManager(port, 9600)  # Создаём один экземпляр

    # Используем наш адаптивный класс вместо обычного QMainWindow
    window = AdaptiveMark(serial_manager)
    window.show()

    serial_listener = SerialListener(serial_manager)  # Используем общий менеджер
    serial_listener.start()

    try:
        sys.exit(app.exec())
    finally:
        serial_listener.stop()
        serial_manager.close()
