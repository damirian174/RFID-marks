from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, QTimer)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QTableView, QTreeWidget,
    QTreeWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem, QDialog, QMessageBox, QFrame, QTabWidget, QGroupBox, QFormLayout, QDialogButtonBox, QScrollArea)
from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from database import *
from PySide6.QtCore import QThread, Signal, Slot
import time
import os, sys
from logger import log_event, log_error, log_warning

def get_status_text(status):
    """Преобразует код статуса в текстовое представление."""
    if status == 1 or status == "1":
        return "Годен"
    elif status == 0 or status == "0":
        return "Брак"
    elif status is None:
        return "Нет данных"
    else:
        return str(status)

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
        QTreeWidgetItem(self.treeWidget, ["Сотрудники"])
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
        

        # Metran 150 таблица
        self.metran_150_table = QTableWidget(0, 7, self.content_area)  # Увеличиваю до 7 колонок для кнопки
        self.metran_150_table.setHorizontalHeaderLabels(["ID", "Название", "Серийный номер", "Статус", "Этап", "Место", "Действия"])
        self.metran_150_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.metran_150_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.Fixed)  # Фиксированная ширина для кнопки
        self.metran_150_table.setColumnWidth(6, 120)  # Ширина колонки с кнопкой
        # Устанавливаем таблицу только для чтения
        self.metran_150_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.metran_150_table.setFocusPolicy(Qt.ClickFocus)  # Оставляем возможность кликать для кнопок
        self.metran_150_table.setSelectionBehavior(QTableWidget.SelectRows)  # Выделение только строк
        self.metran_150_table.hide()
        self.form_layout.addWidget(self.metran_150_table)


        self.metran_75_table = QTableWidget(0, 7, self.content_area)  # Увеличиваю до 7 колонок для кнопки
        self.metran_75_table.setHorizontalHeaderLabels(["ID", "Название", "Серийный номер", "Статус", "Этап", "Место", "Действия"])
        self.metran_75_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.metran_75_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.Fixed)  # Фиксированная ширина для кнопки
        self.metran_75_table.setColumnWidth(6, 120)  # Ширина колонки с кнопкой
        # Устанавливаем таблицу только для чтения
        self.metran_75_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.metran_75_table.setFocusPolicy(Qt.ClickFocus)  # Оставляем возможность кликать для кнопок
        self.metran_75_table.setSelectionBehavior(QTableWidget.SelectRows)  # Выделение только строк
        self.form_layout.addWidget(self.metran_75_table)

        self.metran_55_table = QTableWidget(0, 7, self.content_area)  # Увеличиваю до 7 колонок для кнопки
        self.metran_55_table.setHorizontalHeaderLabels(["ID", "Название", "Серийный номер", "Статус", "Этап", "Место", "Действия"])
        self.metran_55_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.metran_55_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.Fixed)  # Фиксированная ширина для кнопки
        self.metran_55_table.setColumnWidth(6, 120)  # Ширина колонки с кнопкой
        # Устанавливаем таблицу только для чтения
        self.metran_55_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.metran_55_table.setFocusPolicy(Qt.ClickFocus)  # Оставляем возможность кликать для кнопок
        self.metran_55_table.setSelectionBehavior(QTableWidget.SelectRows)  # Выделение только строк
        self.metran_55_table.hide()
        self.form_layout.addWidget(self.metran_55_table)

        # Добавляем таблицу для бракованных деталей
        self.defective_table = QTableWidget(0, 5, self.content_area)
        self.defective_table.hide()
        self.defective_table.setHorizontalHeaderLabels(["ID", "Название", "Серийный номер", "Статус", "Этап"])
        self.defective_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Устанавливаем таблицу только для чтения
        self.defective_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.defective_table.setFocusPolicy(Qt.ClickFocus)
        self.defective_table.setSelectionBehavior(QTableWidget.SelectRows)  # Выделение только строк
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
        
        # Создаем контейнер для поля поиска и таблицы сотрудников
        self.users_container = QWidget(self.content_area)
        self.users_container.hide()
        self.users_layout = QVBoxLayout(self.users_container)
        self.users_layout.setContentsMargins(0, 0, 0, 0)
        self.users_layout.setSpacing(0)
        
        # Создаем верхний виджет, где будет заголовок и поиск
        self.users_header_widget = QWidget()
        self.users_header_widget.setStyleSheet("""
            background-color: #E3EEFF;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            border: 1px solid #BDD7FB;
        """)
        self.header_layout = QHBoxLayout(self.users_header_widget)
        self.header_layout.setContentsMargins(15, 15, 15, 15)
        
        # Заголовок слева
        self.users_title_label = QLabel("Список сотрудников")
        self.users_title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #1A4CA3;
            padding: 5px 10px;
            background-color: #C9E0FF;
            border-radius: 8px;
        """)
        
        # Поле для ввода поискового запроса (справа)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #BDD7FB;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
                max-width: 150px;
            }
            QLineEdit:focus {
                border: 2px solid #5F7ADB;
                background-color: #F7FAFF;
            }
        """)
        self.search_input.setMaximumWidth(150)
        self.search_input.textChanged.connect(self.filter_users_table)
        
        # Кнопка очистки поиска
        self.clear_search_button = QPushButton("✕")
        self.clear_search_button.setStyleSheet("""
            QPushButton {
                background-color: #6E8CD9;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 4px;
                font-size: 12px;
                min-width: 25px;
                max-width: 25px;
                min-height: 25px;
                max-height: 25px;
            }
            QPushButton:hover {
                background-color: #5A78C5;
            }
            QPushButton:pressed {
                background-color: #4A68B5;
            }
        """)
        self.clear_search_button.setFixedSize(25, 25)
        self.clear_search_button.clicked.connect(self.clear_search)
        
        # Создаем виджет для поиска (обертка для поля ввода и кнопки)
        self.search_widget = QWidget()
        self.search_layout = QHBoxLayout(self.search_widget)
        self.search_layout.setContentsMargins(0, 0, 0, 0)
        self.search_layout.setSpacing(5)
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(self.clear_search_button)
        self.search_widget.setMaximumWidth(190)
        
        # Добавляем заголовок (слева) и поиск (справа) в верхний layout
        self.header_layout.addWidget(self.users_title_label, 1, Qt.AlignLeft)
        self.header_layout.addStretch(1)
        self.header_layout.addWidget(self.search_widget, 0, Qt.AlignRight)
        
        # Добавляем верхний виджет в контейнер
        self.users_layout.addWidget(self.users_header_widget)
        
        # Настраиваем таблицу
        self.users_table = QTableWidget()
        self.users_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.users_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.users_table.setSelectionMode(QTableWidget.SingleSelection)
        self.users_table.verticalHeader().setVisible(False)
        self.users_table.setAlternatingRowColors(True)
        self.users_table.setColumnCount(5)
        self.users_table.setHorizontalHeaderLabels(["ID", "Имя", "Фамилия", "Отдел", "Роль"])
        self.users_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Настраиваем размеры столбцов
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.users_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        
        # Стилизуем таблицу
        self.users_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: #333;
                gridline-color: #E6F0FF;
                border: 1px solid #BDD7FB;
                border-top: none;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
            }
            QTableWidget::item {
                padding: 8px;
                font-size: 14px;
                border-bottom: 1px solid #E6F0FF;
            }
            QTableWidget::item:selected {
                background-color: #E6F0FF;
                color: #1A4CA3;
            }
            QTableWidget::item:hover {
                background-color: #F0F7FF;
            }
            QHeaderView::section {
                background-color: #2A58AD;
                color: white;
                font-weight: bold;
                padding: 10px;
                border: none;
                border-right: 1px solid #3968BD;
                font-size: 14px;
            }
            QScrollBar:vertical {
                background-color: #F0F7FF;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #BDD7FB;
                min-height: 30px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #9ABDF5;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar:horizontal {
                background-color: #F0F7FF;
                height: 12px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background-color: #BDD7FB;
                min-width: 30px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #9ABDF5;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                border: none;
                background: none;
            }
        """)
        
        # Добавляем таблицу в контейнер
        self.users_layout.addWidget(self.users_table, 1)
        
        # Основной контейнер
        self.users_container.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
        """)
        
        # Добавляем контейнер в основной layout
        self.form_layout.addWidget(self.users_container)
        self.form_layout.setContentsMargins(10, 10, 10, 10)  # Добавляем отступы для основного layout

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
                    
                    # Добавляем кнопку "Подробности"
                    serial_number = detail_data.get("serial_number", "")
                    if serial_number:
                        details_button = QPushButton("Подробности")
                        details_button.setStyleSheet("""
                            QPushButton {
                                background-color: #5F7ADB;
                                color: white;
                                border: none;
                                padding: 5px 10px;
                                border-radius: 3px;
                                font-size: 12px;
                            }
                            QPushButton:hover {
                                background-color: #4965c8;
                            }
                        """)
                        # Используем lambda для передачи serial_number в обработчик
                        details_button.clicked.connect(lambda checked, sn=serial_number: self.display_detail_info(sn))
                        table.setCellWidget(row, 6, details_button)
            else:
                table.setRowCount(1)  # Создаем одну строку для сообщения
                empty_item = QTableWidgetItem("Список пуст")
                empty_item.setTextAlignment(Qt.AlignCenter)
                table.setItem(0, 0, empty_item)
                table.setSpan(0, 0, 1, 7)  # Объединяем все ячейки в строке
        else:
            log_error("Ошибка при получении данных из базы данных")
            table.setRowCount(1)  # Создаем одну строку для сообщения
            error_item = QTableWidgetItem("Список пуст")
            error_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(0, 0, error_item)
            table.setSpan(0, 0, 1, 7)  # Объединяем все ячейки в строке

    def display_detail_info(self, detail_id):
        """Отображает детальную информацию о детали в диалоговом окне."""
        try:
            log_event(f"Запрос детальной информации о детали {detail_id}")
            
            # Запрашиваем полную информацию о детали
            query = {"type": "details", "serial": detail_id}
            result = database(query)
            
            log_event(f"Получен ответ от сервера: {result}")
            
            if not result or 'status' not in result or result['status'] != "ok":
                log_warning(f"Не удалось получить информацию о детали {detail_id}: {result}")
                self.show_error_message("Ошибка", f"Не удалось получить информацию о детали {detail_id}")
                return
            
            part_info = result.get('data', {})
            log_event(f"Данные для отображения: {part_info}")
            
            rfid_tag = "Нет метки"  # По умолчанию
            rfid_writes = []  # По умолчанию пустой список
            time_info = {}  # По умолчанию пустой словарь
            
            # Проверяем, есть ли поле time и преобразуем его из JSON строки в словарь
            if 'time' in part_info and part_info['time']:
                try:
                    import json
                    time_info = json.loads(part_info['time'])
                    log_event(f"Преобразованная информация о времени: {time_info}")
                except Exception as json_error:
                    log_error(f"Ошибка при преобразовании JSON поля time: {json_error}")
            
            dialog = DetailInfoDialog(part_info, rfid_tag, rfid_writes, time_info, self.main_window)
            dialog.exec_()
            
        except Exception as e:
            log_error(f"Ошибка при отображении информации о детали {detail_id}: {e}")
            self.show_error_message("Ошибка", f"Произошла ошибка: {e}")

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
        self.users_container.hide()  # Скрываем контейнер сотрудников
        
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
        elif item.text(0) == "Сотрудники":
            # Устанавливаем заголовок формы
            self.form_title.setText("")  # Оставляем заголовок пустым, так как у нас уже есть заголовок в контейнере сотрудников
            
            # Показываем контейнер с пользователями
            self.users_container.show()
            
            # Очищаем поле поиска
            self.search_input.clear()
            
            # Обновляем данные таблицы
            self.updateUsersTable()
            
            # Логирование
            log_event("Отображаем страницу списка сотрудников")
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
            # Удалено обновление таблицы сотрудников
            # if self.users_container.isVisible():
            #     self.updateUsersTable()
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
    
    def show_error_message(self, title, message):
        """Показывает сообщение об ошибке."""
        from error_test import show_error_dialog
        show_error_dialog(title, message)

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

    def updateUsersTable(self):
        """Обновляет таблицу со списком всех сотрудников"""
        query = {"type": "allUsers"}
        if not hasattr(self, 'workers'):
            self.workers = []
        worker = DatabaseWorker(query)
        worker.finished.connect(lambda result: self.on_users_finished(result))
        worker.finished.connect(lambda: self.workers.remove(worker))
        worker.finished.connect(worker.deleteLater)
        self.workers.append(worker)
        worker.start()
        log_event("Отправлен запрос на получение списка всех сотрудников")

    @Slot(dict)
    def on_users_finished(self, result):
        """Обрабатывает результат запроса на получение списка сотрудников"""
        log_event(f"Получен ответ для таблицы сотрудников: {result}")
        if result and result.get('status') == 'ok':
            users = result['data']
            log_event(f"Число полученных сотрудников: {len(users) if users else 0}")
            
            if users:  # Проверяем, есть ли данные
                # Очищаем таблицу
                self.users_table.clearContents()
                self.users_table.setRowCount(len(users))
                
                for row, user in enumerate(users):
                    self.users_table.setItem(row, 0, QTableWidgetItem(str(user.get("id", ""))))
                    self.users_table.setItem(row, 1, QTableWidgetItem(user.get("name", "")))
                    self.users_table.setItem(row, 2, QTableWidgetItem(user.get("surname", "")))
                    self.users_table.setItem(row, 3, QTableWidgetItem(user.get("profession", "")))
                    self.users_table.setItem(row, 4, QTableWidgetItem(user.get("uid", "")))
                
                # Обновляем таблицу и ее отображение
                self.users_table.resizeColumnsToContents()
                self.users_table.resizeRowsToContents()
                self.users_table.viewport().update()
                log_event("Таблица сотрудников обновлена")
            else:
                self.users_table.setRowCount(1)
                empty_item = QTableWidgetItem("Список сотрудников пуст")
                empty_item.setTextAlignment(Qt.AlignCenter)
                self.users_table.setItem(0, 0, empty_item)
                self.users_table.setSpan(0, 0, 1, 5)  # Объединяем все ячейки в строке
                log_event("Таблица сотрудников: список пуст")
        else:
            log_error("Ошибка при получении списка сотрудников из базы данных")
            self.users_table.setRowCount(1)
            error_item = QTableWidgetItem("Ошибка при получении данных")
            error_item.setTextAlignment(Qt.AlignCenter)
            self.users_table.setItem(0, 0, error_item)
            self.users_table.setSpan(0, 0, 1, 5)  # Объединяем все ячейки в строке

    def filter_users_table(self):
        search_text = self.search_input.text().lower()
        
        # Если поле поиска пустое, показываем все строки
        if not search_text:
            for row in range(self.users_table.rowCount()):
                self.users_table.setRowHidden(row, False)
            return
            
        # Иначе фильтруем строки
        for row in range(self.users_table.rowCount()):
            hide_row = True
            
            # Проверяем все ячейки в строке
            for col in range(self.users_table.columnCount()):
                item = self.users_table.item(row, col)
                if item and search_text in item.text().lower():
                    hide_row = False
                    break
                    
            # Скрываем или показываем строку
            self.users_table.setRowHidden(row, hide_row)

    def clear_search(self):
        """Очищает поле поиска и показывает все строки таблицы"""
        self.search_input.clear()
        for row in range(self.users_table.rowCount()):
            self.users_table.setRowHidden(row, False)

class DetailInfoDialog(QDialog):
    """Диалоговое окно для отображения детальной информации о детали."""
    
    def __init__(self, part_info, rfid_tag, rfid_writes, time_info, parent=None):
        super().__init__(parent)
        
        self.part_info = part_info
        self.rfid_tag = rfid_tag
        self.rfid_writes = rfid_writes
        self.time_info = time_info
        self.worker_threads = []  # Инициализируем список потоков
        
        self.setup_ui()
        self.populate_data()
        self.setup_connections()
        
    def setup_ui(self):
        """Настраивает пользовательский интерфейс диалога."""
        self.setWindowTitle("Детальная информация о детали")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                border: 2px solid #5F7ADB;
                border-radius: 10px;
            }
            QGroupBox {
                background-color: white;
                border: 1px solid #d1d9e6;
                border-radius: 8px;
                margin-top: 15px;
                font-weight: bold;
                padding: 10px;
                color: #2E3239;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 5px 10px;
                background-color: #5F7ADB;
                color: white;
                border-radius: 4px;
            }
            QLabel {
                color: #333;
                padding: 5px;
                font-size: 13px;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #d1d9e6;
                gridline-color: #e9ecef;
                border-radius: 5px;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #f1f3f5;
            }
            QTableWidget::item:selected {
                background-color: #e7f5ff;
                color: #1971c2;
            }
            QHeaderView::section {
                background-color: #5F7ADB;
                color: white;
                padding: 8px;
                font-weight: bold;
                border: none;
                border-right: 1px solid #4965c8;
            }
            QTabWidget::pane {
                border: 1px solid #d1d9e6;
                background-color: white;
                border-radius: 8px;
            }
            QTabWidget {
                background-color: transparent;
            }
            QTabBar::tab {
                background-color: #e9ecef;
                padding: 10px 20px;
                margin-right: 2px;
                margin-bottom: -1px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                border: 1px solid #d1d9e6;
                border-bottom: none;
                color: #495057;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #5F7ADB;
                color: #5F7ADB;
            }
            QTabBar::tab:hover:!selected {
                background-color: #dee2e6;
            }
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #d1d9e6;
                border-radius: 4px;
                padding: 5px;
            }
            QScrollBar:vertical {
                border: none;
                background: #f1f3f5;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #adb5bd;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        # Верхняя панель с заголовком
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        header_label = QLabel("Информация о детали")
        header_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2E3239;
            padding: 10px;
            background-color: #e7f5ff;
            border-radius: 5px;
        """)
        header_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(header_label)
        
        main_layout.addWidget(header_widget)
        
        # Создаем вкладки
        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)
        
        # Вкладка основной информации
        self.info_tab = QWidget()
        info_layout = QVBoxLayout(self.info_tab)
        info_layout.setContentsMargins(10, 10, 10, 10)
        info_layout.setSpacing(15)
        
        # Основная информация о детали
        self.info_group = QGroupBox("Основная информация")
        info_form_layout = QFormLayout(self.info_group)
        info_form_layout.setLabelAlignment(Qt.AlignRight)
        info_form_layout.setFormAlignment(Qt.AlignLeft)
        info_form_layout.setSpacing(12)
        info_form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        
        self.part_id_label = QLabel("Загрузка...")
        self.part_name_label = QLabel("Загрузка...")
        self.rfid_tag_label = QLabel("Загрузка...")
        self.status_label = QLabel("Загрузка...")
        self.current_stage_label = QLabel("Загрузка...")
        self.storage_sector_label = QLabel("Загрузка...")
        self.note_text = QTextEdit()
        self.note_text.setReadOnly(True)
        self.note_text.setMinimumHeight(100)
        
        # Стили для меток
        self.part_id_label.setStyleSheet("font-weight: bold; color: #5F7ADB; font-size: 14px;")
        self.status_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        info_form_layout.addRow("<b>ID детали:</b>", self.part_id_label)
        info_form_layout.addRow("<b>Название:</b>", self.part_name_label)
        info_form_layout.addRow("<b>Статус:</b>", self.status_label)
        info_form_layout.addRow("<b>Текущий этап:</b>", self.current_stage_label)
        info_form_layout.addRow("<b>Место хранения:</b>", self.storage_sector_label)
        info_form_layout.addRow("<b>Примечание:</b>", self.note_text)
        
        info_layout.addWidget(self.info_group)
        
        # Вкладка информации о времени
        self.time_tab = QWidget()
        self.time_layout = QVBoxLayout(self.time_tab)
        self.time_layout.setContentsMargins(10, 10, 10, 10)
        self.time_layout.setSpacing(15)
        
        # Заголовок для вкладки времени
        time_header = QLabel("История прохождения этапов")
        time_header.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #2E3239;
            padding: 5px;
            border-bottom: 2px solid #5F7ADB;
        """)
        time_header.setAlignment(Qt.AlignCenter)
        self.time_layout.addWidget(time_header)
        
        # Добавляем вкладки в виджет вкладок
        self.tab_widget.addTab(self.info_tab, "Основная информация")
        self.tab_widget.addTab(self.time_tab, "История этапов")
        
        main_layout.addWidget(self.tab_widget)
        
        # Кнопки внизу диалога
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.setStyleSheet("""
            QPushButton {
                background-color: #5F7ADB;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #4965c8;
            }
            QPushButton:pressed {
                background-color: #3b51a3;
            }
        """)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)
        
        # Обновляем геометрию
        self.updateGeometry()

    def populate_data(self):
        """Заполняет интерфейс данными о детали."""
        log_event(f"Начинаем заполнение данных в диалоге. part_info: {self.part_info}")
        # Заполняем основную информацию
        part_id = self.part_info.get('id', 'Нет данных')
        log_event(f"ID детали: {part_id}")
        self.part_id_label.setText(str(part_id))
        
        part_name = self.part_info.get('name', 'Нет данных')
        log_event(f"Название детали: {part_name}")
        self.part_name_label.setText(part_name)
        
        self.rfid_tag_label.setText(str(self.rfid_tag))
        
        # Проверка статуса и установка значения
        status = self.part_info.get('defective', None)
        log_event(f"Статус (defective): {status}")
        
        if status is None:
            status_text = "Нет данных"
        elif status == 1 or status == "1" or status is True:
            status_text = "Брак"
        else:
            status_text = "Годен"
        log_event(f"Текст статуса: {status_text}")
        self.status_label.setText(status_text)
        
        current_stage = self.part_info.get('stage', 'Нет данных')
        log_event(f"Текущий этап: {current_stage}")
        self.current_stage_label.setText(current_stage)
        
        storage_sector = self.part_info.get('sector', None)
        log_event(f"Сектор хранения: {storage_sector}")
        if storage_sector is None or storage_sector == "":
            self.storage_sector_label.setText("Не хранится")
        else:
            self.storage_sector_label.setText(str(storage_sector))
        
        note = self.part_info.get('note', '')
        log_event(f"Примечание: {note}")
        self.note_text.setText(note if note else "Нет примечаний")
        
        # Заполняем информацию о времени прохождения этапов
        log_event(f"Обрабатываем данные времени: {self.time_info}")
        self.process_time_info(self.time_info)
        log_event("Завершено заполнение данных в диалоге")

    def process_time_info(self, time_data):
        """Обрабатывает информацию о времени для этапов и отображает на интерфейсе"""
        try:
            log_event(f"Обработка информации о времени: {time_data}")
            
            # Очистка существующих виджетов в макете времени
            self.clear_layout(self.time_layout)
            
            # Заголовок
            header_label = QLabel("История прохождения этапов")
            header_label.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                color: #2E3239;
                padding: 8px;
                border-bottom: 2px solid #5F7ADB;
            """)
            header_label.setAlignment(Qt.AlignCenter)
            self.time_layout.addWidget(header_label)
            
            # Проверяем, есть ли поле time в информации о детали
            mark_time = self.part_info.get('time')
            if mark_time and not time_data:
                log_event(f"Найдено поле time в информации о детали: {mark_time}")
                # Создаем структуру для этапа mark с временем из поля time
                time_data = {
                    "mark": {
                        "time": mark_time
                    }
                }
            
            if not time_data or not isinstance(time_data, dict):
                warning_widget = QWidget()
                warning_layout = QVBoxLayout(warning_widget)
                warning_icon = QLabel("ℹ️")
                warning_icon.setAlignment(Qt.AlignCenter)
                warning_icon.setStyleSheet("font-size: 24px; margin: 10px;")
                warning_text = QLabel("Нет данных о времени по этапам")
                warning_text.setAlignment(Qt.AlignCenter)
                warning_text.setStyleSheet("color: #6c757d; font-style: italic; font-size: 14px;")
                warning_layout.addWidget(warning_icon)
                warning_layout.addWidget(warning_text)
                warning_widget.setStyleSheet("""
                    background-color: #f8f9fa;
                    border: 1px dashed #ced4da;
                    border-radius: 8px;
                    margin: 20px;
                """)
                self.time_layout.addWidget(warning_widget)
                return
            
            # Создаем прокручиваемую область для этапов
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setStyleSheet("""
                QScrollArea {
                    border: none;
                    background-color: transparent;
                }
            """)
            
            scroll_content = QWidget()
            scroll_layout = QVBoxLayout(scroll_content)
            scroll_layout.setContentsMargins(5, 5, 5, 5)
            scroll_layout.setSpacing(15)
            
            # Сортируем этапы по дате начала (если она есть)
            stages = []
            for stage_name, stage_info in time_data.items():
                if stage_name != 'sector' and isinstance(stage_info, dict):
                    # Для обычных этапов используем start, для этапа mark используем time
                    if stage_name == "mark" and "time" in stage_info:
                        stage_start = stage_info.get('time')
                    else:
                        stage_start = stage_info.get('start')
                    stages.append((stage_name, stage_info, stage_start))
            
            # Сортировка по времени начала
            sorted_stages = sorted(stages, key=lambda x: x[2] if x[2] else "")
            
            # Для каждого этапа создаем красивый виджет
            for index, (stage_name, stage_info, _) in enumerate(sorted_stages):
                stage_widget = QGroupBox()
                
                # Чередующиеся цвета для виджетов этапов
                if index % 2 == 0:
                    stage_widget.setStyleSheet("""
                        QGroupBox {
                            background-color: #f0f7ff;
                            border: 1px solid #bdd7f9;
                            border-radius: 8px;
                            padding: 10px;
                            margin: 5px;
                        }
                    """)
                else:
                    stage_widget.setStyleSheet("""
                        QGroupBox {
                            background-color: #fff9f0;
                            border: 1px solid #f9e5bd;
                            border-radius: 8px;
                            padding: 10px;
                            margin: 5px;
                        }
                    """)
                
                stage_layout = QVBoxLayout(stage_widget)
                
                # Заголовок этапа
                stage_header = QLabel(f"Этап: {stage_name}")
                stage_header.setStyleSheet("""
                    font-size: 14px;
                    font-weight: bold;
                    color: #2E3239;
                    padding: 5px;
                    border-bottom: 1px solid #dee2e6;
                """)
                stage_layout.addWidget(stage_header)
                
                # Времена начала и окончания или просто время для mark
                time_table = QWidget()
                time_table_layout = QFormLayout(time_table)
                time_table_layout.setLabelAlignment(Qt.AlignRight)
                time_table_layout.setFormAlignment(Qt.AlignLeft)
                time_table_layout.setSpacing(5)
                time_table_layout.setContentsMargins(5, 5, 5, 5)
                
                # Обработка особого случая для этапа mark
                if stage_name == "mark" and "time" in stage_info:
                    mark_time_value = stage_info.get('time')
                    if mark_time_value:
                        time_label = QLabel(self.format_time(mark_time_value))
                        time_label.setStyleSheet("color: #0d6efd; font-weight: bold;")
                        time_table_layout.addRow("<b>Время маркировки:</b>", time_label)
                    else:
                        no_time_label = QLabel("Время маркировки не зафиксировано")
                        no_time_label.setStyleSheet("color: #6c757d; font-style: italic;")
                        time_table_layout.addRow("", no_time_label)
                else:
                    # Стандартная обработка для обычных этапов
                    start_time = stage_info.get('start')
                    end_time = stage_info.get('end')
                    
                    if start_time:
                        start_label = QLabel(self.format_time(start_time))
                        start_label.setStyleSheet("color: #0d6efd; font-weight: bold;")
                        time_table_layout.addRow("<b>Начало:</b>", start_label)
                    
                    if end_time:
                        end_label = QLabel(self.format_time(end_time))
                        end_label.setStyleSheet("color: #198754; font-weight: bold;")
                        time_table_layout.addRow("<b>Окончание:</b>", end_label)
                    
                    if not start_time and not end_time:
                        no_time_label = QLabel("Время выполнения не зафиксировано")
                        no_time_label.setStyleSheet("color: #6c757d; font-style: italic;")
                        time_table_layout.addRow("", no_time_label)
                
                stage_layout.addWidget(time_table)
                
                # Информация о пользователе
                user_id = stage_info.get('user')
                if user_id:
                    user_frame = QFrame()
                    user_frame.setStyleSheet("""
                        QFrame {
                            background-color: rgba(255, 255, 255, 0.7);
                            border-radius: 5px;
                            padding: 5px;
                        }
                    """)
                    user_layout = QHBoxLayout(user_frame)
                    user_layout.setContentsMargins(5, 5, 5, 5)
                    
                    user_icon = QLabel("👤")
                    user_layout.addWidget(user_icon)
                    
                    user_label = QLabel(f"Исполнитель: загрузка... (ID: {user_id})")
                    user_label.setStyleSheet("color: #495057;")
                    user_layout.addWidget(user_label)
                    
                    stage_layout.addWidget(user_frame)
                    
                    # Получаем информацию о пользователе
                    self.get_user_name_and_update(user_id, stage_name, user_label)
                else:
                    user_frame = QFrame()
                    user_frame.setStyleSheet("""
                        QFrame {
                            background-color: rgba(255, 255, 255, 0.7);
                            border-radius: 5px;
                            padding: 5px;
                        }
                    """)
                    user_layout = QHBoxLayout(user_frame)
                    user_layout.setContentsMargins(5, 5, 5, 5)
                    
                    user_icon = QLabel("❓")
                    user_layout.addWidget(user_icon)
                    
                    user_label = QLabel("Исполнитель не указан")
                    user_label.setStyleSheet("color: #6c757d; font-style: italic;")
                    user_layout.addWidget(user_label)
                    
                    stage_layout.addWidget(user_frame)
                
                scroll_layout.addWidget(stage_widget)
            
            # Добавляем растягивающийся элемент в конец
            spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            scroll_layout.addItem(spacer)
            
            scroll_area.setWidget(scroll_content)
            self.time_layout.addWidget(scroll_area)
            
        except Exception as e:
            log_error(f"Ошибка при обработке информации о времени: {e}")
            error_widget = QWidget()
            error_layout = QVBoxLayout(error_widget)
            
            error_icon = QLabel("⚠️")
            error_icon.setAlignment(Qt.AlignCenter)
            error_icon.setStyleSheet("font-size: 24px; margin: 10px;")
            
            error_text = QLabel(f"Ошибка обработки данных: {e}")
            error_text.setAlignment(Qt.AlignCenter)
            error_text.setStyleSheet("color: #dc3545; font-size: 14px;")
            error_text.setWordWrap(True)
            
            error_layout.addWidget(error_icon)
            error_layout.addWidget(error_text)
            
            error_widget.setStyleSheet("""
                background-color: #fff5f5;
                border: 1px solid #ffcccc;
                border-radius: 8px;
                margin: 20px;
            """)
            
            self.time_layout.addWidget(error_widget)

    def get_user_name_and_update(self, user_id, stage, user_label):
        """Получает имя пользователя по ID и обновляет интерфейс."""
        try:
            log_event(f"Запрашиваем информацию о пользователе с ID: {user_id} для этапа {stage}")
            
            # Отправляем запрос на получение данных о пользователе
            query = {"type": "userById", "id": user_id}
            
            # Сохраняем ID пользователя, которого запрашиваем
            user_label.setProperty("requested_user_id", user_id)
            
            # Создаем отдельный поток для запроса информации о пользователе
            worker = DatabaseWorker(query)
            worker.finished.connect(lambda result, label=user_label, stage_name=stage, uid=user_id: 
                                    self.update_user_label(result, label, stage_name, uid))
            worker.finished.connect(lambda: self.clean_up_thread(worker))
            worker.finished.connect(worker.deleteLater)
            
            # Добавляем поток в список для отслеживания
            self.worker_threads.append(worker)
            worker.start()
            
        except Exception as e:
            log_error(f"Общая ошибка при получении данных о пользователе: {e}")
            user_label.setText(f"Исполнитель: ошибка ({str(e)[:30]}...)" if len(str(e)) > 30 else f"Исполнитель: ошибка ({e})")

    def update_user_label(self, result, label, stage_name, requested_user_id):
        """Обновляет метку с именем пользователя после получения данных."""
        try:
            log_event(f"Обработка результата для этапа {stage_name}, запрошенный ID: {requested_user_id}, результат: {result}")
            
            # Получаем ID пользователя, для которого был сделан запрос
            label_user_id = label.property("requested_user_id")
            
            # Проверяем, совпадает ли ID в ответе с ID для этой метки
            if str(label_user_id) != str(requested_user_id):
                log_warning(f"ID пользователя в метке ({label_user_id}) не совпадает с запрошенным ID ({requested_user_id}). Пропускаем обновление.")
                return
            
            if result and result.get('status') == 'ok' and 'data' in result:
                user_data = result.get('data', [])
                
                # Проверяем, что user_data это список или словарь и не пустой
                if user_data:
                    # Обрабатываем случай, когда API возвращает список
                    if isinstance(user_data, list) and len(user_data) > 0:
                        user_data = user_data[0]  # Берем первый элемент списка
                    
                    # Теперь user_data должен быть словарем
                    if isinstance(user_data, dict):
                        user_id_from_data = user_data.get('id')
                        
                        name = user_data.get('name', 'Неизвестно')
                        surname = user_data.get('surname', 'Неизвестно')
                        prof = user_data.get('profession', 'Неизвестно')
                        full_name = f"{surname} {name}"
                        
                        # Определяем цвет метки в зависимости от ID пользователя
                        color_styles = {
                            "1": "color: #0d6efd; font-weight: bold;",  # Синий
                            "2": "color: #198754; font-weight: bold;",  # Зеленый
                            "3": "color: #dc3545; font-weight: bold;",  # Красный
                            "4": "color: #fd7e14; font-weight: bold;",  # Оранжевый
                            "5": "color: #6f42c1; font-weight: bold;",  # Фиолетовый
                        }
                        
                        id_str = str(user_id_from_data)
                        style = color_styles.get(id_str, "color: #495057; font-weight: bold;")
                        label.setStyleSheet(style)
                        
                        # Явно добавляем ID пользователя в текст
                        label.setText(f"Исполнитель [{id_str}]: {full_name} ({prof})")
                        log_event(f"Метка пользователя обновлена для этапа {stage_name}: {full_name}, ID: {user_id_from_data}")
                    else:
                        label.setText(f"Исполнитель: некорректный формат данных")
                        log_error(f"Некорректный формат данных пользователя: {type(user_data)}")
                else:
                    label.setText(f"Исполнитель: данные не найдены для ID {requested_user_id}")
                    log_error(f"Пустые данные о пользователе для этапа {stage_name}, ID: {requested_user_id}")
            else:
                error_msg = result.get('message') if result and 'message' in result else 'Данные не найдены'
                label.setText(f"Исполнитель: {error_msg} (ID: {requested_user_id})")
                log_error(f"Не удалось получить данные о пользователе для этапа {stage_name}, ID: {requested_user_id}: {error_msg}")
        except Exception as e:
            log_error(f"Ошибка при обновлении метки пользователя для этапа {stage_name}, ID: {requested_user_id}: {e}")
            label.setText(f"Исполнитель: ошибка ({str(e)[:30]}...)")

    def closeEvent(self, event):
        """Перехватываем событие закрытия окна для корректного завершения потоков."""
        # Пытаемся остановить все потоки
        for thread in self.worker_threads:
            if thread.isRunning():
                thread.quit()
                thread.wait(500)  # Ждем до 500 мс
        
        event.accept()

    def clean_up_thread(self, thread):
        """Удаляет поток из списка активных потоков."""
        if thread in self.worker_threads:
            self.worker_threads.remove(thread)

    def setup_connections(self):
        """Устанавливает сигнал-слот соединения для виджетов."""
        # Здесь будут подключения сигналов к слотам, если они понадобятся
        pass

    def format_time(self, time_str):
        """Форматирует временную метку в читаемый вид."""
        try:
            # Проверяем, является ли строка уже отформатированной
            if isinstance(time_str, str) and len(time_str) >= 19:
                # Предполагаем формат: "YYYY-MM-DD HH:MM:SS"
                return time_str
            else:
                return str(time_str)
        except Exception as e:
            log_error(f"Ошибка при форматировании времени: {e}")
            return str(time_str)

    def clear_layout(self, layout):
        """Очищает все виджеты из макета."""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    # Если элемент является подмакетом
                    self.clear_layout(item.layout())

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
