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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        self.main_window = MainWindow
        MainWindow.resize(1000, 800)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        
        # Header Section
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 1000, 50))
        self.widget.setStyleSheet(u"color: #5F7ADB;\n"
"font: 20px;\n"
"background-color: #2E3239;\n"
"font-weight: 700;")

        self.logo_label = QLabel(self.widget)
        self.logo_label.setObjectName(u"logo_label")
        self.logo_label.setGeometry(QRect(10, 5, 100, 40))
        self.logo_label.setPixmap(QPixmap(u"Frame 1 (1).png"))
        self.logo_label.setScaledContents(True)

        self.pushButton_7 = QPushButton(self.widget)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setGeometry(QRect(110, 0, 180, 50))
        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(470, 0, 180, 50))
        self.pushButton_2.setStyleSheet(u"")
        self.pushButton_5 = QPushButton(self.widget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(650, 0, 180, 50))
        self.pushButton_6 = QPushButton(self.widget)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(830, 0, 180, 50))
        self.pushButton_8 = QPushButton(self.widget)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setGeometry(QRect(290, 0, 180, 50))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"Маркировка", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Тестирование", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Упаковка", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Админ панель", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"Обработка", None))

        # Tree Widget Section
        self.treeWidget = QTreeWidget(self.centralwidget)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setGeometry(QRect(10, 60, 250, 730))
        self.treeWidget.setStyleSheet(u"QTreeWidget {\n"
"    background-color: #2E3239;\n"
"    color: white;\n"
"    font-size: 14px;\n"
"    border: 1px solid #5F7ADB;\n"
"    border-radius: 8px;\n"
"}\n"
"QTreeWidget::item {\n"
"    height: 30px;\n"
"    padding: 5px;\n"
"    border: none;\n"
"}\n"
"QTreeWidget::item:selected {\n"
"    background-color: #5F7ADB;\n"
"    color: white;\n"
"    border-radius: 4px;\n"
"}\n"
"QTreeWidget::branch:closed:has-children {\n"
"    border-image: none;\n"
"    image: url(':/icons/arrow-right.png');\n"
"}\n"
"QTreeWidget::branch:open:has-children {\n"
"    border-image: none;\n"
"    image: url(':/icons/arrow-down.png');\n"
"}")

        # Populate the Tree Widget
        self.treeWidget.setHeaderLabel(QCoreApplication.translate("MainWindow", "Предприятие"))


        top_item_1 = QTreeWidgetItem(self.treeWidget, ["Добавление пользователя"])
        top_item_2 = QTreeWidgetItem(self.treeWidget, ["Добавление датчика"])
        top_item_3 = QTreeWidgetItem(self.treeWidget, ["Датчики"])
        child_item_1 = QTreeWidgetItem(top_item_3, ["Датчики давления"])
        metran_150_item = QTreeWidgetItem(child_item_1, ["Метран 150"])
        metran_75_item = QTreeWidgetItem(child_item_1, ["Метран 75"])
        metran_55_item = QTreeWidgetItem(child_item_1, ["Метран 55"])
        child_item_2 = QTreeWidgetItem(top_item_3, ["Датчик температуры"])
        dashboard_item = QTreeWidgetItem(self.treeWidget, ["Дэшборд"])
        exit_item = QTreeWidgetItem(self.treeWidget, ["Выход"])

        

        # Main Content Area
        self.content_area = QWidget(self.centralwidget)
        self.content_area.setGeometry(QRect(270, 60, 720, 730))
        self.content_area.setObjectName(u"content_area")
        self.content_area.setStyleSheet(u"background-color: #EBF0FF; border-radius: 8px; padding: 10px; border: 2px solid #5F7ADB;")

        self.form_layout = QVBoxLayout(self.content_area)
        self.form_layout.setContentsMargins(10, 10, 10, 10)

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

        self.metran_150_table = QTableWidget(3, 2, self.content_area)
        self.metran_150_table.setHorizontalHeaderLabels(["Параметр", "Значение"])
        self.metran_150_table.setItem(0, 0, QTableWidgetItem("Масса"))
        self.metran_150_table.setItem(0, 1, QTableWidgetItem("5 кг"))
        self.metran_150_table.setItem(1, 0, QTableWidgetItem("Диаметр"))
        self.metran_150_table.setItem(1, 1, QTableWidgetItem("10 см"))
        self.metran_150_table.setItem(2, 0, QTableWidgetItem("Давление"))
        self.metran_150_table.setItem(2, 1, QTableWidgetItem("150 бар"))
        self.metran_150_table.hide()
        self.form_layout.addWidget(self.metran_150_table)


        self.metran_75_table = QTableWidget(3, 2, self.content_area)
        self.metran_75_table.setHorizontalHeaderLabels(["Параметр", "Значение"])
        self.metran_75_table.setItem(0, 0, QTableWidgetItem("Масса"))
        self.metran_75_table.setItem(0, 1, QTableWidgetItem("3 кг"))
        self.metran_75_table.setItem(1, 0, QTableWidgetItem("Диаметр"))
        self.metran_75_table.setItem(1, 1, QTableWidgetItem("8 см"))
        self.metran_75_table.setItem(2, 0, QTableWidgetItem("Давление"))
        self.metran_75_table.setItem(2, 1, QTableWidgetItem("75 бар"))
        self.metran_75_table.hide()
        self.form_layout.addWidget(self.metran_75_table)

        self.metran_55_table = QTableWidget(99999999, 6, self.content_area)
        self.metran_55_table.setHorizontalHeaderLabels(["Параметр", "Значение"])
        self.metran_55_table.setItem(0, 0, QTableWidgetItem("Идентификационный номер"))
        self.metran_55_table.setItem(0, 1, QTableWidgetItem("Наименование"))
        self.metran_55_table.setItem(0, 2, QTableWidgetItem("Серийный номер"))
        self.metran_55_table.setItem(0, 3, QTableWidgetItem("Дефектный"))
        self.metran_55_table.setItem(0, 4, QTableWidgetItem("Стадия производства"))
        self.metran_55_table.setItem(0, 5, QTableWidgetItem("Сектор хранения"))
        self.metran_55_table.hide()
        self.form_layout.addWidget(self.metran_55_table)

        self.treeWidget.itemClicked.connect(self.handle_item_clicked)

        MainWindow.setCentralWidget(self.centralwidget)
                # Таймер для проверки активности таблиц
        self.timer = QTimer()
        self.timer.setInterval(15000)  # 15 секунд
        self.timer.timeout.connect(self.check_active_table)
        self.timer.start()
        # Привязываем нажатие кнопки к методу обработки
        self.submit_button.clicked.connect(self.handle_submit)


        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
        
    
    def updateDetails(self, detail):
        data = {"type": "allDetails", "detail": detail}
        x = database(data)
        count = 1
        if x:
            for i in x['data']:
                self.metran_55_table.setItem(0, count, QTableWidgetItem(i["id"]))
                self.metran_55_table.setItem(1, count, QTableWidgetItem(i["name"]))
                self.metran_55_table.setItem(2, count, QTableWidgetItem(i["serial_number"]))
                self.metran_55_table.setItem(3, count, QTableWidgetItem(i["defective"]))
                self.metran_55_table.setItem(4, count, QTableWidgetItem(i["stage"]))
                self.metran_55_table.setItem(5, count, QTableWidgetItem(i["sector"]))
                count +=1

            
        else:
            return None
    
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
            print(user_data)
            if result:
                print("Пользователь добавлен:", result)
            else:
                print("Ошибка добавления пользователя. Проверьте данные.")
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
                print("Деталь добавлена:", result)
            else:
                print("Ошибка добавления детали. Проверьте данные.")
        else:
            print("Неверная операция или не выбрана форма.")
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
            print("Поля детали не заполнены.")
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
            print("Поля пользователя не заполнены.")
            return None


    def check_active_table(self):
        """Проверяет активность окна и отображаемой таблицы каждые 15 секунд."""
        if self.main_window.isActiveWindow():  # Используем экземпляр окна
            if self.metran_150_table.isVisible():
                self.updateDetails("МЕТРАН 150")
            elif self.metran_75_table.isVisible():
                self.updateDetails("МЕТРАН 75")
            elif self.metran_55_table.isVisible():
                self.updateDetails("МЕТРАН 55")
            else:
                print("Ни одна из таблиц Метран не активна")
        else:
            print("Окно не активно")

    def log_active_table(self, table_name):
        """Логирует или выполняет действие при входе в таблицу."""
        print(f"Вход в таблицу: {table_name}")
        # Здесь можно добавить логику, например обновление данных

    def handle_item_clicked(self, item):
        """Обрабатывает клики по элементам дерева."""
        self.metran_150_table.hide()
        self.metran_75_table.hide()
        self.metran_55_table.hide()
        self.dashboard_widget.hide()
        self.line_edit_1.hide()
        self.line_edit_2.hide()
        self.line_edit_3.hide()
        self.submit_button.hide()

        if item.text(0) == "Дэшборд":
            self.form_title.setText("Дэшборд")
            self.show_dashboard()
        elif item.text(0) == "Метран 150":
            self.form_title.setText("Метран 150")
            self.metran_150_table.show()
            self.updateDetails("МЕТРАН 150")  # Вызов функции при заходе
        elif item.text(0) == "Метран 75":
            self.form_title.setText("Метран 75")
            self.metran_75_table.show()
            self.updateDetails("МЕТРАН 75")  # Вызов функции при заходе
        elif item.text(0) == "Метран 55":
            self.form_title.setText("Метран 55")
            self.metran_55_table.show()
            self.updateDetails("МЕТРАН 55")  # Вызов функции при заходе
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
            self.form_title.setText("")

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
