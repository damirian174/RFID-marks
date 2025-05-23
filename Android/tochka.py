from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.properties import ListProperty, DictProperty, StringProperty, NumericProperty, ObjectProperty
import math

class LineChart(BoxLayout):
    """Точечная диаграмма с линиями для отображения динамики производства"""
    title = StringProperty("Динамика производства за последние 4 месяца")
    data = DictProperty({})  # Словарь серий данных: {"название": [(x1,y1), (x2,y2), ...]}
    colors = ListProperty([
        '#3498DB',  # Синий
        '#E74C3C',  # Красный
        '#2ECC71',  # Зеленый
        '#F39C12',  # Оранжевый
    ])
    digits_font_name = StringProperty("RobotoMono-Regular.ttf")  # Шрифт для цифр
    
    def __init__(self, **kwargs):
        super(LineChart, self).__init__(**kwargs)
        self.orientation = 'vertical'
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
        
        chart = LineChartWidget(
            data=self.data,
            colors=self.colors,
            digits_font_name=self.digits_font_name,
            size_hint=(1, 0.9)
        )
        self.add_widget(chart)

class LineChartWidget(Widget):
    data = DictProperty({})
    colors = ListProperty([])
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 
              'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    digits_font_name = StringProperty("RobotoMono-Regular.ttf")
    
    def __init__(self, **kwargs):
        super(LineChartWidget, self).__init__(**kwargs)
        self.bind(size=self.draw_chart)
        self.bind(pos=self.draw_chart)
        self.bind(data=self.draw_chart)
    
    def draw_chart(self, *args):
        self.canvas.after.clear()
        
        if not self.data:
            return
        
        # Адаптивные размеры
        min_size = min(self.width, self.height)
        base_padding = min_size * 0.15  # 15% от минимального размера
        padding = max(dp(20), min(dp(40), base_padding))
        
        # Адаптивный размер шрифта
        base_font_size = min_size * 0.02
        font_size = max(dp(6), min(dp(10), base_font_size))
        
        # Размеры области графика
        chart_width = self.width - padding * 2
        chart_height = self.height - padding * 2
        start_x = self.x + padding
        start_y = self.y + padding
        
        # Находим минимальные и максимальные значения
        all_points = []
        for series in self.data.values():
            all_points.extend(series)
        
        min_x = min(p[0] for p in all_points)
        max_x = max(p[0] for p in all_points)
        min_y = min(p[1] for p in all_points)
        max_y = max(p[1] for p in all_points)
        
        # Добавляем отступы к диапазону значений
        y_range = max_y - min_y
        max_y += y_range * 0.1
        min_y -= y_range * 0.1
        
        # Защита от деления на ноль, если x_range слишком мал
        x_range = max_x - min_x
        if x_range < 0.1:
            max_x += 0.5
            min_x -= 0.5
            x_range = 1.0
        
        # Функции преобразования координат
        def scale_x(x):
            return start_x + (x - min_x) * chart_width / (max_x - min_x)
        
        def scale_y(y):
            return start_y + (y - min_y) * chart_height / (max_y - min_y)
        
        with self.canvas.after:
            # Рисуем сетку
            Color(*get_color_from_hex('#EEEEEE'))
            
            # Вертикальные линии сетки и подписи месяцев
            num_x_lines = min(int(max_x - min_x) + 1, 12)
            if num_x_lines <= 1:
                num_x_lines = 2
            
            # Создаем список для хранения меток месяцев
            month_labels = []
            
            for i in range(num_x_lines):
                x = min_x + i * (max_x - min_x) / (num_x_lines - 1)
                scaled_x = scale_x(x)
                Line(points=[scaled_x, start_y, scaled_x, start_y + chart_height],
                     width=1, dash_length=5, dash_offset=3)
                
                # Подписи месяцев
                month_idx = (int(x) - 1) % 12
                month_text = self.months[month_idx]
                
                # Создаем метку месяца
                label = Label(
                    text=month_text,
                    pos=(scaled_x - dp(30), start_y - dp(25)),
                    size=(dp(60), dp(20)),
                    color=(0.3, 0.3, 0.3, 1),
                    font_size=font_size,
                    halign='center'
                )
                label.texture_update()
                month_labels.append((label, scaled_x))
            
            # Горизонтальные линии сетки
            num_y_lines = 8
            y_labels = []
            
            for i in range(num_y_lines):
                y = min_y + i * (max_y - min_y) / (num_y_lines - 1)
                scaled_y = scale_y(y)
                Line(points=[start_x, scaled_y, start_x + chart_width, scaled_y],
                     width=1, dash_length=5, dash_offset=3)
                
                # Подписи по Y с цифровым шрифтом
                value_text = str(int(y))
                
                # Создаем метку с контрастным текстом без фона
                label = Label(
                    text=value_text,
                    pos=(start_x - dp(25), scaled_y - dp(8)),
                    size=(dp(25), dp(16)),
                    color=(0.1, 0.1, 0.1, 1),  # Темный текст для контраста с белым фоном
                    font_size=font_size,
                    halign='right',
                    bold=True,  # Жирный текст для лучшей читаемости
                    outline_width=1,  # Тонкая обводка для улучшения читаемости
                    outline_color=(1, 1, 1, 0.8)  # Светлая полупрозрачная обводка
                )
                label.texture_update()
                y_labels.append((label, scaled_y))
            
            # Рисуем оси
            Color(*get_color_from_hex('#333333'))
            Line(points=[start_x, start_y, start_x, start_y + chart_height], width=1)
            Line(points=[start_x, start_y, start_x + chart_width, start_y], width=1)
            
            # Рисуем линии и точки для каждой серии данных
            point_radius = max(dp(3), min(dp(6), min_size * 0.01))
            
            # Создаем список для хранения меток значений
            value_labels = []
            
            for idx, (series_name, points) in enumerate(self.data.items()):
                color = self.colors[idx % len(self.colors)]
                
                # Рисуем линии
                Color(*get_color_from_hex(color))
                line_points = []
                for x, y in points:
                    line_points.extend([scale_x(x), scale_y(y)])
                Line(points=line_points, width=dp(1.5))
                
                # Рисуем точки и добавляем метки значений
                for x, y in points:
                    scaled_x = scale_x(x)
                    scaled_y = scale_y(y)
                    
                    # Белый фон точки
                    Color(1, 1, 1, 1)
                    Ellipse(pos=(scaled_x - point_radius, scaled_y - point_radius),
                           size=(point_radius * 2, point_radius * 2))
                    
                    # Цветная точка
                    Color(*get_color_from_hex(color))
                    Ellipse(pos=(scaled_x - point_radius, scaled_y - point_radius),
                           size=(point_radius * 2, point_radius * 2))
                    
                    # Подпись значения с цифровым шрифтом
                    value_text = str(int(y))
                    
                    # Значительно увеличиваем размер шрифта
                    value_font_size = font_size * 1.5
                    
                    # Создаем метку без фона и с хорошим контрастом
                    label = Label(
                        text=value_text,
                        pos=(scaled_x - dp(12), scaled_y + point_radius + dp(3)),
                        size=(dp(24), dp(16)),
                        color=get_color_from_hex(color),  # Используем цвет точки для контраста
                        font_size=value_font_size,
                        halign='center',
                        bold=True,  # Жирный текст для лучшей читаемости
                        outline_width=1,  # Тонкая обводка для улучшения читаемости
                        outline_color=(1, 1, 1, 0.8)  # Светлая полупрозрачная обводка
                    )
                    label.texture_update()
                    value_labels.append((label, scaled_x, scaled_y))
            
            # Оптимизация позиционирования меток значений
            for i in range(len(value_labels)):
                label, x, y = value_labels[i]
                
                # Проверяем пересечения с другими метками
                for j in range(i + 1, len(value_labels)):
                    other_label, other_x, other_y = value_labels[j]
                    
                    # Если метки пересекаются по вертикали
                    if abs(y - other_y) < dp(20):
                        # Сдвигаем текущую метку вверх
                        label.pos = (x - dp(15), y + dp(20))
                        # Сдвигаем другую метку вниз
                        other_label.pos = (other_x - dp(15), other_y - dp(20))
            
            # Рисуем легенду
            legend_padding = dp(10)
            legend_item_height = dp(20)
            legend_start_x = start_x + chart_width - dp(150)
            legend_start_y = start_y + chart_height + dp(10)
            
            for idx, (series_name, _) in enumerate(self.data.items()):
                color = self.colors[idx % len(self.colors)]
                
                # Цветной квадрат
                Color(*get_color_from_hex(color))
                Rectangle(
                    pos=(legend_start_x, legend_start_y - idx * legend_item_height),
                    size=(dp(15), dp(15))
                )
                
                # Текст легенды
                legend_label = Label(
                    text=series_name,
                    pos=(legend_start_x + dp(20), legend_start_y - idx * legend_item_height - dp(12)),
                    size=(dp(120), dp(20)),
                    color=(0.3, 0.3, 0.3, 1),
                    font_size=font_size,
                    halign='left'
                )
                legend_label.texture_update()

# Тестовый код
if __name__ == '__main__':
    from kivy.app import App
    
    class TestApp(App):
        def build(self):
            layout = BoxLayout(orientation='vertical', padding=dp(10))
            
            # Тестовые данные за последние 4 месяца
            test_data = {
                'Метран 150': [(1, 15), (2, 25), (3, 45), (4, 60)],
                'Метран 75': [(1, 10), (2, 30), (3, 50), (4, 80)],
                'Метран 55': [(1, 12), (2, 28), (3, 48), (4, 70)]
            }
            
            chart = LineChart(
                data=test_data,
                size_hint=(1, 0.9)
            )
            layout.add_widget(chart)
            
            return layout
    
    TestApp().run()
