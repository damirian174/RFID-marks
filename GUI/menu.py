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
    QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem)
from logger import log_event, log_error


class AdaptiveMainWindow(QMainWindow):
    """
    Расширенное главное окно с поддержкой адаптивных элементов
    и шрифтов, которые изменяются в зависимости от размера окна.
    """
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.adjustFontSizes()  # Начальное применение размеров шрифтов
        self.setMinimumSize(800, 600)  # Устанавливаем минимальный размер окна
        
    def resizeEvent(self, event):
        """Обрабатываем изменение размера окна"""
        super().resizeEvent(event)
        self.adjustFontSizes()
        
    def adjustFontSizes(self):
        """Устанавливаем размеры шрифтов в зависимости от размера окна"""
        window_width = self.width()
        window_height = self.height()
        
        # Вычисляем базовый размер шрифта (3% от меньшей стороны окна)
        base_font_size = min(window_width, window_height) * 0.03
        
        # Устанавливаем размеры для заголовка и текста описания
        title_size = max(20, int(base_font_size * 1.8))  # Не меньше 20px
        desc_size = max(14, int(base_font_size * 1.3))   # Не меньше 14px
        
        # Создаем новые шрифты с нужными размерами
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(title_size)
        
        desc_font = QFont()
        desc_font.setBold(False)
        desc_font.setPointSize(desc_size)
        
        # Применяем шрифты к элементам UI
        self.ui.label.setFont(title_font)
        self.ui.label.setStyleSheet(f"font-size: {title_size}px; font-weight: 700;")
        
        self.ui.label_2.setFont(desc_font)
        self.ui.label_2.setStyleSheet(f"font-size: {desc_size}px; font-weight: 600;")
        
        # Адаптируем размер центрального виджета
        card_width = int(min(window_width * 0.6, 800))  # Не больше 800px, но не меньше 60% от ширины
        card_height = int(min(window_height * 0.5, 500))  # Не больше 500px, но не меньше 50% от высоты
        
        # Минимальные значения для виджета
        card_width = max(card_width, 400)  # Минимум 400px ширина
        card_height = max(card_height, 300)  # Минимум 300px высота
        
        # Устанавливаем новый размер виджета
        self.ui.widget.setMinimumSize(card_width, card_height)
        self.ui.widget.setMaximumSize(800, 500)  # Максимальный размер виджета
        
        # Логирование изменений
        log_event(f"Menu: размер окна изменен: {window_width}x{window_height}, шрифты: {title_size}/{desc_size}px, виджет: {card_width}x{card_height}")


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 800)
        MainWindow.setStyleSheet(u"background-color: rgb(235, 240, 255);")
        
        # Центральный виджет
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        
        # Создаем главный вертикальный layout для центрирования содержимого
        self.main_layout = QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Добавляем spacer сверху для центрирования по вертикали
        self.main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Создаем горизонтальный layout для центрирования по горизонтали
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Создаем виджет с синим фоном и закругленными углами
        self.widget = QWidget()
        self.widget.setObjectName(u"widget")
        
        # Устанавливаем size policy, чтобы виджет расширялся вместе с окном
        self.widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.widget.setMinimumSize(600, 400)  # Минимальный размер синего виджета
        self.widget.setMaximumSize(800, 500)  # Максимальный размер синего виджета
        
        self.widget.setStyleSheet(u"background-color: #5F7ADB;\n"
                                  "border-radius: 50px;\n"
                                  "color: rgb(255, 255, 255);")
        
        # Создаем вертикальный layout для содержимого синего виджета
        self.content_layout = QVBoxLayout(self.widget)
        self.content_layout.setContentsMargins(30, 30, 30, 30)
        self.content_layout.setSpacing(20)
        
        # Добавляем spacer сверху
        self.content_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Добавляем заголовок
        self.label = QLabel(u"Отсканируйте вашу карточку!")
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(self.label)
        
        # Добавляем описание
        self.label_2 = QLabel(u"Для входа в приложение нужна ваша рабочая карточка")
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setWordWrap(True)  # Разрешаем перенос строк
        self.content_layout.addWidget(self.label_2)
        
        # Добавляем spacer снизу
        self.content_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Добавляем синий виджет в горизонтальный layout
        self.horizontal_layout.addWidget(self.widget)
        
        # Добавляем еще один spacer для центрирования
        self.horizontal_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Добавляем горизонтальный layout в главный вертикальный
        self.main_layout.addLayout(self.horizontal_layout)
        
        # Добавляем spacer снизу для центрирования по вертикали
        self.main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Устанавливаем центральный виджет
        MainWindow.setCentralWidget(self.centralwidget)
        
        # Подключаем слоты и сигналы
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"АО Метран - Вход", None))

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
    # Используем наш адаптивный класс вместо обычного QMainWindow
    window = AdaptiveMainWindow()
    window.show()
    
    sys.exit(app.exec())
