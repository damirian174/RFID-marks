from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, QTimer)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QTableView, QTreeWidget,
    QTreeWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem)
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
            table.setRowCount(len(details))  # устанавливаем нужное число строк
            for row, detail_data in enumerate(details):
                table.setItem(row, 0, QTableWidgetItem(str(detail_data.get("id", ""))))
                table.setItem(row, 1, QTableWidgetItem(detail_data.get("name", "")))
                table.setItem(row, 2, QTableWidgetItem(detail_data.get("serial_number", "")))
                table.setItem(row, 3, QTableWidgetItem(str(detail_data.get("defective", ""))))
                table.setItem(row, 4, QTableWidgetItem(detail_data.get("stage", "")))
                table.setItem(row, 5, QTableWidgetItem(detail_data.get("sector", "")))
        else:
            log_error("Ошибка при получении данных из базы данных")

    
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
        
        # Показать нужный контент в зависимости от выбранного элемента
        if item.text(0) == "Дэшборд":
            self.form_title.setText("Дэшборд")
            self.show_dashboard()
            self.timer.start()  # Перезапускаем таймер, так как страница с таблицей не выбрана
        elif item.text(0) == "Метран 150":
            self.form_title.setText("Метран 150")
            self.metran_150_table.show()
            self.updateTable(self.metran_150_table, "МЕТРАН 150")
            self.timer.start()  # Перезапускаем таймер, так как таблица выбрана
        elif item.text(0) == "Метран 75":
            self.form_title.setText("Метран 75")
            self.metran_75_table.show()
            self.updateTable(self.metran_75_table, "МЕТРАН 75")
            self.timer.start()  # Перезапускаем таймер, так как таблица выбрана
        elif item.text(0) == "Метран 55":
            self.form_title.setText("Метран 55")
            self.metran_55_table.show()
            self.updateTable(self.metran_55_table, "МЕТРАН 55")
            self.timer.start()  # Перезапускаем таймер, так как таблица выбрана
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
        else:
            self.form_title.setText("")  # Если ничего не выбрано, скрываем заголовок

        self.timer.start() 

    def check_active_table(self):
        if self.main_window.isActiveWindow():  # Проверка активности окна
            if self.metran_150_table.isVisible():  # Проверка видимости таблицы
                self.updateTable(self.metran_150_table, "МЕТРАН 150")
            if self.metran_75_table.isVisible():
                self.updateTable(self.metran_75_table, "МЕТРАН 75")
            if self.metran_55_table.isVisible():
                self.updateTable(self.metran_55_table, "МЕТРАН 55")
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


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
