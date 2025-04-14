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
        '#3498DB',  # Синий
        '#E74C3C',  # Красный
        '#2ECC71',  # Зеленый
        '#F39C12',  # Оранжевый
        '#9B59B6',  # Фиолетовый
        '#1ABC9C',  # Бирюзовый
        '#E67E22',  # Морковный
        '#34495E',  # Мокрый асфальт
    ])
    
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
            size_hint=(1, 0.9)
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
    
    def draw_chart(self, *args):
        self.canvas.after.clear()
        
        if not self.data:
            return
        
        # Адаптивные размеры
        min_size = min(self.width, self.height)
        base_padding = min_size * 0.15  # 15% от минимального размера
        padding = max(dp(20), min(dp(40), base_padding))
        
        # Адаптивный размер шрифта
        base_font_size = min_size * 0.03
        font_size = max(dp(10), min(dp(14), base_font_size))
        
        # Размеры области графика
        chart_width = self.width - padding * 2
        chart_height = self.height - padding * 2
        start_x = self.x + padding
        start_y = self.y + padding
        
        # Находим максимальное значение
        max_value = max(self.data.values()) if self.data else 0
        if max_value == 0:
            return
        
        # Вычисляем шаг сетки
        grid_step = self._calculate_grid_step(max_value)
        
        # Рисуем сетку
        with self.canvas.after:
            Color(*get_color_from_hex('#EEEEEE'))
            
            # Горизонтальные линии сетки
            num_grid_lines = int(max_value / grid_step) + 1
            for i in range(num_grid_lines):
                y = start_y + (i * grid_step * chart_height / max_value)
                Line(points=[start_x, y, start_x + chart_width, y],
                     width=1, dash_length=5, dash_offset=3)
                
                # Подписи значений
                value = i * grid_step
                label = Label(
                    text=self._format_value(value),
                    pos=(start_x - dp(35), y - dp(10)),
                    size=(dp(30), dp(20)),
                    color=(0.3, 0.3, 0.3, 1),
                    font_size=font_size,
                    halign='right'
                )
                label.texture_update()
        
        # Рисуем оси
        with self.canvas.after:
            Color(*get_color_from_hex('#333333'))
            Line(points=[start_x, start_y, start_x, start_y + chart_height], width=1)
            Line(points=[start_x, start_y, start_x + chart_width, start_y], width=1)
        
        # Рисуем столбцы
        num_bars = len(self.data)
        bar_width = chart_width / (num_bars * 2)  # Ширина столбца
        bar_spacing = bar_width  # Расстояние между столбцами
        
        for idx, (label, value) in enumerate(self.data.items()):
            # Вычисляем позицию и размеры столбца
            bar_x = start_x + (idx * (bar_width + bar_spacing)) + bar_width/2
            bar_height = (value / max_value) * chart_height
            
            # Выбираем цвет
            color = self.colors[idx % len(self.colors)]
            
            # Рисуем столбец
            with self.canvas.after:
                # Основной цвет
                Color(*get_color_from_hex(color))
                Rectangle(
                    pos=(bar_x - bar_width/2, start_y),
                    size=(bar_width, bar_height)
                )
                
                # Градиент
                Color(*get_color_from_hex(color), 0.7)
                Rectangle(
                    pos=(bar_x - bar_width/2, start_y + bar_height/2),
                    size=(bar_width, bar_height/2)
                )
            
            # Подпись значения
            value_label = Label(
                text=self._format_value(value),
                pos=(bar_x - dp(20), start_y + bar_height + dp(5)),
                size=(dp(40), dp(20)),
                color=get_color_from_hex(color),
                font_size=font_size,
                bold=True,
                halign='center'
            )
            value_label.texture_update()
            
            # Подпись категории
            category_label = Label(
                text=label,
                pos=(bar_x - dp(40), start_y - dp(25)),
                size=(dp(80), dp(20)),
                color=(0.3, 0.3, 0.3, 1),
                font_size=font_size,
                halign='center'
            )
            category_label.texture_update()
    
    def _calculate_grid_step(self, max_value):
        """Вычисляет оптимальный шаг сетки"""
        if max_value <= 0:
            return 1
        
        # Находим порядок величины
        magnitude = 10 ** int(math.log10(max_value))
        step = magnitude / 2
        
        # Если шаг слишком мал, увеличиваем его
        while max_value / step > 10:
            step *= 2
        
        return step
    
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
                data=test_data,
                size_hint=(1, 0.9)
            )
            layout.add_widget(chart)
            
            return layout
    
    TestApp().run()
