from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QTableView, QTreeWidget,
    QTreeWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QLineEdit, QTextEdit)
from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
import sys

from database import database
class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Метран ")
        self.setFixedSize(800, 600)

        # Основной виджет
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Добавление графиков
        layout.addWidget(self.create_performance_chart())
        layout.addWidget(self.create_sensor_type_chart())

    def create_performance_chart(self):
        # Общая производительность (в процентах)
        performance_chart = QChart()
        performance_chart.setTitle("Общая производительность")

        METRAN_150 = ''
        METRAN_75 = ''
        METRAN_50 = ''

        x = {"type": "getstats", "name": "МЕТРАН 150"}
        x2 = {"type": "getstats", "name": "МЕТРАН 75"}
        x3 = {"type": "getstats", "name": "МЕТРАН 55"}


        metran150 = database(x)
        metran75 = database(x2)    
        metran50 = database(x3)


        
        if metran150["total"] > 0:
            METRAN_150 = (metran150["non_defective"] / metran150["total"]) * 100
        else:
            METRAN_150 = 0

        
        if metran75["total"] > 0:
            METRAN_75 = (metran75["non_defective"] / metran75["total"]) * 100
        else:
            METRAN_75 = 0

        if metran50["total"] > 0:
            METRAN_50 = (metran50["non_defective"] / metran50["total"]) * 100
        else:
            METRAN_50 = 0




        bar_set = QBarSet("Процент нормальных деталей")
        bar_set.append([METRAN_150, METRAN_75, METRAN_50])  # Примерные данные

        series = QBarSeries()
        series.append(bar_set)

        performance_chart.addSeries(series)

        categories = ["Метран 150", "Метран 75", "Метран 55"]
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        performance_chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, 100)
        performance_chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        chart_view = QChartView(performance_chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        return chart_view

    def create_sensor_type_chart(self):
        # Производительность по типам датчиков
        sensor_chart = QChart()
        sensor_chart.setTitle("Производительность по типам датчиков")

        bar_set1 = QBarSet("Датчики давления")
        bar_set2 = QBarSet("Датчики температуры")
        bar_set1.append([30, 60, 90])  # Примерные данные
        bar_set2.append([20, 50, 80])

        series = QBarSeries()
        series.append(bar_set1)
        series.append(bar_set2)

        sensor_chart.addSeries(series)

        categories = ["Январь", "Февраль", "Март"]
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        sensor_chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, 100)
        sensor_chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        chart_view = QChartView(sensor_chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        return chart_view

 
def main():
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()