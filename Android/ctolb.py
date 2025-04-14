from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Line, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.properties import ListProperty, DictProperty, StringProperty, NumericProperty
import math

class BarChart(BoxLayout):
    """Столбчатая диаграмма для отображения данных о датчиках"""
    title = StringProperty("")
    data = DictProperty({})
    colors = ListProperty([
        '#4B0082',  # Индиго (темно-синий)
        '#00BFFF',  # Голубой
        '#32CD32',  # Зеленый
        '#FFA500',  # Оранжевый
    ])
    
    def __init__(self, **kwargs):
        super(BarChart, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(30)  # Увеличиваем отступы для сетки
        self.spacing = dp(10)
        self.bind(size=self.update_chart)
        self.bind(data=self.update_chart)
        
        # Белый фон
        with self.canvas.before:
            Color(*get_color_from_hex('#FFFFFF'))
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
    
    def update_chart(self, *args):
        self.clear_widgets()
        self.canvas.after.clear()
        
        chart = BarChartWidget(
            data=self.data,
            colors=self.colors,
            size_hint=(1, 1)
        )
        self.add_widget(chart)

class BarChartWidget(Widget):
    data = DictProperty({})
    colors = ListProperty([])
    
    def __init__(self, **kwargs):
        super(BarChartWidget, self).__init__(**kwargs)
        self.bind(size=self.draw_chart)
        self.bind(pos=self.draw_chart)
        self.bind(data=self.draw_chart)
        
        # Минимальная высота для подписей
        self.min_label_height = dp(60)
    
    def draw_chart(self, *args):
        self.canvas.after.clear()
        
        if not self.data:
            return
            
        # Адаптивные размеры в зависимости от размера виджета
        min_size = min(self.width, self.height)
        base_padding = min_size * 0.1  # 10% от минимального размера
        padding = max(dp(20), min(dp(40), base_padding))  # Ограничиваем минимальный и максимальный отступ
        
        # Адаптивный размер шрифта
        base_font_size = min_size * 0.03  # 3% от минимального размера
        font_size = max(dp(8), min(dp(12), base_font_size))  # Ограничиваем минимальный и максимальный размер шрифта
        
        # Резервируем место для подписей внизу
        bottom_label_height = max(self.min_label_height, self.height * 0.15)  # Минимум 60dp или 15% высоты
        
        # Размеры области графика с учетом места для подписей
        chart_width = self.width - padding * 2
        chart_height = self.height - padding * 2 - bottom_label_height
        start_x = self.x + padding
        start_y = self.y + padding + bottom_label_height  # Поднимаем график выше для места подписей
        
        # Находим максимальное значение для масштабирования
        max_value = max(self.data.values())
        
        # Определяем оптимальный шаг сетки
        target_lines = 8
        magnitude = 10 ** math.floor(math.log10(max_value))
        grid_step_options = [magnitude/2, magnitude/4, magnitude/5, magnitude]
        
        best_step = grid_step_options[0]
        best_diff = float('inf')
        for step in grid_step_options:
            num_lines = math.ceil(max_value / step)
            if 5 <= num_lines <= 10:
                diff = abs(num_lines - target_lines)
                if diff < best_diff:
                    best_diff = diff
                    best_step = step
        
        grid_step = best_step
        max_grid_value = math.ceil(max_value / grid_step) * grid_step
        
        with self.canvas.after:
            # Рисуем сетку
            Color(*get_color_from_hex('#DDDDDD'))
            num_lines = int(max_grid_value / grid_step)
            
            # Рисуем горизонтальные линии и подписи значений
            for i in range(num_lines + 1):
                y = start_y + (i * chart_height / num_lines)
                # Горизонтальные линии сетки
                Line(points=[start_x, y, start_x + chart_width, y], width=1, dash_length=5, dash_offset=3)
                
                # Подписи значений на оси Y
                value = int(i * max_grid_value / num_lines)
                # Форматируем значение для лучшей читаемости
                if value >= 1000000:
                    value_str = f"{value/1000000:.1f}M"
                elif value >= 1000:
                    value_str = f"{value/1000:.0f}K"
                else:
                    value_str = str(value)
                
                # Адаптивное позиционирование подписей оси Y
                y_label_width = len(value_str) * font_size * 0.7  # Примерная ширина текста
                label = Label(
                    text=value_str,
                    pos=(start_x - y_label_width - dp(5), y - font_size/2),
                    size=(y_label_width, font_size * 2),
                    color=(0.3, 0.3, 0.3, 1),
                    font_size=font_size
                )
                label.texture_update()
            
            # Рисуем столбцы
            num_bars = len(self.data)
            min_bar_width = dp(20)  # Минимальная ширина столбца
            available_width = chart_width - (num_bars - 1) * dp(5)  # Доступная ширина с учетом минимальных отступов
            
            if available_width / num_bars < min_bar_width:
                # Если столбцы получаются слишком узкими, уменьшаем отступы
                bar_width = min_bar_width
                bar_spacing = max(dp(2), (chart_width - num_bars * min_bar_width) / (num_bars + 1))
            else:
                # Иначе используем пропорциональные отступы
                bar_spacing = chart_width * 0.1 / num_bars
                bar_width = (chart_width - (num_bars + 1) * bar_spacing) / num_bars
            
            # Рисуем оси
            Color(*get_color_from_hex('#333333'))
            Line(points=[start_x, start_y, start_x, start_y + chart_height], width=1)
            Line(points=[start_x, start_y, start_x + chart_width + dp(10), start_y], width=1)
            
            for i, (key, value) in enumerate(self.data.items()):
                # Позиция и размеры столбца
                x = start_x + bar_spacing + i * (bar_width + bar_spacing)
                height = (value / max_grid_value) * chart_height
                y = start_y
                
                # Рисуем столбец
                Color(*get_color_from_hex(self.colors[i % len(self.colors)]))
                Rectangle(pos=(x, y), size=(bar_width, height))
                
                # Подпись значения над столбцом
                value_label = Label(
                    text=str(value),
                    pos=(x - dp(5), y + height + dp(2)),
                    size=(bar_width + dp(10), font_size * 2),
                    color=(0.2, 0.2, 0.2, 1),
                    font_size=font_size,
                    bold=True,
                    halign='center'
                )
                value_label.texture_update()
                
                # Улучшенная обработка подписей категорий
                words = key.split()
                max_chars_per_line = int(bar_width / (font_size * 0.6))  # Примерное количество символов, которое поместится в строку
                
                if len(words) > 1:
                    # Формируем строки с учетом доступной ширины
                    lines = []
                    current_line = []
                    current_length = 0
                    
                    for word in words:
                        if current_length + len(word) + 1 <= max_chars_per_line:
                            current_line.append(word)
                            current_length += len(word) + 1
                        else:
                            if current_line:
                                lines.append(' '.join(current_line))
                            current_line = [word]
                            current_length = len(word)
                    
                    if current_line:
                        lines.append(' '.join(current_line))
                    
                    text = '\n'.join(lines)
                else:
                    text = key
                
                # Создаем фон для подписи категории
                label_height = (text.count('\n') + 1) * font_size * 1.5
                label_height = max(label_height, font_size * 2)  # Минимальная высота
                
                # Рисуем светлый фон под текстом для лучшей читаемости
                Color(*get_color_from_hex('#FFFFFF'), 0.9)
                RoundedRectangle(
                    pos=(x - dp(5), y - label_height - dp(8)),
                    size=(bar_width + dp(10), label_height + dp(6)),
                    radius=[dp(3)]
                )
                
                # Рисуем подпись категории
                category_label = Label(
                    text=text,
                    pos=(x - dp(5), y - label_height - dp(5)),
                    size=(bar_width + dp(10), label_height),
                    color=(0.2, 0.2, 0.2, 1),
                    font_size=font_size,
                    halign='center',
                    valign='middle',
                    bold=True
                )
                category_label.texture_update()

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
                data=test_data,
                size_hint=(1, 0.9)
            )
            layout.add_widget(chart)
            
            return layout
    
    TestApp().run()
