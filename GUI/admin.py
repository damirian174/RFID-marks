from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, QTimer)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QTableView, QTreeWidget,
    QTreeWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem, QDialog, QMessageBox)
from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from database import *
from PySide6.QtCore import QThread, Signal, Slot
import time
import os, sys
from logger import log_event, log_error

class DatabaseWorker(QThread):
    # Сигнал для передачи данных в основной поток
    finished = Signal(dict)

    def __init__(self, query):
        super().__init__()
        self.query = query
        log_event(f"Создан поток DatabaseWorker с запросом: {query}")
        self.run()  # Запрос к базе данных

    def run(self):
        try:
            result = database(self.query)
            log_event(f"Выполнен запрос к БД: {self.query}")
            self.finished.emit(result)
        except Exception as e:
            log_error(f"Ошибка при запросе к базе данных: {e}")


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        self.main_window = MainWindow
        MainWindow.resize(1300, 750)
        MainWindow.setStyleSheet(u"background-color:rgb(255, 255, 255)")
        log_event("Создан интерфейс админ-панели")

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
        self.horizontalLayoutMain.setSpacing(20)
        self.horizontalLayoutMain.setContentsMargins(0, 20, 20, 20)
        # Tree Widget левый блок
        

        # Tree Widget (левый блок)
        self.treeWidget = QTreeWidget(self.centralwidget)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setStyleSheet(u"""
            QTreeWidget {
                background-color: #2E3239;
                color: white;
                font-size: 14px;
                border: 1px solid #5F7ADB;
                border-radius: 8px;
            }
            QTreeWidget::item {
                height: 30px;
                padding: 5px;
                border: none;
            }
            QTreeWidget::item:selected {
                background-color: #5F7ADB;
                color: white;
                border-radius: 4px;
            }
            QTreeWidget::branch:closed:has-children {
                border-image: none;
                image: url(':/icons/arrow-right.png');
            }
            QTreeWidget::branch:open:has-children {
                border-image: none;
                image: url(':/icons/arrow-down.png');
            }
        """)
        self.treeWidget.setHeaderLabel(QCoreApplication.translate("MainWindow", "Предприятие"))

        # Заполнение Tree Widget
        top_item_1 = QTreeWidgetItem(self.treeWidget, ["Добавление пользователя"])
        top_item_2 = QTreeWidgetItem(self.treeWidget, ["Добавление датчика"])
        top_item_3 = QTreeWidgetItem(self.treeWidget, ["Брак"])
        top_item_4 = QTreeWidgetItem(self.treeWidget, ["Датчики"])
        child_item_1 = QTreeWidgetItem(top_item_4, ["Датчики давления"])
        QTreeWidgetItem(child_item_1, ["Метран 150"])
        QTreeWidgetItem(child_item_1, ["Метран 75"])
        QTreeWidgetItem(child_item_1, ["Метран 55"])
        QTreeWidgetItem(top_item_4, ["Датчик температуры"])
        QTreeWidgetItem(self.treeWidget, ["Дэшборд"])
        QTreeWidgetItem(self.treeWidget, ["Отчеты"])
        QTreeWidgetItem(self.treeWidget, ["Активные сессии"])
        QTreeWidgetItem(self.treeWidget, ["Выход"])

        self.horizontalLayoutMain.addWidget(self.treeWidget, stretch=1)  # Растягиваем на 1 часть

        # Правый блок (контент)
        self.content_area = QWidget(self.centralwidget)
        self.content_area.setObjectName(u"content_area")
        self.content_area.setStyleSheet(u"""
            background-color: #EBF0FF;
            border-radius: 8px;
            padding: 10px;
            border: 2px solid #5F7ADB;
        """)
        
        self.form_layout = QVBoxLayout(self.content_area)
        self.form_layout.setContentsMargins(20, 20, 20, 20)

        self.form_title = QLabel("", self.content_area)
        self.form_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.form_layout.addWidget(self.form_title)

        self.dashboard_widget = QWidget(self.content_area)
        self.dashboard_widget.setObjectName("dashboard_widget")
        self.dashboard_widget_layout = QVBoxLayout(self.dashboard_widget)
        self.dashboard_widget.setStyleSheet("background-color: white; border: 1px solid #C0C0C0; border-radius: 5px; padding: 5px;")
        self.dashboard_widget.hide()
        self.form_layout.addWidget(self.dashboard_widget)


        self.line_edit_1 = QLineEdit(self.content_area)
        self.line_edit_1.setPlaceholderText("Поле 1")
        self.line_edit_1.setStyleSheet("background-color: white; border: 1px solid #C0C0C0; border-radius: 5px; padding: 5px;")
        self.form_layout.addWidget(self.line_edit_1)
        self.line_edit_1.hide()

        self.line_edit_2 = QLineEdit(self.content_area)
        self.line_edit_2.setPlaceholderText("Поле 2")
        self.line_edit_2.setStyleSheet("background-color: white; border: 1px solid #C0C0C0; border-radius: 5px; padding: 5px;")
        self.form_layout.addWidget(self.line_edit_2)
        self.line_edit_2.hide()

        self.line_edit_3 = QLineEdit(self.content_area)
        self.line_edit_3.setPlaceholderText("Поле 3")
        self.line_edit_3.setStyleSheet("background-color: white; border: 1px solid #C0C0C0; border-radius: 5px; padding: 5px;")
        self.form_layout.addWidget(self.line_edit_3)
        self.line_edit_3.hide()

        self.submit_button = QPushButton("Сохранить", self.content_area)
        self.submit_button.setStyleSheet("background-color: #5F7ADB; color: white; border-radius: 5px; font-size: 14px;")
        self.form_layout.addWidget(self.submit_button)
        self.submit_button.hide()
        

        self.metran_150_table = QTableWidget(0, 6, self.content_area)
        self.metran_150_table.hide()
        self.form_layout.addWidget(self.metran_150_table)


        self.metran_75_table = QTableWidget(0, 6, self.content_area)
        self.form_layout.addWidget(self.metran_75_table)

        self.metran_55_table = QTableWidget(0, 6, self.content_area)
        self.metran_55_table.hide()
        self.form_layout.addWidget(self.metran_55_table)

        # Добавляем таблицу для бракованных деталей
        self.defective_table = QTableWidget(0, 5, self.content_area)
        self.defective_table.hide()
        self.defective_table.setHorizontalHeaderLabels(["ID", "Название", "Серийный номер", "Статус", "Этап"])
        self.defective_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.defective_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: #333;
                gridline-color: #d3d3d3;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
            QHeaderView::section {
                background-color: #5F7ADB;
                color: white;
                padding: 5px;
                font-weight: bold;
                border: none;
            }
        """)
        self.form_layout.addWidget(self.defective_table)

        # Добавляем таблицу для репортов
        self.reports_table = QTableWidget(0, 5, self.content_area)  # Увеличиваем количество колонок на 1 для кнопки
        self.reports_table.hide()
        self.reports_table.setHorizontalHeaderLabels(["ID", "Имя", "Текст", "Время", ""])
        self.reports_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.reports_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)  # Фиксированный размер для кнопки
        self.reports_table.setColumnWidth(4, 100)  # Ширина колонки с кнопкой
        
        # Устанавливаем таблицу только для чтения
        self.reports_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.reports_table.setFocusPolicy(Qt.NoFocus)
        self.reports_table.setSelectionMode(QTableWidget.NoSelection)
        
        self.form_layout.addWidget(self.reports_table)

        # Добавляем таблицу для активных сессий
        self.sessions_table = QTableWidget(0, 3, self.content_area)
        self.sessions_table.hide()
        self.sessions_table.setHorizontalHeaderLabels(["Сотрудник", "Время старта", "Описание работы"])
        self.sessions_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Устанавливаем таблицу только для чтения
        self.sessions_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.sessions_table.setFocusPolicy(Qt.NoFocus)
        self.sessions_table.setSelectionMode(QTableWidget.NoSelection)
        
        # Создаем кнопку для удаления всех сессий
        self.delete_all_sessions_button = QPushButton("Удалить все сессии")
        self.delete_all_sessions_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                min-width: 200px;
                margin: 10px 0;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)
        self.delete_all_sessions_button.clicked.connect(self.delete_all_sessions)
        self.delete_all_sessions_button.hide()  # Скрываем кнопку по умолчанию
        
        # Создаем контейнер для таблицы и кнопки
        self.sessions_container = QWidget(self.content_area)
        self.sessions_container.hide()
        self.sessions_layout = QVBoxLayout(self.sessions_container)
        self.sessions_layout.addWidget(self.sessions_table)
        self.sessions_layout.addWidget(self.delete_all_sessions_button, 0, Qt.AlignRight)
        
        self.form_layout.addWidget(self.sessions_container)

        self.form_layout.setContentsMargins(0, 0, 0, 0)
        
        self.treeWidget.itemClicked.connect(self.handle_item_clicked)
        # Добавляем правый блок в основной макет
        self.horizontalLayoutMain.addWidget(self.content_area, stretch=3)  # Растягиваем на 3 части
        self.verticalLayout.addLayout(self.horizontalLayoutMain)

        # Подключение сигналов
        self.treeWidget.itemClicked.connect(self.handle_item_clicked)

                # Таймер для проверки активности таблиц

        self.timer = QTimer()
        self.timer.setInterval(15000)  # 15 секунд
        self.timer.timeout.connect(self.check_active_table)
        self.timer.start()
        # Привязываем нажатие кнопки к методу обработки
        self.submit_button.clicked.connect(self.handle_submit)
        self.treeWidget.itemClicked.connect(self.handle_item_clicked)
        self.retranslateUi(MainWindow)
        #
        QMetaObject.connectSlotsByName(MainWindow)
        
    
    def updateTable(self, table, detail):
        table.setRowCount(0)
        query = {"type": "allDetails", "detail": detail}
        if not hasattr(self, 'workers'):
            self.workers = []
        worker = DatabaseWorker(query)
        worker.finished.connect(lambda result, t=table: self.on_database_finished_generic(result, t))
        worker.finished.connect(lambda: self.workers.remove(worker))
        worker.finished.connect(worker.deleteLater)
        self.workers.append(worker)
        worker.start()

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

    @Slot(dict)
    def on_database_finished_generic(self, result, table):
        if result and result.get('status') == 'ok':
            details = result['data']
            if details:  # Проверяем, есть ли данные
                table.setRowCount(len(details))  # устанавливаем нужное число строк
                for row, detail_data in enumerate(details):
                    table.setItem(row, 0, QTableWidgetItem(str(detail_data.get("id", ""))))
                    table.setItem(row, 1, QTableWidgetItem(detail_data.get("name", "")))
                    table.setItem(row, 2, QTableWidgetItem(detail_data.get("serial_number", "")))
                    if detail_data.get("defective", ""):
                        x = "Брак"
                    else:
                        x = "Годен"
                    table.setItem(row, 3, QTableWidgetItem(x))
                    table.setItem(row, 4, QTableWidgetItem(detail_data.get("stage", "")))
                    if detail_data.get("sector", ""):
                        y = detail_data.get("sector", "")
                    else:
                        y = "Не храним"
                    table.setItem(row, 5, QTableWidgetItem(y))
            else:
                table.setRowCount(1)  # Создаем одну строку для сообщения
                empty_item = QTableWidgetItem("Список пуст")
                empty_item.setTextAlignment(Qt.AlignCenter)
                table.setItem(0, 0, empty_item)
                table.setSpan(0, 0, 1, 6)  # Объединяем все ячейки в строке
        else:
            log_error("Ошибка при получении данных из базы данных")
            table.setRowCount(1)  # Создаем одну строку для сообщения
            error_item = QTableWidgetItem("Список пуст")
            error_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(0, 0, error_item)
            table.setSpan(0, 0, 1, 6)  # Объединяем все ячейки в строке

    def handle_submit(self):
    # Проверяем, какой элемент был выбран
        if self.form_title.text() == "Добавление пользователя":
            # Получаем данные из полей и вызываем функцию addUser
            user_data = {
                "name": self.line_edit_2.text(),
                "surname": self.line_edit_1.text(),
                "prof": self.line_edit_3.text()
            }
            result = self.addUser(user_data)
            if result:
                log_event(f"Добавление пользователя: {user_data}")
            else:
                log_error(f"Ошибка добавления пользователя: {user_data}")
        elif self.form_title.text() == "Добавление детали":
            # Получаем данные из полей и вызываем функцию addDetail
            detail_data = { 
                "name ": self.line_edit_1.text(), 
                "pressure_pa ": self.line_edit_2.text(), 
                "temperature":self.line_edit_3.text(),
                "form_factor": self.line_edit_4.text() 
            }
            result = self.addDetail(detail_data)
            if result:
                log_event(f"Добавление датчика: {user_data}")
            else:
                log_error("Ошибка добавления детали. Проверьте данные.")
        else:
            log_error("Неверная операция или не выбрана форма.")
    def addDetail(self, data):
        if data["sensor"] and data["model"] and data["index"]:
            query = {
                "type": "addDetail",
                "name": data["name"],
                "pressure_pa": data["pressure_pa"],
                "temperature": data["temperature"],
                "form_factor": data["form_factor"]
            }
            return database(query)
        else:
            log_error("Поля детали не заполнены.")
            return None

        
    def addUser(self, data):
        if data["name"] and data["surname"] and data["prof"]:
            query = {
                "type": "addUser",
                "name": data["name"],
                "surname": data["surname"],
                "prof": data["prof"]
            }
            return database(query)
        else:
            log_error("Поля пользователя не заполнены.")
            return None





    def log_active_table(self, table_name):
        """Логирует или выполняет действие при входе в таблицу."""
        log_event(f"Вход в таблицу: {table_name}")
        # Здесь можно добавить логику, например обновление данных
    def handle_item_clicked(self, item):
        self.timer.stop()  # Останавливаем таймер при клике по элементу

        # Скрываем все виджеты (таблицы, формы)
        self.metran_150_table.hide()
        self.metran_75_table.hide()
        self.metran_55_table.hide()
        self.dashboard_widget.hide()
        self.line_edit_1.hide()
        self.line_edit_2.hide()
        self.line_edit_3.hide()
        self.submit_button.hide()
        self.reports_table.hide()
        self.sessions_container.hide()  # Скрываем таблицу сессий
        self.defective_table.hide()  # Скрываем таблицу бракованных деталей
        
        # Показать нужный контент в зависимости от выбранного элемента
        if item.text(0) == "Дэшборд":
            self.form_title.setText("Дэшборд")
            self.show_dashboard()
        elif item.text(0) == "Метран 150":
            self.form_title.setText("Метран 150")
            self.metran_150_table.show()
            self.updateTable(self.metran_150_table, "МЕТРАН 150")
        elif item.text(0) == "Метран 75":
            self.form_title.setText("Метран 75")
            self.metran_75_table.show()
            self.updateTable(self.metran_75_table, "МЕТРАН 75")
        elif item.text(0) == "Метран 55":
            self.form_title.setText("Метран 55")
            self.metran_55_table.show()
            self.updateTable(self.metran_55_table, "МЕТРАН 55")
        elif item.text(0) == "Брак":
            self.form_title.setText("Бракованные детали")
            self.defective_table.show()
            self.updateDefectiveTable()
        elif item.text(0) == "Добавление пользователя":
            self.form_title.setText("Добавление пользователя")
            self.line_edit_1.setPlaceholderText("Фамилия")
            self.line_edit_2.setPlaceholderText("Имя")
            self.line_edit_3.setPlaceholderText("Должность")
            self.line_edit_1.show()
            self.line_edit_2.show()
            self.line_edit_3.show()
            self.submit_button.show()
        elif item.text(0) == "Добавление датчика":
            self.form_title.setText("Добавление детали")
            self.line_edit_1.setPlaceholderText("Датчик")
            self.line_edit_2.setPlaceholderText("Название модели")
            self.line_edit_3.setPlaceholderText("Индекс")
            self.line_edit_1.show()
            self.line_edit_2.show()
            self.line_edit_3.show()
            self.submit_button.show()
        elif item.text(0) == "Выход":
            QApplication.instance().quit()
        elif item.text(0) == "Отчеты":
            self.form_title.setText("Отчеты о проблемах")
            log_event("Выбран пункт меню Отчеты")
            # Очищаем таблицу перед запросом данных
            self.reports_table.setRowCount(0)
            self.reports_table.clearContents()
            self.reports_table.show()
            self.updateReportsTable()
            log_event(f"Статус видимости таблицы отчетов после show(): {self.reports_table.isVisible()}")
        elif item.text(0) == "Активные сессии":
            self.form_title.setText("Активные сессии")
            
            # Принудительно показываем и таблицу, и контейнер
            self.sessions_table.clearContents()
            self.sessions_container.show()
            self.sessions_table.show()
            
            # Обновляем стили таблицы
            self.sessions_table.setStyleSheet("""
                QTableWidget {
                    background-color: white;
                    color: #333;
                    gridline-color: #d3d3d3;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QTableWidget::item {
                    padding: 5px;
                    border-bottom: 1px solid #eee;
                }
                QHeaderView::section {
                    background-color: #5F7ADB;
                    color: white;
                    padding: 5px;
                    font-weight: bold;
                    border: none;
                }
            """)
            
            # Обновляем данные таблицы
            self.sessions_table.setRowCount(0)
            self.updateSessionsTable()
            
            # Логируем для проверки
            log_event("Отображаем страницу активных сессий")
            log_event(f"Видимость таблицы: {self.sessions_table.isVisible()}, контейнера: {self.sessions_container.isVisible()}")
        else:
            self.form_title.setText("")  # Если ничего не выбрано, скрываем заголовок

        self.timer.start()  # Перезапускаем таймер

    def check_active_table(self):
        if self.main_window.isActiveWindow():  # Проверка активности окна
            if self.metran_150_table.isVisible():  # Проверка видимости таблицы
                self.updateTable(self.metran_150_table, "МЕТРАН 150")
            if self.metran_75_table.isVisible():
                self.updateTable(self.metran_75_table, "МЕТРАН 75")
            if self.metran_55_table.isVisible():
                self.updateTable(self.metran_55_table, "МЕТРАН 55")
            if self.reports_table.isVisible():
                self.updateReportsTable()
            if self.sessions_container.isVisible():
                self.updateSessionsTable()
            if self.defective_table.isVisible():
                self.updateDefectiveTable()
    def show_dashboard(self):
        from Dash import Dashboard
        dashboard = Dashboard()

        # Удаляем старые виджеты из layout
        for i in reversed(range(self.dashboard_widget_layout.count())):
            self.dashboard_widget_layout.itemAt(i).widget().setParent(None)

        # Добавляем графики из Dashboard
        charts = [
            dashboard.create_performance_chart(),
            dashboard.create_sensor_type_chart()
        ]
        for chart in charts:
            self.dashboard_widget_layout.addWidget(chart)

        self.dashboard_widget.show()

    def updateReportsTable(self):
        query = {"type": "getreports"}
        if not hasattr(self, 'workers'):
            self.workers = []
        worker = DatabaseWorker(query)
        worker.finished.connect(lambda result: self.on_reports_finished(result))
        worker.finished.connect(lambda: self.workers.remove(worker))
        worker.finished.connect(worker.deleteLater)
        self.workers.append(worker)
        worker.start()

    @Slot(dict)
    def on_reports_finished(self, result):
        log_event(f"Получен ответ для таблицы отчетов: {result}")
        if result and result.get('status') == 'ok':
            reports = result['data']
            log_event(f"Число полученных отчетов: {len(reports) if reports else 0}")
            if reports:  # Проверяем, есть ли данные
                # Сортируем отчеты по дате (новые сверху)
                reports.sort(key=lambda x: x.get("time", ""), reverse=True)
                
                self.reports_table.setRowCount(len(reports))
                log_event(f"Установлено количество строк в таблице: {len(reports)}")
                for row, report in enumerate(reports):
                    log_event(f"Обработка отчета {row+1}/{len(reports)}: {report}")
                    self.reports_table.setItem(row, 0, QTableWidgetItem(str(report.get("id", ""))))
                    self.reports_table.setItem(row, 1, QTableWidgetItem(report.get("name", "")))
                    self.reports_table.setItem(row, 2, QTableWidgetItem(report.get("text", "")))
                    self.reports_table.setItem(row, 3, QTableWidgetItem(report.get("time", "")))
                    
                    # Добавляем кнопку удаления
                    delete_button = QPushButton("Удалить")
                    delete_button.setStyleSheet("""
                        QPushButton {
                            background-color: #dc3545;
                            color: white;
                            border: none;
                            padding: 5px 10px;
                            border-radius: 3px;
                            font-size: 12px;
                        }
                        QPushButton:hover {
                            background-color: #c82333;
                        }
                    """)
                    delete_button.clicked.connect(lambda checked, r=row: self.delete_report(r))
                    self.reports_table.setCellWidget(row, 4, delete_button)
                log_event(f"Таблица отчетов заполнена {len(reports)} записями")
                log_event(f"Статус видимости таблицы: {self.reports_table.isVisible()}")
                
                # Обновляем таблицу и ее отображение
                self.reports_table.resizeColumnsToContents()
                self.reports_table.resizeRowsToContents()
                self.reports_table.viewport().update()
                self.content_area.update()
                
                # Проверяем, что таблица отображается
                if not self.reports_table.isVisible():
                    log_event("Таблица отчетов была скрыта, показываем её снова")
                    self.reports_table.show()
            else:
                self.reports_table.setRowCount(1)  # Создаем одну строку для сообщения
                empty_item = QTableWidgetItem("Список пуст")
                empty_item.setTextAlignment(Qt.AlignCenter)
                self.reports_table.setItem(0, 0, empty_item)
                self.reports_table.setSpan(0, 0, 1, 5)  # Объединяем все ячейки в строке
                log_event("Таблица отчетов: список пуст")
                self.reports_table.viewport().update()
        else:
            log_error("Ошибка при получении отчетов из базы данных")
            self.reports_table.setRowCount(1)  # Создаем одну строку для сообщения
            error_item = QTableWidgetItem("Список пуст")
            error_item.setTextAlignment(Qt.AlignCenter)
            self.reports_table.setItem(0, 0, error_item)
            self.reports_table.setSpan(0, 0, 1, 5)  # Объединяем все ячейки в строке
            self.reports_table.viewport().update()

    def delete_report(self, row):
        try:
            report_id = self.reports_table.item(row, 0).text()
            report_name = self.reports_table.item(row, 1).text()
            report_text = self.reports_table.item(row, 2).text()
            
            # Создаем диалог подтверждения
            confirm_dialog = QDialog(self.main_window)
            confirm_dialog.setWindowTitle("Подтверждение удаления")
            confirm_dialog.setFixedSize(400, 200)
            confirm_dialog.setStyleSheet("""
                QDialog {
                    background-color: #f8f9fa;
                    border-radius: 10px;
                    border: 2px solid #dc3545;
                }
                QLabel {
                    color: #212529;
                    font-size: 14px;
                    margin: 10px;
                }
                QPushButton {
                    padding: 8px 20px;
                    border-radius: 5px;
                    font-size: 14px;
                    min-width: 100px;
                }
                QPushButton#confirmButton {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                }
                QPushButton#confirmButton:hover {
                    background-color: #c82333;
                }
                QPushButton#cancelButton {
                    background-color: #6c757d;
                    color: white;
                    border: none;
                }
                QPushButton#cancelButton:hover {
                    background-color: #5a6268;
                }
            """)
            
            layout = QVBoxLayout(confirm_dialog)
            layout.setContentsMargins(20, 20, 20, 20)
            layout.setSpacing(15)
            
            # Добавляем предупреждающую иконку
            warning_label = QLabel("⚠️")
            warning_label.setStyleSheet("font-size: 24px;")
            warning_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(warning_label)
            
            # Добавляем текст подтверждения
            confirm_text = QLabel(f"Вы действительно хотите удалить отчет от пользователя {report_name}?")
            confirm_text.setAlignment(Qt.AlignCenter)
            confirm_text.setWordWrap(True)
            layout.addWidget(confirm_text)
            
            # Добавляем текст отчета
            report_text_label = QLabel(f"Текст отчета: {report_text}")
            report_text_label.setAlignment(Qt.AlignCenter)
            report_text_label.setWordWrap(True)
            layout.addWidget(report_text_label)
            
            # Создаем кнопки
            button_layout = QHBoxLayout()
            button_layout.setSpacing(10)
            
            confirm_button = QPushButton("Удалить")
            confirm_button.setObjectName("confirmButton")
            cancel_button = QPushButton("Отмена")
            cancel_button.setObjectName("cancelButton")
            
            button_layout.addWidget(confirm_button)
            button_layout.addWidget(cancel_button)
            layout.addLayout(button_layout)
            
            # Подключаем сигналы
            confirm_button.clicked.connect(confirm_dialog.accept)
            cancel_button.clicked.connect(confirm_dialog.reject)
            
            # Показываем диалог и проверяем результат
            if confirm_dialog.exec() == QDialog.Accepted:
                query = {
                    "type": "deleteReport",
                    "id": report_id
                }
                result = database(query)
                if result and result.get('status') == 'ok':
                    log_event(f"Удален отчет с ID: {report_id}")
                    self.updateReportsTable()  # Обновляем таблицу после удаления
                else:
                    log_error(f"Ошибка при удалении отчета с ID: {report_id}")
            else:
                log_event("Удаление отчета отменено пользователем")
                
        except Exception as e:
            log_error(f"Ошибка при удалении отчета: {e}")

    def updateSessionsTable(self):
        query = {"type": "getSessions"}
        if not hasattr(self, 'workers'):
            self.workers = []
        worker = DatabaseWorker(query)
        worker.finished.connect(lambda result: self.on_sessions_finished(result))
        worker.finished.connect(lambda: self.workers.remove(worker))
        worker.finished.connect(worker.deleteLater)
        self.workers.append(worker)
        worker.start()

    @Slot(dict)
    def on_sessions_finished(self, result):
        log_event(f"Получен ответ для таблицы сессий: {result}")
        if result and result.get('status') == 'ok':
            sessions = result['data']
            log_event(f"Число полученных сессий: {len(sessions) if sessions else 0}")
            
            if sessions:  # Проверяем, есть ли данные
                # Очищаем таблицу
                self.sessions_table.clearContents()
                self.sessions_table.setRowCount(len(sessions))
                
                # Принудительно устанавливаем видимость таблицы
                self.sessions_table.show()
                
                # Устанавливаем стили таблицы
                self.sessions_table.setStyleSheet("""
                    QTableWidget {
                        background-color: white;
                        color: #333;
                        gridline-color: #d3d3d3;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        font-size: 14px;
                    }
                    QTableWidget::item {
                        padding: 5px;
                        border-bottom: 1px solid #eee;
                    }
                    QHeaderView::section {
                        background-color: #5F7ADB;
                        color: white;
                        padding: 5px;
                        font-weight: bold;
                        border: none;
                    }
                """)
                
                for row, session in enumerate(sessions):
                    # Объединяем имя и фамилию
                    full_name = f"{session.get('surname', '')} {session.get('name', '')}"
                    self.sessions_table.setItem(row, 0, QTableWidgetItem(full_name))
                    self.sessions_table.setItem(row, 1, QTableWidgetItem(session.get('start_time', '')))
                    self.sessions_table.setItem(row, 2, QTableWidgetItem(session.get('work_description', '')))
                
                # Показываем кнопку удаления всех сессий, если есть больше одной сессии
                if len(sessions) > 1:
                    self.delete_all_sessions_button.show()
                    log_event("Показана кнопка удаления всех сессий")
                else:
                    self.delete_all_sessions_button.hide()
                    log_event("Кнопка удаления всех сессий скрыта (только одна сессия)")
                
                # Обновляем таблицу и ее отображение
                self.sessions_table.resizeColumnsToContents()
                self.sessions_table.resizeRowsToContents()
                self.sessions_table.viewport().update()
                
                # Проверяем видимость таблицы и контейнера
                log_event(f"Видимость таблицы: {self.sessions_table.isVisible()}, контейнера: {self.sessions_container.isVisible()}")
            else:
                self.sessions_table.setRowCount(1)  # Создаем одну строку для сообщения
                empty_item = QTableWidgetItem("Список пуст")
                empty_item.setTextAlignment(Qt.AlignCenter)
                self.sessions_table.setItem(0, 0, empty_item)
                self.sessions_table.setSpan(0, 0, 1, 3)  # Объединяем все ячейки в строке
                self.delete_all_sessions_button.hide()
                log_event("Таблица сессий: список пуст")
        else:
            log_error("Ошибка при получении сессий из базы данных")
            self.sessions_table.setRowCount(1)  # Создаем одну строку для сообщения
            error_item = QTableWidgetItem("Список пуст")
            error_item.setTextAlignment(Qt.AlignCenter)
            self.sessions_table.setItem(0, 0, error_item)
            self.sessions_table.setSpan(0, 0, 1, 3)  # Объединяем все ячейки в строке
            self.delete_all_sessions_button.hide()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))

    def delete_all_sessions(self):
        """Удаляет все сессии, кроме текущей активной сессии пользователя"""
        try:
            # Создаем диалог подтверждения удаления
            confirm_dialog = QDialog(self.main_window)
            confirm_dialog.setWindowTitle("Подтверждение удаления")
            confirm_dialog.setFixedSize(450, 200)
            
            # Установка иконки
            icon_path = self.get_image_path("favicon.ico")
            confirm_dialog.setWindowIcon(QIcon(icon_path))
            
            confirm_dialog.setStyleSheet("""
                QDialog {
                    background-color: #f8f9fa;
                    border-radius: 10px;
                    border: 2px solid #dc3545;
                }
                QLabel {
                    color: #212529;
                    font-size: 14px;
                    margin: 10px;
                }
                QPushButton {
                    padding: 8px 20px;
                    border-radius: 5px;
                    font-size: 14px;
                    min-width: 100px;
                }
                QPushButton#confirmButton {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                }
                QPushButton#confirmButton:hover {
                    background-color: #c82333;
                }
                QPushButton#cancelButton {
                    background-color: #6c757d;
                    color: white;
                    border: none;
                }
                QPushButton#cancelButton:hover {
                    background-color: #5a6268;
                }
            """)
            
            layout = QVBoxLayout(confirm_dialog)
            layout.setContentsMargins(20, 20, 20, 20)
            layout.setSpacing(15)
            
            # Добавляем предупреждающую иконку
            warning_label = QLabel("⚠️")
            warning_label.setStyleSheet("font-size: 24px;")
            warning_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(warning_label)
            
            # Добавляем текст подтверждения
            confirm_text = QLabel("Вы действительно хотите удалить все неактивные сессии?\nТекущая активная сессия не будет удалена.")
            confirm_text.setAlignment(Qt.AlignCenter)
            confirm_text.setWordWrap(True)
            layout.addWidget(confirm_text)
            
            # Создаем кнопки
            button_layout = QHBoxLayout()
            button_layout.setSpacing(10)
            
            confirm_button = QPushButton("Удалить")
            confirm_button.setObjectName("confirmButton")
            cancel_button = QPushButton("Отмена")
            cancel_button.setObjectName("cancelButton")
            
            button_layout.addWidget(confirm_button)
            button_layout.addWidget(cancel_button)
            layout.addLayout(button_layout)
            
            # Подключаем сигналы
            confirm_button.clicked.connect(confirm_dialog.accept)
            cancel_button.clicked.connect(confirm_dialog.reject)
            
            # Показываем диалог и проверяем результат
            if confirm_dialog.exec() == QDialog.Accepted:
                # Отправляем запрос на удаление всех сессий, кроме текущей
                query = {
                    "type": "deleteAllSessions",
                    "keepCurrentSession": True
                }
                log_event("Отправляем запрос на удаление всех сессий, кроме текущей")
                result = database(query)
                
                if result and result.get('status') == 'ok':
                    log_event(f"Успешно удалены неактивные сессии. Удалено: {result.get('count', 0)} сессий")
                    # Показываем сообщение об успешном удалении
                    self.show_success_message(f"Успешно удалено {result.get('count', 0)} сессий")
                    # Обновляем таблицу сессий
                    self.updateSessionsTable()
                else:
                    log_error(f"Ошибка при удалении сессий: {result}")
                    self.show_error_message("Не удалось удалить сессии. Попробуйте позже.")
            else:
                log_event("Удаление сессий отменено пользователем")
        except Exception as e:
            log_error(f"Ошибка при удалении сессий: {e}")
            self.show_error_message(f"Произошла ошибка: {str(e)}")
    
    def show_success_message(self, message):
        """Показывает сообщение об успешном выполнении операции"""
        msg_box = QMessageBox(self.main_window)
        msg_box.setWindowTitle("Успешно")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        
        # Установка иконки
        icon_path = self.get_image_path("favicon.ico")
        msg_box.setWindowIcon(QIcon(icon_path))
        
        msg_box.exec()
    
    def show_error_message(self, message):
        """Показывает сообщение об ошибке"""
        msg_box = QMessageBox(self.main_window)
        msg_box.setWindowTitle("Ошибка")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setStandardButtons(QMessageBox.Ok)
        
        # Установка иконки
        icon_path = self.get_image_path("favicon.ico")
        msg_box.setWindowIcon(QIcon(icon_path))
        
        msg_box.exec()

    def updateDefectiveTable(self):
        """Обновляет таблицу с бракованными деталями"""
        query = {"type": "alldefective"}
        if not hasattr(self, 'workers'):
            self.workers = []
        worker = DatabaseWorker(query)
        worker.finished.connect(lambda result: self.on_defective_finished(result))
        worker.finished.connect(lambda: self.workers.remove(worker))
        worker.finished.connect(worker.deleteLater)
        self.workers.append(worker)
        worker.start()
        log_event("Отправлен запрос на получение бракованных деталей")

    @Slot(dict)
    def on_defective_finished(self, result):
        """Обрабатывает результат запроса на получение бракованных деталей"""
        log_event(f"Получен ответ для таблицы бракованных деталей: {result}")
        if result and result.get('status') == 'ok':
            defective_items = result['data']
            log_event(f"Число полученных бракованных деталей: {len(defective_items) if defective_items else 0}")
            
            if defective_items:  # Проверяем, есть ли данные
                # Очищаем таблицу
                self.defective_table.clearContents()
                self.defective_table.setRowCount(len(defective_items))
                
                # Заполняем таблицу данными
                for row, item in enumerate(defective_items):
                    self.defective_table.setItem(row, 0, QTableWidgetItem(str(item.get("id", ""))))
                    self.defective_table.setItem(row, 1, QTableWidgetItem(item.get("name", "")))
                    self.defective_table.setItem(row, 2, QTableWidgetItem(item.get("serial_number", "")))
                    
                    # В статусе всегда указываем "Брак"
                    status_item = QTableWidgetItem("Брак")
                    status_item.setForeground(QColor(255, 0, 0))  # Красный цвет для статуса "Брак"
                    self.defective_table.setItem(row, 3, status_item)
                    
                    self.defective_table.setItem(row, 4, QTableWidgetItem(item.get("stage", "")))
                
                # Обновляем таблицу
                self.defective_table.resizeColumnsToContents()
                self.defective_table.resizeRowsToContents()
                self.defective_table.viewport().update()
                log_event("Таблица бракованных деталей обновлена")
            else:
                self.defective_table.setRowCount(1)
                empty_item = QTableWidgetItem("Бракованных деталей не найдено")
                empty_item.setTextAlignment(Qt.AlignCenter)
                self.defective_table.setItem(0, 0, empty_item)
                self.defective_table.setSpan(0, 0, 1, 5)  # Объединяем все ячейки в строке
                log_event("Таблица бракованных деталей: список пуст")
        else:
            log_error("Ошибка при получении бракованных деталей из базы данных")
            self.defective_table.setRowCount(1)
            error_item = QTableWidgetItem("Ошибка при получении данных")
            error_item.setTextAlignment(Qt.AlignCenter)
            self.defective_table.setItem(0, 0, error_item)
            self.defective_table.setSpan(0, 0, 1, 5)  # Объединяем все ячейки в строке

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
