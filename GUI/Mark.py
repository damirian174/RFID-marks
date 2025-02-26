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
    QVBoxLayout, QWidget, QMessageBox, QDialog, QProgressBar, QHBoxLayout, QDialogButtonBox, QTextEdit)
from detail_work import end_work, pause_work, couintine_work, update
import serial
from PySide6.QtCore import QThread, Signal, QTimer
import time
import sys
import os
import serial
import serial.tools.list_ports
import button
import database
import datetime
class SerialWorker(QThread):
    finished = Signal(bool, str)
    status_update = Signal(str)
    
    def __init__(self, text, port):
        super().__init__()
        self.text = text.ljust(16)[:16]
        self.port = port #self.find_arduino()  # ★ Проверьте правильность порта!
        self.baudrate = 9600
        self.timeout = 5

    def run(self):
        try:
            # ★ Вывод информации о подключении
            self.status_update.emit(f"Подключаюсь к {self.port}...")
            with serial.Serial(
                self.port,
                self.baudrate,
                timeout=self.timeout,
                write_timeout=self.timeout
            ) as ser:
                time.sleep(2)
                
                # ★ Принудительная очистка буферов
                ser.reset_input_buffer()
                ser.reset_output_buffer()
                
                # ★ Отправка данных с подтверждением
                data_to_send = f"{self.text}\n"
                self.status_update.emit(f"Отправляю: '{data_to_send.strip()}'")
                ser.write(data_to_send.encode('utf-8'))
                ser.flush()  # ★ Важно: принудительная отправка
                
                # ★ Ожидание ответа
                start_time = time.time()
                while time.time() - start_time < self.timeout:
                    if ser.in_waiting:
                        line = ser.readline().decode('utf-8').strip()
                        self.status_update.emit(f"Получено: '{line}'")
                        if "WRITE_SUCCESS" in line:
                            self.finished.emit(True, "Успех!")
                            return
                        elif "WRITE_ERROR" in line:
                            self.finished.emit(False, "Ошибка Arduino")
                            return
                    time.sleep(0.1)
                
                self.finished.emit(False, "Таймаут ответа")

        except serial.SerialException as e:
            self.finished.emit(False, f"Ошибка порта: {str(e)}")
        except Exception as e:
            self.finished.emit(False, f"Неизвестная ошибка: {str(e)}")

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
        color: #5F7ADB;
        font: 20px;
        background-color: #2E3239;
        font-weight: 700;
        """)

        # Горизонтальный макет для шапки
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы
        self.horizontalLayout.setSpacing(0)  # Убираем промежутки между элементами

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
                color: #5F7ADB;\n"
"font: 20px;\n"
"background-color: #2E3239;\n"
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
                color: #5F7ADB;\n"
"font: 20px;\n"
"background-color: #2E3239;\n"
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
                color: #5F7ADB;\n"
"font: 20px;\n"
"background-color: #2E3239;\n"
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
                color: #5F7ADB;\n"
"font: 20px;\n"
"background-color: #2E3239;\n"
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
                color: #5F7ADB;\n"
"font: 20px;\n"
"background-color: #2E3239;\n"
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
        print("name widget initialized")
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
        self.pushButton_9.clicked.connect(button.MainApp.setup_scan_page)
        self.pushButton_4.clicked.connect(self.init_problem)
        # Подключение слотов
        QMetaObject.connectSlotsByName(MainWindow)
    # def init_problem(self):
        
    #     report_text = self.label.text()
    #     data = {"type": "report", "text": report_text, "time": datetime.datetime(), "name": self.label_2.text()}
    #     x = database(data)
    #     if x: 
    #         # Успешно отправлено, ждите специалиста
    #         return
    #     else: 
    #         # Не успешно
    #         return
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

        
        data = {
            "type": "report",  
            "text": report_text,  
            "time": datetime.datetime.now(),  
            "name": self.label_2.text()  
        }
        print()
        
        if database.database(data):  
            QMessageBox.information(self.dialog, "Успех", "Отчет успешно отправлен. Ожидайте специалиста.")
            self.dialog.close()  
        else:
            QMessageBox.critical(self.dialog, "Ошибка", "Не удалось отправить отчет. Пожалуйста, попробуйте снова.")



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
    def find_arduino(self):
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

        self.confirmation_window.show()
    

    def confirm_data(self):
        # Получаем данные из полей ввода
        category = self.lineEdit.text()
        marking = self.comboBox.currentText()
        serial_number = self.lineEdit_3.text()
        
        # Формируем текст для записи (пример формата)
        text_to_write = f"{serial_number}"
        
        # Вызываем функцию записи
        self.write(text_to_write)
        
        # Очищаем поля и закрываем окно
        self.lineEdit.clear()
        self.lineEdit_3.clear()
        self.confirmation_window.close()

    def edit_data(self):
        self.confirmation_window.close()

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
        if not hasattr(self, 'name'):
            print("name widget not initialized!")
            return  # or some other handling mechanism
        
        # Proceed with the normal logic
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
        
        self.serial_thread = SerialWorker(text, self.find_arduino())
        self.serial_thread.finished.connect(self.handle_write_result)
        self.serial_thread.status_update.connect(self.update_status)  # Новый обработчик
        self.serial_thread.start()
        
        self.write_dialog.exec_()

    def update_status(self, message):
        self.status_label.setText(message)
        if "WRITE_SUCCESS" in message:
            self.progress.setRange(0, 1)
            self.progress.setValue(1)
    def handle_write_result(self, success, message):
        if success:
                self.status_label.setText("Успешная запись!")
                print(self.comboBox.currentText(), self.lineEdit_3.text())
                update(self.comboBox.currentText(), self.lineEdit_3.text())
                QTimer.singleShot(2000, self.write_dialog.close)
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
        self.serial_thread = SerialWorker(text, self.find_arduino())
        self.serial_thread.finished.connect(self.handle_write_result)
        self.serial_thread.start()
            
    def updateName(self, name):
        self.label_2.setText(name)
            
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())