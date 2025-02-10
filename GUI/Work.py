# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'WorkZiwzoN.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import time
import asyncio
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,QTimer,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QWidget)



# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'WorkfsCCjY.ui'
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
    QPushButton, QSizePolicy, QWidget, QLabel, QTableView)

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'WorkwkPuEc.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1300, 750)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
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
        self.label_9.setPixmap(QPixmap(u"\u041c\u0435\u0442\u0440\u0430\u043d.jpg"))
        self.pushButton_6 = QPushButton(self.widget)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(1070, 0, 230, 50))
        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(0, 50, 1301, 750))
        self.widget_2.setStyleSheet(u"background-color: rgb(235, 240, 255);")
        self.widget_4 = QWidget(self.widget_2)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setGeometry(QRect(0, 0, 550, 70))
        self.label_2 = QLabel(self.widget_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(50, 10, 450, 40))
        self.label_2.setStyleSheet(u"font: 35px;\n"
"padding-left: 10px;\n"
"font-weight: 600;\n"
"")
        self.widget_5 = QWidget(self.widget_2)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setGeometry(QRect(160, 70, 550, 350))
        self.widget_5.setStyleSheet(u"background-color: #5F7ADB;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 50px;")
        self.label = QLabel(self.widget_5)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(190, 100, 165, 50))
        self.label.setStyleSheet(u"font: 40px;\n"
"font-weight: 800;\n"
"text-align: center;")
        self.label_3 = QLabel(self.widget_5)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(150, 30, 260, 45))
        self.label_3.setStyleSheet(u"font: 30px;\n"
"fonr-weight: 600px;")
        self.pushButton = QPushButton(self.widget_5)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(125, 210, 300, 60))
        self.pushButton.setStyleSheet(u"font: 25px;\n"
"font-weight: 600;\n"
"background-color: #2E3239;\n"
"border-radius: 30px;")
        self.pushButton_3 = QPushButton(self.widget_2)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(100, 440, 300, 50))
        self.pushButton_3.setStyleSheet(u"background-color: #2E3239;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"font: 20px;\n"
"font-weight: 700;")
        self.pushButton_4 = QPushButton(self.widget_2)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(100, 560, 300, 50))
        self.pushButton_4.setStyleSheet(u"background-color: #2E3239;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"font: 20px;\n"
"font-weight: 700;")
        self.pushButton_9 = QPushButton(self.widget_2)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setGeometry(QRect(480, 440, 300, 50))
        self.pushButton_9.setStyleSheet(u"background-color: #2E3239;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"font: 20px;\n"
"font-weight: 700;")
        self.pushButton_10 = QPushButton(self.widget_2)
        self.pushButton_10.setObjectName(u"pushButton_10")
        self.pushButton_10.setGeometry(QRect(480, 560, 300, 50))
        self.pushButton_10.setStyleSheet(u"background-color: #2E3239;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;\n"
"font: 20px;\n"
"font-weight: 700;")
        self.widget_3 = QWidget(self.centralwidget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setGeometry(QRect(780, 50, 520, 700))
        self.widget_3.setStyleSheet(u"background-color: rgb(235, 240, 255);")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Work", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0430\u0440\u043a\u0438\u0440\u043e\u0432\u043a\u0430", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0435\u0441\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"\u0423\u043f\u0430\u043a\u043e\u0432\u043a\u0430", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430", None))
        self.label_9.setText("")
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"\u0410\u0434\u043c\u0438\u043d \u043f\u0430\u043d\u0435\u043b\u044c", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0430\u0441\u0438\u043b\u0438\u0439 \u041f\u0443\u043f\u043a\u0438\u043d", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"00:00", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0440\u0435\u043c\u044f \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0438:", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0432\u0435\u0440\u0448\u0438\u0442\u044c \u044d\u0442\u0430\u043f", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u043e\u0431\u0449\u0438\u0442\u044c \u043e \u0431\u0440\u0430\u043a\u0435", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u043e\u0431\u0449\u0438\u0442\u044c \u043e \u043f\u0440\u043e\u0431\u043b\u0435\u043c\u0435", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0432\u0435\u0440\u0448\u0438\u0442\u044c \u0440\u0430\u0431\u043e\u0442\u0443", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043e\u0439\u0442\u0438", None))
    # retranslateUi




        self.start_time = time.time()  # Время старта
        self.timer = QTimer(MainWindow)  # Передаем self для привязки к Ui_MainWindow
        self.timer.timeout.connect(self.update_time)
        #Раскомментить для автостарта
        #self.timer.start(100)
        
        self.running = True     # Состояние таймера, True для автостарта

        
        # self.tableView = QTableView(self.widget_3)
        # self.tableView.setObjectName(u"tableView")
        # self.tableView.setGeometry(QRect(80, 50, 300, 650))
        # self.tableView.setStyleSheet(u"background-color: #2E3239;")
        self.label_name = QLabel(self.widget_3)
        self.label_name.setAlignment(Qt.AlignHCenter)
        self.label_name.setText("Текст")
        self.label_name.setObjectName(u"label_name")
        self.label_name.setGeometry(QRect(50, 100, 450, 50))
        self.label_name.setStyleSheet(u"font: 20px;\n"
"padding-left: 10px;\n"
"font-weight: 600;")
        self.label_name2 = QLabel(self.widget_3)
        self.label_name2.setAlignment(Qt.AlignHCenter)
        self.label_name2.setText("Текст")
        self.label_name2.setObjectName(u"label_name2")
        self.label_name2.setGeometry(QRect(50, 225, 450, 50))
        self.label_name2.setStyleSheet(u"font: 20px;\n"
"padding-left: 10px;\n"
"font-weight: 600;")
        self.label_name3 = QLabel(self.widget_3)
        self.label_name3.setAlignment(Qt.AlignHCenter)
        self.label_name3.setText("Текст")
        self.label_name3.setObjectName(u"label_name3")
        self.label_name3.setGeometry(QRect(50, 350, 450, 50))
        self.label_name3.setStyleSheet(u"font: 20px;\n"
"padding-left: 10px;\n"
"font-weight: 600;")
        self.label_name4 = QLabel(self.widget_3)
        self.label_name4.setAlignment(Qt.AlignHCenter)
        self.label_name4.setText("Текст")
        self.label_name4.setObjectName(u"label_name4")
        self.label_name4.setGeometry(QRect(50, 475, 450, 50))
        self.label_name4.setStyleSheet(u"font: 20px;\n"
"padding-left: 10px;\n"
"font-weight: 600;")
        self.label_name5 = QLabel(self.widget_3)
        self.label_name5.setAlignment(Qt.AlignHCenter)
        self.label_name5.setText("Текст")
        self.label_name5.setObjectName(u"label_name5")
        self.label_name5.setGeometry(QRect(50, 600, 450, 50))
        self.label_name5.setStyleSheet(u"font: 20px;\n"
"padding-left: 10px;\n"
"font-weight: 600;")
        self.label_name2.setAlignment(Qt.AlignHCenter)
        self.label_name2.setText("Текст")


        QMetaObject.connectSlotsByName(MainWindow)
        self.update_time()
        
    def pause_timer(self):
        if self.running:
            self.timer.stop()  # Остановка таймера
            self.running = False
            self.elapsed_pause_time = time.time() - self.start_time  # Сохранение прошедшего времени

    def resume_timer(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_pause_time  # Возвращаем прошедшее время
            self.timer.start(100)  # Возобновляем работу таймера
            self.running = True


    # setupUi

    def update_time(self):
        
        if self.running:
            
            elapsed = time.time() - self.start_time  # Вычисляем время, прошедшее с момента старта
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            time_string = f"{hours:02}:{minutes:02}:{seconds:02}"
            print(time_string)
            self.label.setText(time_string)  # Обновляем метку времени
        else:
            self.label.setText("00:00:00")

    def start_timer(self):

        self.start_time = time.time()  # Запоминаем время старта
        self.timer.start(100)  # Запуск таймера (каждые 100 мс)
        self.running = True

        
    def stop_timer(self):
        self.timer.stop()  # Остановка таймера
        self.running = False
        

    def updateName(self, name):
        print(name)
        self.label_2.setText(name)



        
        # self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0430\u0441\u0438\u043b\u0438\u0439 \u041f\u0443\u043f\u043a\u0438\u043d", None))
        # uid = 'ef5ed3e9-0ced'
        # worker = asyncSlot(get_user_by_id(uid))
        # name = worker["name"]
        # surname = worker["surname"]
        # fi = surname + name
        
    # retranslateUi

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    app.exec()