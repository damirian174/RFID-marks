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
from pyzbar import pyzbar
import cv2
import numpy as np
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

def preprocess_image(image):
    """
    Улучшение качества изображения для дальнего считывания.
    """
    # Преобразуем изображение в оттенки серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Используем CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    contrast_enhanced = clahe.apply(gray)
    
    # Применяем медианный фильтр для устранения шума
    filtered = cv2.medianBlur(contrast_enhanced, 5)
    
    # Применяем адаптивную бинаризацию для улучшения контраста
    binary = cv2.adaptiveThreshold(filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 11, 2)
    
    return binary

def draw_barcode(decoded, image):
    """
    Рисуем прямоугольник вокруг штрих-кода.
    """
    image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top),
                          (decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
                          color=(0, 255, 0), thickness=3)
    return image

def decode(image):
    """
    Распознаем штрих-коды на изображении и возвращаем изображение с прямоугольниками.
    """
    preprocessed_image = preprocess_image(image)
    
    # Декодируем штрих-коды
    decoded_objects = pyzbar.decode(preprocessed_image)

    for obj in decoded_objects:
        # Отображаем информацию о штрих-ко
        
        # Рисуем прямоугольник вокруг штрих-кода на изображении
        image = draw_barcode(obj, image)
    
    return image, decoded_objects

def show_frame(cap):
    """
    Захватываем кадры с камеры, декодируем штрих-коды и отображаем результат.
    """
    while True:
        _, frame = cap.read()

        # Декодируем штрих-коды и получаем изображение с прямоугольниками
        frame, decoded_objects = decode(frame)

        # Отображаем изображение
        cv2.imshow("Frame", frame)

        # Закрытие окна при нажатии 'q'
        if cv2.waitKey(1) == ord("q"):
            break

if __name__ == "__main__":
    # Захват видео с камеры
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        log_error("Не удалось открыть камеру")
        exit()

    show_frame(cap)

    # Освобождаем камеру и закрываем все окна после выхода из программы
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
