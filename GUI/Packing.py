from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QTableView, QWidget)

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PackingGynApK.ui'
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QTableView, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"Packing")
        MainWindow.resize(995, 800)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(0, 50, 1000, 750))
        self.widget_2.setStyleSheet(u"background-color: rgb(235, 240, 255);")
        self.widget_4 = QWidget(self.widget_2)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setGeometry(QRect(550, 0, 450, 750))
        # self.tableView = QTableView(self.widget_3)
        # self.tableView.setObjectName(u"tableView")
        # self.tableView.setGeometry(QRect(80, 50, 300, 650))
        # self.tableView.setStyleSheet(u"background-color: #2E3239;")
        self.label_name = QLabel(self.widget_4)
        self.label_name.setAlignment(Qt.AlignHCenter)
        self.label_name.setText("Текст")
        self.label_name.setObjectName(u"label_name")
        self.label_name.setGeometry(QRect(0, 100, 450, 50))
        self.label_name.setStyleSheet(u"font: 20px;\n"
"padding-left: 10px;\n"
"font-weight: 600;")
        self.label_name2 = QLabel(self.widget_4)
        self.label_name2.setAlignment(Qt.AlignHCenter)
        self.label_name2.setText("Текст")
        self.label_name2.setObjectName(u"label_name2")
        self.label_name2.setGeometry(QRect(0, 200, 450, 50))
        self.label_name2.setStyleSheet(u"font: 20px;\n"
"padding-left: 10px;\n"
"font-weight: 600;")
        self.label_name3 = QLabel(self.widget_4)
        self.label_name3.setAlignment(Qt.AlignHCenter)
        self.label_name3.setText("Текст")
        self.label_name3.setObjectName(u"label_name3")
        self.label_name3.setGeometry(QRect(0, 300, 450, 50))
        self.label_name3.setStyleSheet(u"font: 20px;\n"
"padding-left: 10px;\n"
"font-weight: 600;")
        self.label_name4 = QLabel(self.widget_4)
        self.label_name4.setAlignment(Qt.AlignHCenter)
        self.label_name4.setText("Текст")
        self.label_name4.setObjectName(u"label_name4")
        self.label_name4.setGeometry(QRect(0, 400, 450, 50))
        self.label_name4.setStyleSheet(u"font: 20px;\n"
"padding-left: 10px;\n"
"font-weight: 600;")
        self.label_name5 = QLabel(self.widget_4)
        self.label_name5.setAlignment(Qt.AlignHCenter)
        self.label_name5.setText("Текст")
        self.label_name5.setObjectName(u"label_name5")
        self.label_name5.setGeometry(QRect(0, 500, 450, 50))
        self.label_name5.setStyleSheet(u"font: 20px;\n"
"padding-left: 10px;\n"
"font-weight: 600;")
        self.label_name2.setAlignment(Qt.AlignHCenter)
        self.label_name2.setText("Текст")
        self.widget_5 = QWidget(self.widget_2)
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
        self.widget_6 = QWidget(self.widget_2)
        self.widget_6.setObjectName(u"widget_6")
        self.widget_6.setGeometry(QRect(0, 70, 550, 680))
        self.label = QLabel(self.widget_6)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(115, 30, 318, 50))
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
        self.label_3 = QLabel(self.widget_7)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(100, 60, 400, 35))
        self.label_3.setStyleSheet(u"font: 20px;\n"
"font-weight: 500;")
        self.label_4 = QLabel(self.widget_7)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(100, 160, 400, 35))
        self.label_4.setStyleSheet(u"font: 20px;")
        self.label_5 = QLabel(self.widget_7)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(100, 260, 400, 35))
        self.label_5.setStyleSheet(u"font: 20px;")
        self.pushButton_9 = QPushButton(self.widget_6)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setGeometry(QRect(25, 600, 237, 50))
        self.pushButton_9.setStyleSheet(u"background-color: #2E3239;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"font: 20px;\n"
"font-weight: 700;")
        self.pushButton_4 = QPushButton(self.widget_6)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(280, 600, 237, 50))
        self.pushButton_4.setStyleSheet(u"background-color: #2E3239;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"font: 20px;\n"
"font-weight: 700;")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 1000, 50))
        self.widget.setStyleSheet(u"color: #5F7ADB;\n"
"font: 20px;\n"
"background-color: #2E3239;\n"
"font-weight: 700;\n"
"")
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
        self.widget_8 = QWidget(self.widget)
        self.widget_8.setObjectName(u"widget_8")
        self.widget_8.setGeometry(QRect(0, 0, 110, 50))
        self.label_9 = QLabel(self.widget_8)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(0, 0, 110, 50))
        self.label_9.setPixmap(QPixmap(u"Frame 1 (1).png"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def updateName(self, name):
        
        self.label_2.setText(name)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        
        self.label.setText(QCoreApplication.translate("MainWindow", u"  \u042d\u0442\u0430\u043f\u044b \u0443\u043f\u0430\u043a\u043e\u0432\u043a\u0438", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0432\u0435\u0440\u0448\u0438\u0442\u044c \u0443\u043f\u0430\u043a\u043e\u0432\u043a\u0443", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"1. \u0417\u0430\u0432\u0435\u0440\u043d\u0443\u0442\u044c \u0432 \u043f\u0443\u043f\u044b\u0440\u0447\u0430\u0442\u0443\u044e \u043f\u043b\u0435\u043d\u043a\u0443.", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"2. \u041f\u043e\u043b\u043e\u0436\u0438\u0442\u044c \u0432 \u043a\u0430\u0440\u0442\u043e\u043d\u043d\u0443\u044e \u043a\u043e\u0440\u043e\u0431\u043a\u0443.", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"3. \u041f\u043e\u043b\u043e\u0436\u0438\u0442\u044c \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430\u0446\u0438\u044e.", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u043e\u0431\u0449\u0438\u0442\u044c \u043e \u0431\u0440\u0430\u043a\u0435", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u043e\u0431\u0449\u0438\u0442\u044c \u043e \u043f\u0440\u043e\u0431\u043b\u0435\u043c\u0435", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0430\u0440\u043a\u0438\u0440\u043e\u0432\u043a\u0430", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0435\u0441\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"\u0423\u043f\u0430\u043a\u043e\u0432\u043a\u0430", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"\u0410\u0434\u043c\u0438\u043d \u043f\u0430\u043d\u0435\u043b\u044c", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430", None))
        self.label_9.setText("")
    # retranslateUi


    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())