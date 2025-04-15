from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Line, Ellipse, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.properties import ListProperty, DictProperty, StringProperty, NumericProperty, BooleanProperty, ObjectProperty
import math

class BarChart(BoxLayout):
    """Столбчатая диаграмма для отображения данных в интерфейсе"""
    title = StringProperty("")
    data = DictProperty({})
    colors = ListProperty([
        '#3498DB',  # Синий
        '#E74C3C',  # Красный
        '#2ECC71',  # Зеленый
        '#F39C12',  # Оранжевый
        '#9B59B6',  # Фиолетовый
        '#1ABC9C',  # Бирюзовый
        '#E67E22',  # Морковный
        '#34495E',  # Мокрый асфальт
    ])
    show_values = BooleanProperty(True)  # Показывать ли значения над столбцами
    digits_font_name = StringProperty("RobotoMono-Regular.ttf")  # Используем Regular вместо Bold, т.к. Bold отсутствует
    
    def __init__(self, **kwargs):
        super(BarChart, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(5)
        self.bind(size=self.update_chart)
        self.bind(data=self.update_chart)
        
        # Устанавливаем белый фон
        with self.canvas.before:
            Color(*get_color_from_hex('#FFFFFF'))
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        # Добавляем заголовок
        self.title_label = Label(
            text=self.title,
            size_hint=(1, 0.1),
            color=(0.2, 0.2, 0.2, 1),
            font_size=dp(16),
            bold=True
        )
        self.add_widget(self.title_label)
    
    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
    
    def update_chart(self, *args):
        self.clear_widgets()
        self.canvas.after.clear()
        
        # Добавляем заголовок заново после clear_widgets
        self.add_widget(self.title_label)
        
        chart = BarChartWidget(
            data=self.data,
            colors=self.colors,
            show_values=self.show_values,
            digits_font_name=self.digits_font_name,
            size_hint=(1, 0.9)
        )
        self.add_widget(chart)

class BarChartWidget(Widget):
    data = DictProperty({})
    colors = ListProperty([])
    show_values = BooleanProperty(True)
    digits_font_name = StringProperty("RobotoMono-Regular.ttf")  # Используем Regular вместо Bold
    
    def __init__(self, **kwargs):
        super(BarChartWidget, self).__init__(**kwargs)
        self.bind(size=self.draw_chart)
        self.bind(pos=self.draw_chart)
        self.bind(data=self.draw_chart)
    
    def draw_chart(self, *args):
        self.canvas.after.clear()
        
        if not self.data:
            return
        
        # Параметры диаграммы
        padding = dp(55)  # Увеличен для большего пространства по бокам
        bottom_padding = dp(90)  # Увеличен для большего пространства внизу
        bar_padding = dp(15)  # Пространство между столбцами
        
        # Вычисляем максимальное значение
        max_value = max(self.data.values())
        if max_value == 0:
            return
        
        # Размеры области диаграммы
        chart_width = self.width - 2 * padding
        chart_height = self.height - padding - bottom_padding
        
        # Вычисляем ширину столбца
        num_bars = len(self.data)
        if num_bars == 0:
            return
            
        bar_width = (chart_width - (num_bars - 1) * bar_padding) / num_bars
        
        # Адаптивный размер шрифта (значительно увеличен)
        min_size = min(self.width, self.height)
        base_font_size = min_size * 0.035  # Уменьшаем с 0.06 до 0.035
        font_size = max(dp(12), min(dp(16), base_font_size))  # Уменьшаем с dp(16-24) до dp(12-16)
        
        # Начальная позиция x для первого столбца
        x_pos = self.x + padding
        
        # Определяем коэффициент масштабирования для столбцов
        scale_factor = chart_height / max_value
        
        # Рисуем сетку и оси
        with self.canvas.after:
            # Рисуем оси
            Color(0.2, 0.2, 0.2, 0.9)  # Более темный цвет для осей
            # Ось X
            Line(
                points=[
                    self.x + padding, self.y + bottom_padding,
                    self.x + padding + chart_width, self.y + bottom_padding
                ],
                width=dp(2.5)  # Ещё толще линии
            )
            # Ось Y
            Line(
                points=[
                    self.x + padding, self.y + bottom_padding,
                    self.x + padding, self.y + bottom_padding + chart_height
                ],
                width=dp(2.5)  # Ещё толще линии
            )
            
            # Рисуем горизонтальные линии сетки (5 линий)
            for i in range(1, 6):
                y = self.y + bottom_padding + (chart_height * i / 5)
                # Линия сетки
                Color(0.7, 0.7, 0.7, 0.5)  # Светло-серый цвет
                Line(
                    points=[
                        self.x + padding, y,
                        self.x + padding + chart_width, y
                    ],
                    width=dp(1.5)  # Толще линии сетки
                )
                
                # Метка значения на оси Y
                value = max_value * i / 5
                value_text = self._format_value(value)
                
                # Метка с текстом без фона
                grid_label = Label(
                    text=value_text,
                    pos=(self.x + padding - dp(40), y - dp(10)),
                    size=(dp(35), dp(20)),
                    color=(0.1, 0.1, 0.1, 1),  # Темный текст для контраста с белым фоном
                    font_size=font_size,
                    font_name=self.digits_font_name,
                    halign='right',
                    valign='middle',
                    bold=True,  # Жирный текст для лучшей читаемости
                    outline_width=1  # Тонкая обводка для лучшей читаемости
                )
        
        # Рисуем столбцы
        for idx, (label, value) in enumerate(self.data.items()):
            # Высота столбца
            bar_height = value * scale_factor
            
            # Координаты столбца
            bar_x = x_pos
            bar_y = self.y + bottom_padding
            
            # Выбираем цвет из палитры
            color = self.colors[idx % len(self.colors)]
            
            with self.canvas.after:
                # Рисуем тень для столбца
                Color(0.1, 0.1, 0.1, 0.4)  # Более заметная тень
                RoundedRectangle(
                    pos=(bar_x + dp(5), bar_y - dp(5)),
                    size=(bar_width, bar_height),
                    radius=[dp(4)]
                )
                
                # Рисуем основной столбец с градиентом
                main_color = get_color_from_hex(color)
                # Цвет для верхней части столбца (немного светлее)
                top_color = [min(c * 1.3, 1.0) for c in main_color[:3]] + [main_color[3]]
                
                # Основа столбца
                Color(*main_color)
                RoundedRectangle(
                    pos=(bar_x, bar_y),
                    size=(bar_width, bar_height),
                    radius=[dp(4)]
                )
                
                # Верхняя часть столбца (градиент)
                Color(*top_color)
                RoundedRectangle(
                    pos=(bar_x, bar_y + bar_height * 0.7),
                    size=(bar_width, bar_height * 0.3),
                    radius=[dp(4), dp(4), 0, 0]
                )
                
                # Добавляем эффект "стекла" - блик
                Color(1, 1, 1, 0.5)  # Более яркий блик
                RoundedRectangle(
                    pos=(bar_x + bar_width * 0.2, bar_y + bar_height * 0.7),
                    size=(bar_width * 0.2, bar_height * 0.3),  # Шире
                    radius=[0]
                )
                
                # Обводка столбца
                Color(0.1, 0.1, 0.1, 0.8)  # Темнее обводка для контраста
                Line(
                    rectangle=(bar_x, bar_y, bar_width, bar_height),
                    width=dp(2)  # Толще обводка
                )
                
                # Рисуем название столбца с фоном и тенью
                # Тень для фона метки
                Color(0, 0, 0, 0.3)
                RoundedRectangle(
                    pos=(bar_x - bar_width * 0.15, bar_y - dp(40)),
                    size=(bar_width * 1.3, dp(32)),
                    radius=[dp(8)]
                )
                
                # Фон для метки названия столбца
                Color(0, 0, 0, 0.8)  # Темнее фон для контраста
                RoundedRectangle(
                    pos=(bar_x - bar_width * 0.1, bar_y - dp(37)),
                    size=(bar_width * 1.2, dp(28)),
                    radius=[dp(7)]
                )
                
                # Метка с названием столбца
                label_x = bar_x + bar_width / 2
                
                # Создаем метку
                label_widget = Label(
                    text=label,
                    pos=(bar_x - bar_width * 0.1, bar_y - dp(37)),
                    size=(bar_width * 1.2, dp(28)),
                    color=(1, 1, 1, 1),  # Белый текст
                    font_size=font_size * 0.75,
                    halign='center',
                    valign='middle',
                    bold=True,
                    outline_width=dp(1),  # Добавляем обводку
                    outline_color=(0, 0, 0, 1),  # Черная обводка
                    shorten=True,  # Сокращать текст при необходимости
                    shorten_from='right'  # Сокращать справа
                )
                label_widget.texture_update()
                
                # Если нужно показывать значения над столбцами
                if self.show_values and bar_height > 0:
                    formatted_value = self._format_value(value)
                    value_x = bar_x + bar_width / 2
                    value_y = bar_y + bar_height + dp(5)
                    
                    # Внутренний фон
                    Color(0, 0, 0, 0.5)  # Уменьшаем непрозрачность с 0.85 до 0.5
                    RoundedRectangle(
                        pos=(value_x - dp(20), value_y - dp(7)),
                        size=(dp(40), dp(24)),
                        radius=[dp(3)]
                    )
                    
                    # Создаем метку с значением без фона
                    value_label = Label(
                        text=formatted_value,
                        pos=(value_x - dp(20), value_y - dp(7)),
                        size=(dp(40), dp(24)),
                        color=main_color,  # Используем цвет столбца для контраста
                        font_size=font_size,
                        font_name=self.digits_font_name,
                        halign='center',
                        valign='middle',
                        bold=True,  # Жирный текст для лучшей читаемости
                        outline_width=1,  # Добавляем тонкую обводку
                        outline_color=(1, 1, 1, 1)  # Белая обводка для контраста
                    )
            
            # Перемещаем x для следующего столбца
            x_pos += bar_width + bar_padding
    
    def _format_value(self, value):
        """Форматирует значение для отображения"""
        if value >= 1000000:
            return f"{value/1000000:.1f}M"
        elif value >= 1000:
            return f"{value/1000:.1f}K"
        else:
            return str(int(value))

# Тестовый код
if __name__ == '__main__':
    from kivy.app import App
    
    class TestApp(App):
        def build(self):
            layout = BoxLayout(orientation='vertical', padding=dp(10))
            
            # Тестовые данные для датчиков давления
            test_data = {
                'МЕТРАН 150': 60,
                'МЕТРАН 75': 110,
                'МЕТРАН 55': 150,
                'Датчик давления': 230
            }
            
            chart = BarChart(
                title="Столбчатая диаграмма",
                data=test_data,
                size_hint=(1, 0.9)
            )
            layout.add_widget(chart)
            
            return layout
    
    TestApp().run()
