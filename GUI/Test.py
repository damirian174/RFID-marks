# -*- coding: utf-8 -*-

from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt, QRect)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QHBoxLayout, QSizePolicy, QCheckBox, QDialog, QTextEdit)
import os
import sys
from detail_work import end_work, pause_work, couintine_work, update, zakurit
# import button
import database
from datetime import datetime

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
        # Логотип (фиксированный размер)
        self.widget_7 = QWidget(self.widget)
        self.widget_7.setObjectName(u"widget_7")
        self.widget_7.setFixedSize(110, 50)  # Фиксированный размер логотипа
        self.label_9 = QLabel(self.widget_7)
        self.label_9.setObjectName(u"label_9")
        image_path = self.get_image_path("main.jpg")
        self.label_9.setPixmap(QPixmap(image_path))
        self.horizontalLayout.addWidget(self.widget_7)

        # Кнопки шапки (адаптируются по ширине)
        self.pushButton_7 = QPushButton(self.widget)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setText(u"Маркировка")
        self.pushButton_7.setFixedHeight(50)
        self.pushButton_7.setStyleSheet(u"""
        QPushButton {
                color: #5F7ADB;
                font: 20px;
                background-color: #2E3239;
                font-weight: 700;
        }
        """)
        self.horizontalLayout.addWidget(self.pushButton_7)

        self.pushButton_8 = QPushButton(self.widget)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setText(u"Сборка")
        self.pushButton_8.setFixedHeight(50)
        self.pushButton_8.setStyleSheet(u"""
        QPushButton {
                color: #5F7ADB;
                font: 20px;
                background-color: #2E3239;
                font-weight: 700;
        }
        """)
        self.horizontalLayout.addWidget(self.pushButton_8)

        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setText(u"Тестирование")
        self.pushButton_2.setFixedHeight(50)
        self.pushButton_2.setStyleSheet(u"""
        QPushButton {
                color: #5F7ADB;
                font: 20px;
                background-color: #2E3239;
                font-weight: 700;
        }
        """)
        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton_5 = QPushButton(self.widget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setText(u"Упаковка")
        self.pushButton_5.setFixedHeight(50)
        self.pushButton_5.setStyleSheet(u"""
        QPushButton {
                color: #5F7ADB;
                font: 20px;
                background-color: #2E3239;
                font-weight: 700;
        }
        """)
        self.horizontalLayout.addWidget(self.pushButton_5)

        self.pushButton_6 = QPushButton(self.widget)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setText(u"Админ панель")
        self.pushButton_6.setFixedHeight(50)
        self.pushButton_6.setStyleSheet(u"""
        QPushButton {
                color: #5F7ADB;
                font: 20px;
                background-color: #2E3239;
                font-weight: 700;
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
        self.label.setText(u"Тесты")
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
        self.checkBox.setText(u"Выдерживает температуру")
        self.verticalLayoutWidget7.addWidget(self.checkBox)

        self.checkBox_2 = QCheckBox(self.widget_7)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setStyleSheet(u"font: 20px; font-weight: 600;")
        self.checkBox_2.setText(u"Показывает по стандартам")
        self.verticalLayoutWidget7.addWidget(self.checkBox_2)

        self.checkBox_3 = QCheckBox(self.widget_7)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setStyleSheet(u"font: 20px; font-weight: 600;")
        self.checkBox_3.setText(u"Работает без ошибок")
        self.verticalLayoutWidget7.addWidget(self.checkBox_3)

        # Кнопка "Закончить тестирование"
        self.pushButton = QPushButton(self.widget_7)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"""
        font: 25px;
        font-weight: 600;
        background-color: #2E3239;
        border-radius: 15px;
        color: white;
        """)
        self.pushButton.setText(u"Завершить тестирование")
        self.verticalLayoutWidget7.addWidget(self.pushButton)

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
        self.pushButton.clicked.connect(self.update2)
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

        self.pushButton_4.clicked.connect(self.init_problem)

        # Подключение слотов
        QMetaObject.connectSlotsByName(MainWindow)
    def update2(self):
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

    def away(self):
        self.centralwidget.setEnabled(False)
        pause_work()
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Отошел")
        msg_box.setText("Нажми, чтобы продолжить работать")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.buttonClicked.connect(self.countine)
        msg_box.exec()

    def countine(self):
        self.centralwidget.setEnabled(True)
        couintine_work()

    def detail(self, data=None):
        if data:
            self.name.setText(str(data['name']))
            self.serial.setText(str(data['serial_number']))
            self.defective.setText(str(data['defective']))
            self.stage.setText(str(data['stage']))
            self.sector.setText(str(data['sector']))
        else:
            self.name.setText("Отсканируй деталь")
            self.serial.setText("Отсканируй деталь")
            self.defective.setText("Отсканируй деталь")
            self.stage.setText("Отсканируй деталь")
            self.sector.setText("Отсканируй деталь")
            
    def updateName(self, name):
        self.label_2.setText(name)
    def init_problem(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle("Сообщить о проблеме")  
        self.dialog.setFixedSize(300, 200)  
        global dialog
        self.layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        global text_edit
        self.text_edit.setPlaceholderText("Опишите вашу проблему здесь...")  
        self.layout.addWidget(self.text_edit)  

        self.send_button = QPushButton("Отправить")
        global send_button
        self.layout.addWidget(self.send_button)  
        self.send_button.clicked.connect(self.send_report)

        self.dialog.setLayout(self.layout)

        self.dialog.show()

    # Функция, которая вызывается при нажатии на кнопку "Отправить"
    def send_report(self):
        report_text = self.text_edit.toPlainText()
        
        
        if not report_text.strip():
            QMessageBox.warning(self.dialog, "Ошибка", "Пожалуйста, опишите вашу проблему перед отправкой.")
            return
           # Исправлено: вызываем now() для получения текущего времени
        vrema = datetime.datetime.now()  # Теперь vrema — это объект datetime
        time = vrema.strftime("%Y-%m-%d %H:%M")  # Форматируем вре
        data = {
            "type": "report",  
            "text": report_text,  
            "time": time,  
            "name": self.label_2.text()  
        }
        print(type(vrema))
        
        if database.database(data):  
            QMessageBox.information(self.dialog, "Успех", "Отчет успешно отправлен. Ожидайте специалиста.")
            self.dialog.close()  
        else:
            QMessageBox.critical(self.dialog, "Ошибка", "Не удалось отправить отчет. Пожалуйста, попробуйте снова.")

        def kocak(self):
            zakurit()



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())