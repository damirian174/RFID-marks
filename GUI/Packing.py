# -*- coding: utf-8 -*-

from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt, QTimer, QRect)
from PySide6.QtGui import QPixmap, QIcon, QFont
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QHBoxLayout, QLayout, QCheckBox, QTextEdit, QDialog)
from detail_work import end_work, pause_work, couintine_work, update, zakurit
import time
import os
import sys
# import button
import database
from datetime import datetime
from logger import log_event, log_error
from problema_window import show_problem_dialog  # Импорт функции для показа окна проблемы


class AdaptivePacking(QMainWindow):
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
        checkbox_size = max(15, int(base_font_size * 1.3)) # Чекбоксы
        
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
        
        checkbox_font = QFont()
        checkbox_font.setPointSize(checkbox_size)
        checkbox_font.setBold(True)
        
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
        
        # Чекбоксы для упаковки
        for checkbox in [self.ui.checkBox, self.ui.checkBox_2, self.ui.checkBox_3]:
            if hasattr(self.ui, checkbox.objectName()):
                checkbox.setFont(checkbox_font)
                checkbox.setStyleSheet(f"font-size: {checkbox_size}px; font-weight: 600;")
        
        # Инфо метки о детали
        for label in [self.ui.name, self.ui.serial, self.ui.defective, 
                     self.ui.stage, self.ui.sector]:
            if hasattr(self.ui, label.objectName()):
                label.setFont(normal_font)
                style = label.styleSheet()
                style = style.replace("font-size: 18px;", f"font-size: {normal_size}px;")
                label.setStyleSheet(style)
        
        # Кнопки действий
        for btn in [self.ui.pushButton, self.ui.pushButton_3, 
                    self.ui.pushButton_4, self.ui.pushButton_9, 
                    self.ui.pushButton_15]:
            if hasattr(self.ui, btn.objectName()):
                btn.setFont(button_font)
                style = btn.styleSheet()
                style = style.replace("font-size: 18px;", f"font-size: {button_size}px;")
                btn.setStyleSheet(style)
        
        # Логирование изменений
        log_event(f"Packing: размер окна изменен: {window_width}x{window_height}, шрифты: {header_size}/{title_size}/{normal_size}/{checkbox_size}px")


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
            background-color: #004B8D;
            color: #FFFFFF;
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
        QPushButton:hover {
                background-color: #4A6ED9;
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
        QPushButton:hover {
                background-color: #4A6ED9;
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
        QPushButton:hover {
                background-color: #4A6ED9;
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
        QPushButton:hover {
                background-color: #4A6ED9;
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
        QPushButton:hover {
                background-color: #4A6ED9;
        }
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
        self.verticalLayoutLeft.setContentsMargins(20, 20, 20, 20)
        self.verticalLayoutLeft.setSpacing(15)

        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setText(u"Василий Пупкин")
        self.label_2.setFixedHeight(40)
        self.label_2.setStyleSheet(u"""
            font: 30px;
            font-weight: 600;
            color: black;
        """)
        self.label_2.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Выравнивание по левому краю
        self.verticalLayoutLeft.addWidget(self.label_2)

        # Заголовок "Тесты"
        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")
        self.label.setFixedHeight(45)
        self.label.setStyleSheet(u"""
        color: rgb(255, 255, 255);
        background-color: #2E3239;
        font: 35px;
        font-weight: 700;
        border-radius: 15px;
        """)
        self.label.setText(u"Упаковка")
        self.label.setAlignment(Qt.AlignCenter)
        self.verticalLayoutLeft.addWidget(self.label)

        # Виджет для чекбоксов и кнопки
        self.widget_7 = QWidget(self.widget_2)
        self.widget_7.setObjectName(u"widget_7")
        self.widget_7.setStyleSheet(u"""
        background-color: #5F7ADB;
        color: rgb(255, 255, 255);
        border-radius: 50px;
        padding: 20px;
        """)
        self.verticalLayoutLeft.addWidget(self.widget_7)

        # Вертикальный макет для содержимого widget_7
        self.verticalLayoutWidget7 = QVBoxLayout(self.widget_7)
        self.verticalLayoutWidget7.setContentsMargins(20, 20, 20, 20)
        self.verticalLayoutWidget7.setSpacing(20)

        # Чекбоксы
        self.checkBox = QCheckBox(self.widget_7)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setStyleSheet(u"font: 20px; font-weight: 600;")
        self.checkBox.setText(u"1. Обернуто пупырчатой пленкой.")
        self.verticalLayoutWidget7.addWidget(self.checkBox)

        self.checkBox_2 = QCheckBox(self.widget_7)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setStyleSheet(u"font: 20px; font-weight: 600;")
        self.checkBox_2.setText(u"2. Документация в комплекте.")
        self.verticalLayoutWidget7.addWidget(self.checkBox_2)

        self.checkBox_3 = QCheckBox(self.widget_7)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setStyleSheet(u"font: 20px; font-weight: 600;")
        self.checkBox_3.setText(u"3. Упаковано в коробку.")
        self.verticalLayoutWidget7.addWidget(self.checkBox_3)

        # Добавляем обработчики событий для чекбоксов
        self.checkBox.stateChanged.connect(self.check_box_1_state_changed)
        self.checkBox_2.stateChanged.connect(self.check_box_2_state_changed)
        self.checkBox_3.stateChanged.connect(self.check_box_3_state_changed)
        
        # Инициализируем состояние чекбоксов (сбрасываем все галочки)
        self.reset_checkboxes()
        
        # Создаем таймер для периодической проверки состояния чекбоксов
        self.validation_timer = QTimer()
        self.validation_timer.timeout.connect(self.validate_checkboxes)
        self.validation_timer.start(500)  # Проверка каждые 500 мс

        # Кнопка "Закончить упаковку"
        self.pushButton = QPushButton(self.widget_7)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"""
        font: 25px;
        font-weight: 600;
        background-color: #2E3239;
        border-radius: 15px;
        color: white;
        """)
        self.pushButton.setText(u"Завершить упаковку")
        self.verticalLayoutWidget7.addWidget(self.pushButton)

        # Добавляем левую панель в основной макет
        self.horizontalLayoutMain.addWidget(self.widget_2, stretch=15)
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

        self.pushButton_4.clicked.connect(self.init_problem)
        self.pushButton_3.clicked.connect(self.kocak)  # Подключаем кнопку "Сообщить о браке" к функции kocak

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
        # Подключение слотов
        QMetaObject.connectSlotsByName(MainWindow)
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
        
        # Проверяем, все ли пункты упаковки выполнены
        all_items_checked = (self.checkBox.isChecked() and 
                            self.checkBox_2.isChecked() and 
                            self.checkBox_3.isChecked())
                            
        if not all_items_checked:
            # Проверяем, в правильной ли последовательности отмечены пункты
            if self.checkBox_2.isChecked() and not self.checkBox.isChecked():
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Ошибка порядка действий")
                msg_box.setText("Обнаружено нарушение последовательности действий!\nПункт 2 отмечен, но пункт 1 пропущен.")
                msg_box.setInformativeText("Выполните действия в правильном порядке.")
                msg_box.setStandardButtons(QMessageBox.Ok)
                self.style_message_box(msg_box)
                msg_box.exec()
                # Восстанавливаем правильное состояние
                self.reset_checkboxes()
                return
                
            if self.checkBox_3.isChecked() and (not self.checkBox.isChecked() or not self.checkBox_2.isChecked()):
                missing = "пункты 1 и 2" if not self.checkBox.isChecked() and not self.checkBox_2.isChecked() else "пункт 1" if not self.checkBox.isChecked() else "пункт 2"
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Ошибка порядка действий")
                msg_box.setText(f"Обнаружено нарушение последовательности действий!\nПункт 3 отмечен, но {missing} пропущен.")
                msg_box.setInformativeText("Выполните действия в правильном порядке.")
                msg_box.setStandardButtons(QMessageBox.Ok)
                self.style_message_box(msg_box)
                msg_box.exec()
                # Восстанавливаем правильное состояние
                self.reset_checkboxes()
                return
            
            # Если не все пункты отмечены, но порядок правильный, не даем завершить этап
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Предупреждение")
            formatted_text = f"Упаковка не завершена для детали\nс серийным номером\n\n{serial_number}"
            msg_box.setText(formatted_text)
            msg_box.setInformativeText("Пожалуйста, выполните все пункты упаковки перед завершением этапа.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            self.style_message_box(msg_box)
            msg_box.exec()
            return
            
        # Если все пункты выполнены, показываем диалог подтверждения
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
            # Сбрасываем чекбоксы
            self.reset_checkboxes()

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
        
            
        # Создаем окно подтверждения
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
            # Сбрасываем чекбоксы
            self.checkBox.setChecked(False)

    def detail(self, data=None):
        if data:
            self.name.setText(str(data['name']))
            self.serial.setText(str(data['serial_number']))
            self.defective.setText(str(data['defective']))
            self.stage.setText(str(data['stage']))
            self.sector.setText(str(data['sector']))
            self.change_color(2)
            log_event("Деталь принята в работу")
        else:
            log_event("Деталь не принята")
            self.name.setText("Отсканируй деталь")
            self.serial.setText("Отсканируй деталь")
            self.defective.setText("Отсканируй деталь")
            self.stage.setText("Отсканируй деталь")
            self.sector.setText("Отсканируй деталь")

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

    # Добавляем обработчики состояния чекбоксов
    def check_box_1_state_changed(self, state):
        # Первый чекбокс нельзя снять, если отмечены другие
        if state == Qt.Unchecked and (self.checkBox_2.isChecked() or self.checkBox_3.isChecked()):
            # Блокируем сигналы, чтобы избежать рекурсивных вызовов
            self.checkBox.blockSignals(True)
            self.checkBox.setChecked(True)
            self.checkBox.blockSignals(False)
            
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Предупреждение")
            msg_box.setText("Нельзя снимать галочки не по порядку!\nСначала снимите галочки с пунктов 3 и 2.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            self.style_message_box(msg_box)
            msg_box.exec()
        
    def check_box_2_state_changed(self, state):
        # Второй чекбокс можно отметить только если отмечен первый
        if state == Qt.Checked and not self.checkBox.isChecked():
            # Блокируем сигналы, чтобы избежать рекурсивных вызовов
            self.checkBox_2.blockSignals(True)
            self.checkBox_2.setChecked(False)
            self.checkBox_2.blockSignals(False)
            
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Предупреждение")
            msg_box.setText("Нельзя отмечать пункты не по порядку!\nСначала выполните пункт 1.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            self.style_message_box(msg_box)
            msg_box.exec()
        # Второй чекбокс нельзя снять, если отмечен третий
        elif state == Qt.Unchecked and self.checkBox_3.isChecked():
            # Блокируем сигналы, чтобы избежать рекурсивных вызовов
            self.checkBox_2.blockSignals(True)
            self.checkBox_2.setChecked(True)
            self.checkBox_2.blockSignals(False)
            
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Предупреждение")
            msg_box.setText("Нельзя снимать галочки не по порядку!\nСначала снимите галочку с пункта 3.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            self.style_message_box(msg_box)
            msg_box.exec()
            
    def check_box_3_state_changed(self, state):
        # Третий чекбокс можно отметить только если отмечены первый и второй
        if state == Qt.Checked and (not self.checkBox.isChecked() or not self.checkBox_2.isChecked()):
            # Блокируем сигналы, чтобы избежать рекурсивных вызовов
            self.checkBox_3.blockSignals(True)
            self.checkBox_3.setChecked(False)
            self.checkBox_3.blockSignals(False)
            
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Предупреждение")
            not_checked = "пункты 1 и 2" if not self.checkBox.isChecked() and not self.checkBox_2.isChecked() else "пункт 1" if not self.checkBox.isChecked() else "пункт 2"
            msg_box.setText(f"Нельзя отмечать пункты не по порядку!\nСначала выполните {not_checked}.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            self.style_message_box(msg_box)
            msg_box.exec()
        # Третий чекбокс можно снять в любом случае
        # так как это последний пункт в последовательности

    def reset_checkboxes(self):
        """Сбрасывает все чекбоксы в исходное состояние"""
        # Блокируем сигналы перед изменением состояния
        self.checkBox.blockSignals(True)
        self.checkBox_2.blockSignals(True)
        self.checkBox_3.blockSignals(True)
        
        # Сбрасываем все галочки
        self.checkBox.setChecked(False)
        self.checkBox_2.setChecked(False)
        self.checkBox_3.setChecked(False)
        
        # Восстанавливаем обработку сигналов
        self.checkBox.blockSignals(False)
        self.checkBox_2.blockSignals(False)
        self.checkBox_3.blockSignals(False)

    def validate_checkboxes(self):
        """Проверяет правильность порядка проставления галочек"""
        # Блокируем сигналы, чтобы избежать рекурсивных вызовов при исправлении
        self.checkBox.blockSignals(True)
        self.checkBox_2.blockSignals(True)
        self.checkBox_3.blockSignals(True)
        
        need_reset = False
        error_message = ""
        
        # Проверка на нарушение порядка
        if self.checkBox_2.isChecked() and not self.checkBox.isChecked():
            need_reset = True
            error_message = "Обнаружено нарушение последовательности действий!\nПункт 2 отмечен, но пункт 1 пропущен."
        elif self.checkBox_3.isChecked() and (not self.checkBox.isChecked() or not self.checkBox_2.isChecked()):
            need_reset = True
            missing = "пункты 1 и 2" if not self.checkBox.isChecked() and not self.checkBox_2.isChecked() else "пункт 1" if not self.checkBox.isChecked() else "пункт 2"
            error_message = f"Обнаружено нарушение последовательности действий!\nПункт 3 отмечен, но {missing} пропущен."
        
        # Восстанавливаем обработку сигналов
        self.checkBox.blockSignals(False)
        self.checkBox_2.blockSignals(False)
        self.checkBox_3.blockSignals(False)
        
        # Если обнаружено нарушение, сбрасываем чекбоксы и показываем сообщение
        if need_reset:
            self.reset_checkboxes()
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Ошибка порядка действий")
            msg_box.setText(error_message)
            msg_box.setInformativeText("Выполните действия в правильном порядке.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            self.style_message_box(msg_box)
            msg_box.exec()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
    # Используем наш адаптивный класс вместо обычного QMainWindow
    window = AdaptivePacking()
    window.show()
    
    sys.exit(app.exec())