from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QTableView,
    QWidget, QVBoxLayout)

class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):

        self.setWindowTitle("Главная страница")
        self.setGeometry(0, 0, 1000, 800)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Левая область
        left_widget = QWidget(central_widget)
        left_widget.setGeometry(0, 120, 550, 680)
        left_widget.setStyleSheet("background-color: rgb(235, 240, 255);")

        # Поле ввода категории детали
        label_category = QLabel("Введите категорию детали:", left_widget)
        label_category.setGeometry(70, 30, 225, 40)
        label_category.setStyleSheet("font: 16px; font-weight: 600;")

        line_edit_category = QLineEdit(left_widget)
        line_edit_category.setGeometry(110, 80, 250, 40)

        # Выпадающий список для маркировки товара
        label_marking = QLabel("Введите маркировку товара:", left_widget)
        label_marking.setGeometry(70, 150, 225, 40)
        label_marking.setStyleSheet("font: 16px; font-weight: 600;")

        combo_box_marking = QComboBox(left_widget)
        combo_box_marking.setGeometry(110, 210, 250, 40)
        combo_box_marking.addItems(["Метран 150", "Метран 75", "Метран 55"])

        # Поле ввода метки детали
        label_tag = QLabel("Метка детали:", left_widget)
        label_tag.setGeometry(70, 270, 225, 40)
        label_tag.setStyleSheet("font: 16px; font-weight: 600;")

        line_edit_tag = QLineEdit(left_widget)
        line_edit_tag.setGeometry(110, 320, 250, 40)

        # Кнопка "Внести деталь"
        button_add_detail = QPushButton("Внести деталь", left_widget)
        button_add_detail.setGeometry(180, 420, 200, 50)
        button_add_detail.setStyleSheet(
            "background-color: #5F7ADB; color: rgb(255, 255, 255); border-radius: 20px; font: 20px; font-weight: 700;"
        )

        # Кнопка "Сообщить о проблеме"
        button_report_issue = QPushButton("Сообщить о проблеме", left_widget)
        button_report_issue.setGeometry(130, 520, 300, 50)
        button_report_issue.setStyleSheet(
            "background-color: #2E3239; color: rgb(255, 255, 255); border-radius: 20px; font: 20px; font-weight: 700;"
        )

        # Кнопка "Сообщить о браке"
        button_report_defect = QPushButton("Сообщить о браке", left_widget)
        button_report_defect.setGeometry(130, 600, 300, 50)
        button_report_defect.setStyleSheet(
            "background-color: #2E3239; color: rgb(255, 255, 255); border-radius: 20px; font: 20px; font-weight: 700;"
        )

        # Правая область
        right_widget = QWidget(central_widget)
        right_widget.setGeometry(550, 50, 450, 750)
        right_widget.setStyleSheet("background-color: rgb(235, 240, 255);")

        layout_widget = QWidget(right_widget)
        layout_widget.setGeometry(100, 60, 271, 611)

        v_layout = QVBoxLayout(layout_widget)
        for _ in range(5):
            label = QLabel("TextLabel")
            label.setAlignment(Qt.AlignCenter)
            v_layout.addWidget(label)

        # Верхний виджет с кнопками
        top_widget = QWidget(central_widget)
        top_widget.setGeometry(0, 0, 1000, 50)
        top_widget.setStyleSheet("background-color: #2E3239; color: #5F7ADB; font: 20px; font-weight: 700;")

        buttons = [
            ("Маркировка", 110),
            ("Обработка", 290),
            ("Тестирование", 470),
            ("Упаковка", 650),
            ("Админ панель", 830),
        ]

        for text, x in buttons:
            button = QPushButton(text, top_widget)
            button.setGeometry(x, 0, 180, 50)

        # Лейбл с именем
        name_label = QLabel("Василий Пупкин", central_widget)
        name_label.setGeometry(50, 10, 450, 40)
        name_label.setStyleSheet("font: 35px; padding-left: 10px; font-weight: 600;")

    def updateName(self, name):
        
        self.name_label.setText(name)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0413\u043b\u0430\u0432\u043d\u0430\u044f \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044e \u0434\u0435\u0442\u0430\u043b\u0438:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043c\u0430\u0440\u043a\u0438\u0440\u043e\u0432\u043a\u0443 \u0442\u043e\u0432\u0430\u0440\u0430:", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u0412\u043d\u0435\u0441\u0442\u0438 \u0434\u0435\u0442\u0430\u043b\u044c ", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0435\u0442\u043a\u0430 \u0434\u0435\u0442\u0430\u043b\u0438:", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u043e\u0431\u0449\u0438\u0442\u044c \u043e \u0431\u0440\u0430\u043a\u0435", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"\u041c\u0435\u0442\u0440\u0430\u043d 150", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"\u041c\u0435\u0442\u0440\u0430\u043d 75", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"\u041c\u0435\u0442\u0440\u0430\u043d 55", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u043e\u0431\u0449\u0438\u0442\u044c \u043e \u043f\u0440\u043e\u0431\u043b\u0435\u043c\u0435", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0430\u0440\u043a\u0438\u0440\u043e\u0432\u043a\u0430", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0435\u0441\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"\u0423\u043f\u0430\u043a\u043e\u0432\u043a\u0430", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"\u0410\u0434\u043c\u0438\u043d \u043f\u0430\u043d\u0435\u043b\u044c", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430", None))
        self.label_9.setText("")
    # retranslateUi



    def open_confirmation_window(self):
        # Создание окна подтверждения
        self.confirmation_window = QWidget()
        self.confirmation_window.setWindowTitle("Подтверждение данных")
        self.confirmation_window.setGeometry(375, 150, 250, 500)
        self.confirmation_window.setStyleSheet("background-color: #F0F0F0;")

        layout = QVBoxLayout(self.confirmation_window)
        layout.addWidget(QLabel(f"Категория детали: {self.lineEdit.text()}"))
        layout.addWidget(QLabel(f"Маркировка товара: {self.comboBox.currentText()}"))
        layout.addWidget(QLabel(f"######: {self.lineEdit_3.text()}"))

        button_confirm = QPushButton("Данные верны")
        button_confirm.clicked.connect(self.confirm_data)
        layout.addWidget(button_confirm)

        button_edit = QPushButton("Изменить данные")
        button_edit.clicked.connect(self.edit_data)
        layout.addWidget(button_edit)

        self.confirmation_window.show()

    def confirm_data(self):
        self.lineEdit.clear()
        self.comboBox.clear()
        self.lineEdit_3.clear()
        self.confirmation_window.close()

    def edit_data(self):
        self.confirmation_window.close()

if __name__ == "__main__":
    app = QApplication([])
    window = Ui_MainWindow()
    window.show()
    app.exec()
