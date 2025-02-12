# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TestsTzlgnq.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QLabel, QLayout,
    QMainWindow, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget, QMessageBox)
from detail_work import end_work, pause_work, couintine_work


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1300, 750)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(0, 50, 1000, 750))
        self.widget_2.setStyleSheet(u"background-color: rgb(235, 240, 255);")
        self.widget_3 = QWidget(self.widget_2)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setGeometry(QRect(0, 0, 550, 750))
        self.widget_5 = QWidget(self.widget_3)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setGeometry(QRect(0, 0, 550, 70))
        self.widget_5.setStyleSheet(u"background-color: rgb(235, 240, 255);\n"
"color: #26292B;")
        self.label_2 = QLabel(self.widget_5)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(50, 10, 450, 40))
        self.label_2.setStyleSheet(u"font: 35px;\n"
"padding-left: 10px;\n"
"font-weight: 600;")
        self.widget_6 = QWidget(self.widget_3)
        self.widget_6.setObjectName(u"widget_6")
        self.widget_6.setGeometry(QRect(0, 70, 550, 680))
        self.label = QLabel(self.widget_6)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(175, 30, 200, 50))
        self.label.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: #2E3239;\n"
"font: 35px;\n"
"font-weight: 700;\n"
"border-radius: 15px;")
        self.widget_7 = QWidget(self.widget_6)
        self.widget_7.setObjectName(u"widget_7")
        self.widget_7.setGeometry(QRect(0, 100, 550, 450))
        self.widget_7.setStyleSheet(u"background-color: #5F7ADB;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 50px;")
        self.pushButton = QPushButton(self.widget_7)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(100, 370, 350, 60))
        self.pushButton.setStyleSheet(u"font: 25px;\n"
"font-weight: 600;\n"
"background-color: #2E3239;\n"
"border-radius: 30px;")
        self.checkBox = QCheckBox(self.widget_7)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(100, 60, 400, 40))
        self.checkBox.setStyleSheet(u"font: 20px;\n"
"font-weight: 600;")
        self.checkBox_2 = QCheckBox(self.widget_7)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setGeometry(QRect(100, 160, 400, 40))
        self.checkBox_2.setStyleSheet(u"font: 20px;\n"
"font-weight: 600;")
        self.checkBox_3 = QCheckBox(self.widget_7)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setGeometry(QRect(100, 260, 400, 40))
        self.checkBox_3.setStyleSheet(u"font: 20px;\n"
"font-weight: 600;")
        self.widget_4 = QWidget(self.widget_2)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setGeometry(QRect(550, 0, 450, 750))
        self.pushButton_9 = QPushButton(self.widget_4)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setGeometry(QRect(90, 310, 300, 50))
        self.pushButton_9.setStyleSheet(u"background-color: #2E3239;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"font: 20px;\n"
"font-weight: 700;")
        self.pushButton_4 = QPushButton(self.widget_4)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(90, 90, 300, 50))
        self.pushButton_4.setStyleSheet(u"background-color: #2E3239;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"font: 20px;\n"
"font-weight: 700;")
        self.pushButton_3 = QPushButton(self.widget_4)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(90, 200, 300, 50))
        self.pushButton_3.setStyleSheet(u"background-color: #2E3239;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"font: 20px;\n"
"font-weight: 700;")
        self.pushButton_15 = QPushButton(self.widget_4)
        self.pushButton_15.setObjectName(u"pushButton_15")
        self.pushButton_15.setGeometry(QRect(90, 420, 300, 50))
        self.pushButton_15.setStyleSheet(u"background-color: #2E3239;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"font: 20px;\n"
"font-weight: 700;")
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
        self.widget_8 = QWidget(self.widget)
        self.widget_8.setObjectName(u"widget_8")
        self.widget_8.setGeometry(QRect(0, 0, 110, 50))
        self.label_9 = QLabel(self.widget_8)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(0, 0, 110, 50))
        self.label_9.setPixmap(QPixmap(u"\u041c\u0435\u0442\u0440\u0430\u043d.jpg"))
        self.pushButton_6 = QPushButton(self.widget)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(1070, 0, 230, 50))
        self.widget_9 = QWidget(self.centralwidget)
        self.widget_9.setObjectName(u"widget_9")
        self.widget_9.setGeometry(QRect(1000, 50, 301, 711))
        self.widget_9.setStyleSheet(u"background-color: rgb(235, 240, 255);")
        self.verticalLayoutWidget = QWidget(self.widget_9)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 50, 271, 611))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.serial = QLabel(self.verticalLayoutWidget)
        self.serial.setObjectName(u"serial")
        self.serial.setStyleSheet(u"background-color: #5F7ADB;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"font: 20px;\n"
"font-weight: 700;")
        self.serial.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.serial)

        self.name = QLabel(self.verticalLayoutWidget)
        self.name.setObjectName(u"name")
        self.name.setStyleSheet(u"background-color: #5F7ADB;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"font: 20px;\n"
"font-weight: 700;")
        self.name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.name)

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
        self.pushButton_15.clicked.connect(self.away)
        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Tests", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0430\u0441\u0438\u043b\u0438\u0439 \u041f\u0443\u043f\u043a\u0438\u043d", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"     \u0422\u0435\u0441\u0442\u044b", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0432\u0435\u0440\u0448\u0438\u0442\u044c \u0442\u0435\u0441\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0430\u0431\u043e\u0442\u0430\u0435\u0442 \u043f\u0440\u0438 \u0440\u0430\u0437\u043d\u044b\u0445 \u0442\u0435\u043c\u043f\u0435\u0440\u0430\u0442\u0443\u0440\u0430\u0445", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0434\u0435\u0440\u0436\u0438\u0432\u0430\u0435\u0442 \u043f\u043e\u043f\u0430\u0434\u0430\u043d\u0438\u0435 \u0432\u043e\u0434\u044b", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u0430\u0437\u044b\u0432\u0430\u0435\u0442 \u043f\u043e \u0441\u0442\u0430\u043d\u0434\u0430\u0440\u0442\u0430\u043c", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0432\u0435\u0440\u0448\u0438\u0442\u044c \u0440\u0430\u0431\u043e\u0442\u0443", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u043e\u0431\u0449\u0438\u0442\u044c \u043e \u043f\u0440\u043e\u0431\u043b\u0435\u043c\u0435", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u043e\u0431\u0449\u0438\u0442\u044c \u043e \u0431\u0440\u0430\u043a\u0435", None))
        self.pushButton_15.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043e\u0439\u0442\u0438", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0430\u0440\u043a\u0438\u0440\u043e\u0432\u043a\u0430", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0435\u0441\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"\u0423\u043f\u0430\u043a\u043e\u0432\u043a\u0430", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430", None))
        self.label_9.setText("")
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"\u0410\u0434\u043c\u0438\u043d \u043f\u0430\u043d\u0435\u043b\u044c", None))
        self.serial.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.name.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.defective.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.stage.setText(QCoreApplication.translate("MainWindow", u"stage", None))
        self.sector.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi


        QMetaObject.connectSlotsByName(MainWindow)
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
    def countine(self):
        self.centralwidget.setEnabled(True)
        couintine_work()
    def away(self):
        self.centralwidget.setEnabled(False)

        pause_work()
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Отошел")
        msg_box.setText("Нажми, чтобы продолжить работать")
        msg_box.setStandardButtons(QMessageBox.Ok)

        msg_box.buttonClicked.connect(self.countine)

        msg_box.exec()
    # setupUi
    def updateName(self, name):
        
        self.label_2.setText(name)
    

    # retranslateUi

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())