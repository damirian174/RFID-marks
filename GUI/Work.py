# -*- coding: utf-8 -*-

from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt, QTimer, QRect)
from PySide6.QtGui import QPixmap, QIcon, QFont
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QHBoxLayout, QLayout, QDialog, QTextEdit)
from detail_work import end_work, pause_work, couintine_work, update, zakurit, getDetail
import time
import os, sys
from datetime import datetime
# import button
import database
from problema_window import show_problem_dialog  # Импорт функции для показа окна проблемы
from logger import log_event
import serial.tools.list_ports
from COM import SerialManager, SerialListener


class AdaptiveWork(QMainWindow):
    """
    Расширенное главное окно с поддержкой адаптивных элементов
    и шрифтов, которые изменяются в зависимости от размера окна.
    """
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
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
        timer_size = max(20, int(base_font_size * 2.0))   # Размер таймера
        
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
        
        timer_font = QFont()
        timer_font.setPointSize(timer_size)
        timer_font.setBold(True)
        
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
        
        # Заголовки секций и имя пользователя
        self.ui.label_2.setFont(title_font)
        self.ui.label_2.setStyleSheet(f"font-size: {title_size}px; font-weight: 600; color: black;")
        
        self.ui.label.setFont(title_font)
        self.ui.label.setStyleSheet(f"""
        color: rgb(255, 255, 255);
        background-color: #2E3239;
        font-size: {title_size}px;
        font-weight: 700;
        border-radius: 15px;
        """)
        
        # Таймер и заголовок
        self.ui.label_3.setFont(title_font)
        self.ui.label_3.setStyleSheet(f"font-size: {title_size}px; font-weight: 600;")
        
        # Время таймера
        self.ui.label.setFont(timer_font)
        self.ui.label.setStyleSheet(f"font-size: {timer_size}px; font-weight: 800; text-align: center;")
        
        # Инфо метки о детали
        for label in [self.ui.name, self.ui.serial, self.ui.defective, 
                     self.ui.stage, self.ui.sector]:
            label.setFont(normal_font)
            style = label.styleSheet()
            style = style.replace("font-size: 18px;", f"font-size: {normal_size}px;")
            label.setStyleSheet(style)
        
        # Кнопки действий
        for btn in [self.ui.pushButton, self.ui.pushButton_3, 
                    self.ui.pushButton_4, self.ui.pushButton_9, 
                    self.ui.pushButton_15]:
            btn.setFont(button_font)
            style = btn.styleSheet()
            style = style.replace("font-size: 18px;", f"font-size: {button_size}px;")
            btn.setStyleSheet(style)
        
        # Логирование изменений
        log_event(f"Work: размер окна изменен: {window_width}x{window_height}, шрифты: {header_size}/{title_size}/{normal_size}px")


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
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
        # Верхняя панель (Header)
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setFixedHeight(50)  # Фиксированная высота шапки
        self.widget.setStyleSheet(u"""
            background-color: #2E3239;
            color: #5F7ADB;
            font-size: 20px;
            font-weight: 700;
        """)
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)

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
        QPushButton:hover {{
                background-color: #4A6ED9;
        }}
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
        QPushButton:hover {{
                background-color: #4A6ED9;
        }}
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
        QPushButton:hover {{
                background-color: #4A6ED9;
        }}
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
        QPushButton:hover {{
                background-color: #4A6ED9;
        }}
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
        QPushButton:hover {{
                background-color: #4A6ED9;
        }}
        """)
        self.horizontalLayout.addWidget(self.pushButton_6)
        # Добавляем шапку в основной макет
        self.verticalLayout.addWidget(self.widget)

        # Основной контент (горизонтальный макет)
        self.horizontalLayoutMain = QHBoxLayout()
        self.horizontalLayoutMain.setSpacing(0)

        # Левая панель (Синий блок и кнопки)
        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setStyleSheet(u"background-color: rgb(235, 240, 255);")
        self.verticalLayoutLeft = QVBoxLayout(self.widget_2)
        self.verticalLayoutLeft.setContentsMargins(20, 20, 20, 100)
        self.verticalLayoutLeft.setSpacing(30)

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
        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")
        self.label.setFixedHeight(40)
        self.label.setStyleSheet(u"""
        color: rgb(255, 255, 255);
        background-color: #2E3239;
        font: 35px;
        font-weight: 700;
        border-radius: 15px;
        """)
        self.label.setText(u"Сборка")
        self.label.setAlignment(Qt.AlignCenter)
        self.verticalLayoutLeft.addWidget(self.label)

        # Синий блок (таймер и кнопка "Завершить этап")
        self.widget_5 = QWidget(self.widget_2)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setStyleSheet(u"""
            background-color: #5F7ADB;
            color: rgb(255, 255, 255);
            border-radius: 50px;
            padding: 20px;
        """)
        self.verticalLayoutBlue = QVBoxLayout(self.widget_5)
        self.verticalLayoutBlue.setSpacing(15)

        self.label_3 = QLabel(self.widget_5)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"font: 30px; font-weight: 600;")
        self.label_3.setText(u"Время обработки:")
        self.verticalLayoutBlue.addWidget(self.label_3, alignment=Qt.AlignCenter)

        self.label = QLabel(self.widget_5)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font: 40px; font-weight: 800; text-align: center;")
        self.label.setText(u"00:00")
        self.verticalLayoutBlue.addWidget(self.label, alignment=Qt.AlignCenter)

        self.pushButton = QPushButton(self.widget_5)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"""
            font: 25px;
            font-weight: 600;
            background-color: #2E3239;
            border-radius: 15px;
        """)
        self.pushButton.setText(u"Завершить этап")
        self.verticalLayoutBlue.addWidget(self.pushButton, alignment=Qt.AlignCenter)
        self.horizontalLayoutMain.addWidget(self.widget_2, stretch=15)
        self.verticalLayoutLeft.addWidget(self.widget_5, stretch=15)  # Синий блок занимает больше места

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
        self.pushButton_4.clicked.connect(self.init_problem)

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

        # Добавляем новую кнопку для сброса детали
        self.reset_button = QPushButton(self.widget_3) # widget_3 - центральная панель
        self.reset_button.setObjectName(u"reset_button")
        self.reset_button.setStyleSheet(u"""
            QPushButton {
                background-color: #DC3545;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 15px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #BD2130;
            }
        """)
        self.reset_button.setText(u"Сбросить деталь")
        self.reset_button.clicked.connect(self.reset_detail)
        self.verticalLayoutCenter.addWidget(self.reset_button)

        self.horizontalLayoutMain.addWidget(self.widget_3, stretch=10)

        

          # Левая панель занимает больше места

        # Правая панель (Информация о детали)
        self.widget_3 = QWidget(self.centralwidget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setStyleSheet(u"background-color: rgb(235, 240, 255);")
        self.verticalLayoutRight = QVBoxLayout(self.widget_3)
        self.verticalLayoutRight.setContentsMargins(20, 20, 20, 20)
        self.verticalLayoutRight.setSpacing(15)

        self.name = QLabel(self.widget_3)
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

        self.serial = QLabel(self.widget_3)
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




        self.defective = QLabel(self.widget_3)
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

        self.stage = QLabel(self.widget_3)
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

        self.sector = QLabel(self.widget_3)
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

        self.horizontalLayoutMain.addWidget(self.widget_3, stretch=10)  # Правая панель занимает меньше места

        self.verticalLayout.addLayout(self.horizontalLayoutMain)
        self.pushButton.clicked.connect(self.update2)

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
        
        QMetaObject.connectSlotsByName(MainWindow)

        # Таймер
        self.start_time = time.time()
        self.timer = QTimer(MainWindow)
        self.timer.timeout.connect(self.update_time)
        self.running = True

    def update_time(self):
        if self.running:
            elapsed = time.time() - self.start_time
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            time_string = f"{hours:02}:{minutes:02}:{seconds:02}"
            self.label.setText(time_string)
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
        formatted_text = f"Вы хотите отправить деталь\nс серийным номером\n\n{serial_number}\n\nв брак?"
        msg_box.setText(formatted_text)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        self.style_message_box(msg_box)
        
        # Если пользователь подтвердил действие
        if msg_box.exec() == QMessageBox.Yes:
            zakurit()
            log_event(f"Деталь {serial_number} отправлена в брак")


    def start_timer(self):
        self.start_time = time.time()
        self.timer.start(100)
        self.running = True

    def stop_timer(self):
        self.timer.stop()
        self.running = False

    def pause_timer(self):
        if self.running:
            self.timer.stop()
            self.running = False
            self.elapsed_pause_time = time.time() - self.start_time

    def resume_timer(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_pause_time
            self.timer.start(100)
            self.running = True
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
        # Через 7 секунд вернуть стандартный цвет
        from PySide6.QtCore import QTimer
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


    def detail(self, data=None):
        # Заполняем поля данными
        self.name.setText("")
        self.serial.setText("")
        self.defective.setText("")
        self.stage.setText("")
        self.sector.setText("")
        
        # Очищаем все поля перед обновлением
        name, serial, defective, stage, sector = getDetail(data) if data else ("", "", "", "", "")
        self.name.setText(name)
        self.serial.setText(serial)
        self.defective.setText(defective)
        self.stage.setText(stage)
        self.sector.setText(sector)
        self.change_color(2)

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

    def updateName(self, name):
        self.label_2.setText(name)
    def init_problem(self):
        # Вместо создания собственного диалога вызываем функцию из problema_window
        show_problem_dialog(self.centralwidget)

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

    # Добавляем новый метод reset_detail 
    def reset_detail(self):
        """
        Сбрасывает информацию о детали в интерфейсе без изменения её состояния на сервере
        """
        # Показываем диалог подтверждения
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Подтверждение сброса")
        msg_box.setText("Вы уверены, что хотите сбросить информацию о детали?\nЭто действие не изменит статус детали на сервере.")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        self.style_message_box(msg_box)
        
        # Устанавливаем иконку
        icon_path = self.get_image_path("favicon.ico")
        msg_box.setWindowIcon(QIcon(icon_path))
        
        # Если пользователь подтвердил действие
        if msg_box.exec() == QMessageBox.Yes:
            # Сбрасываем отображение информации о детали
            self.detail(False)
            
            # Останавливаем таймер, если он запущен
            if hasattr(self, 'timer') and self.running:
                self.stop_timer()
            
            # Сбрасываем глобальные переменные в detail_work
            from detail_work import data_detail
            import detail_work
            
            # Сбрасываем переменные, но не вызываем end_work(), 
            # так как это изменило бы статус на сервере
            detail_work.data_detail = None
            detail_work.detail_work = False
            
            # Сброс переменных в config
            import config
            config.detail = None
            config.work = False
            
            log_event("Информация о детали сброшена пользователем без изменения статуса на сервере")

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
    
    # Используем наш адаптивный класс вместо обычного QMainWindow
    window = AdaptiveWork()
    window.show()
    
    sys.exit(app.exec())