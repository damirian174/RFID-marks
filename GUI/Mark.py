# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MarkXOwPlZ.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QLayout,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)
from detail_work import end_work

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1300, 750)
        MainWindow.setTabletTracking(False)
        MainWindow.setStyleSheet(u"background-color:rgb(255, 255, 255)")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(0, 120, 550, 680))
        self.widget_2.setStyleSheet(u"background-color: rgb(235, 240, 255);")
        self.lineEdit = QLineEdit(self.widget_2)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(110, 80, 250, 40))
        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(70, 30, 225, 40))
        self.label.setStyleSheet(u"font: 16px;\n"
"font-weight: 600;")
        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(70, 150, 225, 40))
        self.label_3.setStyleSheet(u"font: 16px;\n"
"font-weight: 600;")
        self.pushButton = QPushButton(self.widget_2)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(180, 420, 200, 50))
        self.pushButton.setStyleSheet(u"background-color: #5F7ADB;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"font: 20px;\n"
"font-weight: 700;")
        self.label_4 = QLabel(self.widget_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(70, 270, 225, 40))
        self.label_4.setStyleSheet(u"font: 16px;\n"
"font-weight: 600;")
        self.lineEdit_3 = QLineEdit(self.widget_2)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(110, 320, 250, 40))
        self.comboBox = QComboBox(self.widget_2)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(110, 210, 250, 40))
        self.widget_3 = QWidget(self.centralwidget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setGeometry(QRect(550, 50, 450, 750))
        self.widget_3.setStyleSheet(u"background-color: rgb(235, 240, 255);")
        self.pushButton_4 = QPushButton(self.widget_3)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(20, 90, 300, 50))
        self.pushButton_4.setStyleSheet(u"background-color: #2E3239;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"font: 20px;\n"
"font-weight: 700;")
        self.pushButton_3 = QPushButton(self.widget_3)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(20, 200, 300, 50))
        self.pushButton_3.setStyleSheet(u"background-color: #2E3239;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"font: 20px;\n"
"font-weight: 700;")
        self.pushButton_9 = QPushButton(self.widget_3)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setGeometry(QRect(20, 310, 300, 50))
        self.pushButton_9.setStyleSheet(u"background-color: #2E3239;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"font: 20px;\n"
"font-weight: 700;")
        self.pushButton_15 = QPushButton(self.widget_3)
        self.pushButton_15.setObjectName(u"pushButton_15")
        self.pushButton_15.setGeometry(QRect(20, 420, 300, 50))
        self.pushButton_15.setStyleSheet(u"background-color: #2E3239;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"font: 20px;\n"
"font-weight: 700;")
        self.widget_4 = QWidget(self.centralwidget)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setGeometry(QRect(0, 50, 550, 70))
        self.widget_4.setStyleSheet(u"background-color: rgb(235, 240, 255);\n"
"color: #26292B;")
        self.label_2 = QLabel(self.widget_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(50, 10, 450, 40))
        self.label_2.setStyleSheet(u"font: 35px;\n"
"padding-left: 10px;\n"
"font-weight: 600;")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 1300, 50))
        self.widget.setStyleSheet(u"color: #5F7ADB;\n"
"font: 20px;\n"
"background-color: #2E3239;\n"
"font-weight: 700;\n"
"")
        self.pushButton_7 = QPushButton(self.widget)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setGeometry(QRect(110, 0, 240, 50))
        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(590, 0, 240, 50))
        self.pushButton_2.setStyleSheet(u"")
        self.pushButton_5 = QPushButton(self.widget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(830, 0, 240, 50))
        self.pushButton_8 = QPushButton(self.widget)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setGeometry(QRect(350, 0, 240, 50))
        self.widget_7 = QWidget(self.widget)
        self.widget_7.setObjectName(u"widget_7")
        self.widget_7.setGeometry(QRect(0, 0, 110, 50))
        self.label_9 = QLabel(self.widget_7)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(0, 0, 110, 50))
        self.label_9.setPixmap(QPixmap(u"Frame 1 (1).png"))
        self.pushButton_6 = QPushButton(self.widget)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(1070, 0, 230, 50))
        self.widget_5 = QWidget(self.centralwidget)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setGeometry(QRect(1000, 50, 301, 701))
        self.widget_5.setStyleSheet(u"background-color: rgb(235, 240, 255);")
        self.verticalLayoutWidget = QWidget(self.widget_5)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 40, 271, 611))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.name = QLabel(self.verticalLayoutWidget)
        self.name.setObjectName(u"name")
        self.name.setStyleSheet(u"background-color: #5F7ADB;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"font: 20px;\n"
"font-weight: 700;")
        self.name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.name)

        self.serial = QLabel(self.verticalLayoutWidget)
        self.serial.setObjectName(u"serial")
        self.serial.setStyleSheet(u"background-color: #5F7ADB;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"font: 20px;\n"
"font-weight: 700;")
        self.serial.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.serial)

        self.defective = QLabel(self.verticalLayoutWidget)
        self.defective.setObjectName(u"defective")
        self.defective.setStyleSheet(u"background-color: #5F7ADB;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"font: 20px;\n"
"font-weight: 700;")
        self.defective.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.defective)

        self.stage = QLabel(self.verticalLayoutWidget)
        self.stage.setObjectName(u"stage")
        self.stage.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.stage.setStyleSheet(u"background-color: #5F7ADB;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"font: 20px;\n"
"font-weight: 700;")
        self.stage.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.stage)

        self.sector = QLabel(self.verticalLayoutWidget)
        self.sector.setObjectName(u"sector")
        self.sector.setStyleSheet(u"background-color: #5F7ADB;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"font: 20px;\n"
"font-weight: 700;")
        self.sector.setAlignment(Qt.AlignmentFlag.AlignCenter)
        

        self.verticalLayout.addWidget(self.sector)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0413\u043b\u0430\u0432\u043d\u0430\u044f \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044e \u0434\u0435\u0442\u0430\u043b\u0438:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043c\u0430\u0440\u043a\u0438\u0440\u043e\u0432\u043a\u0443 \u0442\u043e\u0432\u0430\u0440\u0430:", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", "\u0412\u043d\u0435\u0441\u0442\u0438 \u0434\u0435\u0442\u0430\u043b\u044c ", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0435\u0442\u043a\u0430 \u0434\u0435\u0442\u0430\u043b\u0438:", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"\u041c\u0435\u0442\u0440\u0430\u043d 150", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"\u041c\u0435\u0442\u0440\u0430\u043d 75", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"\u041c\u0435\u0442\u0440\u0430\u043d 55", None))

        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u043e\u0431\u0449\u0438\u0442\u044c \u043e \u043f\u0440\u043e\u0431\u043b\u0435\u043c\u0435", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u043e\u0431\u0449\u0438\u0442\u044c \u043e \u0431\u0440\u0430\u043a\u0435", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0432\u0435\u0440\u0448\u0438\u0442\u044c \u0440\u0430\u0431\u043e\u0442\u0443", None))
        self.pushButton_15.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043e\u0439\u0442\u0438", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0430\u0441\u0438\u043b\u0438\u0439 \u041f\u0443\u043f\u043a\u0438\u043d", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0430\u0440\u043a\u0438\u0440\u043e\u0432\u043a\u0430", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0435\u0441\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"\u0423\u043f\u0430\u043a\u043e\u0432\u043a\u0430", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430", None))
        self.label_9.setText("")
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"\u0410\u0434\u043c\u0438\u043d \u043f\u0430\u043d\u0435\u043b\u044c", None))
        self.name.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.serial.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.defective.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.stage.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.sector.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.pushButton.clicked.connect(self.open_confirmation_window)
        self.detail()
    # retranslateUi



        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi
    def detail(self, data=None):
        
                # name VARCHAR(100) NOT NULL,
                # serial_number VARCHAR(100) NOT NULL UNIQUE,
                # defective BOOLEAN DEFAULT FALSE,
                # stage VARCHAR(50),
                # sector VARCHAR(100) DEFAULT NULL,
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
        end_work()
        self.lineEdit.clear()
        self.comboBox.clear()
        self.lineEdit_3.clear()
        
        self.confirmation_window.close()

    def edit_data(self):
        self.confirmation_window.close()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
    