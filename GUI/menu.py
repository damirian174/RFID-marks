# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'menuGGUeNu.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QSizePolicy,
    QWidget)
from logger import log_event, log_error

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 800)
        MainWindow.setStyleSheet(u"background-color: rgb(235, 240, 255);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(350, 250, 600, 400))
        self.widget.setStyleSheet(u"background-color: #5F7ADB;\n"
"border-radius: 50px;\n"
"color: rgb(255, 255, 255);")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(110, 100, 400, 50))
        self.label.setStyleSheet(u"font: 25px;\n"
"font-weight: 700;")
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(50, 220, 500, 30))
        self.label_2.setStyleSheet(u"font: 18px;\n"
"font-weight: 600;")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Отсканируйте ваш штрихкод!", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Для входа в приложения нужен ваш рабочий штрихкод", None))
    # retranslateUi

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
