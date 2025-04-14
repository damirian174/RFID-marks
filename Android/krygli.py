from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line, Rectangle, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.properties import ListProperty, DictProperty, StringProperty, NumericProperty, BooleanProperty
import math

class PieChart(BoxLayout):
    """
    Круговая диаграмма для Kivy приложений
    """
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
    show_legend = BooleanProperty(True)
    show_values = BooleanProperty(True)
    show_percentages = BooleanProperty(True)
    
    def __init__(self, **kwargs):
        super(PieChart, self).__init__(**kwargs)
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
        
        chart = PieChartWidget(
            data=self.data,
            colors=self.colors,
            size_hint=(1, 0.9)
        )
        self.add_widget(chart)

class PieChartWidget(Widget):
    data = DictProperty({})
    colors = ListProperty([])
    
    def __init__(self, **kwargs):
        super(PieChartWidget, self).__init__(**kwargs)
        self.bind(size=self.draw_chart)
        self.bind(pos=self.draw_chart)
        self.bind(data=self.draw_chart)
    
    def draw_chart(self, *args):
        self.canvas.after.clear()
        
        if not self.data:
            return
        
        # Адаптивные размеры
        min_size = min(self.width, self.height)
        center_x = self.center_x
        center_y = self.center_y
        radius = min_size * 0.4  # 40% от минимального размера
        
        # Адаптивный размер шрифта
        base_font_size = min_size * 0.03
        font_size = max(dp(10), min(dp(14), base_font_size))
        
        # Вычисляем общую сумму
        total = sum(self.data.values())
        if total == 0:
            return
        
        # Рисуем сектора
        start_angle = 0
        for idx, (label, value) in enumerate(self.data.items()):
            # Вычисляем угол сектора
            angle = (value / total) * 360
            
            # Выбираем цвет
            color = self.colors[idx % len(self.colors)]
            
            # Рисуем сектор
            with self.canvas.after:
                Color(*get_color_from_hex(color))
                Line(
                    circle=(center_x, center_y, radius, start_angle, start_angle + angle),
                    width=dp(2)
                )
                
                # Рисуем внутренний сектор с отступом
                inner_radius = radius * 0.7
                Color(*get_color_from_hex(color))
                Line(
                    circle=(center_x, center_y, inner_radius, start_angle, start_angle + angle),
                    width=dp(2)
                )
                
                # Соединяем внешний и внутренний сектора
                start_rad = math.radians(start_angle)
                end_rad = math.radians(start_angle + angle)
                
                # Внешние точки
                x1 = center_x + radius * math.cos(start_rad)
                y1 = center_y + radius * math.sin(start_rad)
                x2 = center_x + radius * math.cos(end_rad)
                y2 = center_y + radius * math.sin(end_rad)
                
                # Внутренние точки
                x3 = center_x + inner_radius * math.cos(start_rad)
                y3 = center_y + inner_radius * math.sin(start_rad)
                x4 = center_x + inner_radius * math.cos(end_rad)
                y4 = center_y + inner_radius * math.sin(end_rad)
                
                # Рисуем соединительные линии
                Line(points=[x1, y1, x3, y3], width=dp(2))
                Line(points=[x2, y2, x4, y4], width=dp(2))
            
            # Вычисляем позицию для метки
            mid_angle = start_angle + angle / 2
            mid_rad = math.radians(mid_angle)
            
            # Позиция метки
            label_radius = radius * 1.2
            label_x = center_x + label_radius * math.cos(mid_rad)
            label_y = center_y + label_radius * math.sin(mid_rad)
            
            # Вычисляем процент
            percentage = (value / total) * 100
            
            # Создаем метку
            label_text = f"{label}\n{percentage:.1f}%"
            label = Label(
                text=label_text,
                pos=(label_x - dp(40), label_y - dp(20)),
                size=(dp(80), dp(40)),
                color=get_color_from_hex(color),
                font_size=font_size,
                halign='center',
                valign='middle',
                bold=True
            )
            label.texture_update()
            
            start_angle += angle
        
        # Рисуем легенду
        legend_padding = dp(10)
        legend_item_height = dp(25)
        legend_start_x = center_x - dp(100)
        legend_start_y = center_y - radius - dp(50)
        
        for idx, (label, value) in enumerate(self.data.items()):
            color = self.colors[idx % len(self.colors)]
            
            # Цветной квадрат
            with self.canvas.after:
                Color(*get_color_from_hex(color))
                Rectangle(
                    pos=(legend_start_x, legend_start_y - idx * legend_item_height),
                    size=(dp(15), dp(15))
                )
            
            # Текст легенды
            legend_label = Label(
                text=f"{label}: {value}",
                pos=(legend_start_x + dp(20), legend_start_y - idx * legend_item_height - dp(12)),
                size=(dp(180), dp(20)),
                color=(0.3, 0.3, 0.3, 1),
                font_size=font_size,
                halign='left'
            )
            legend_label.texture_update()

class ColorBox(Widget):
    """Виджет для отображения цветного квадрата в легенде"""
    color = StringProperty('#3498DB')
    
    def __init__(self, **kwargs):
        super(ColorBox, self).__init__(**kwargs)
        self.bind(pos=self.update_rect, size=self.update_rect, color=self.update_rect)
        self.update_rect()
    
    def update_rect(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(*get_color_from_hex(self.color))
            Rectangle(pos=self.pos, size=self.size)


# Код для тестового запуска приложения
if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    
    class TestApp(App):
        def build(self):
            # Создаем основной контейнер
            main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
            
            # Добавляем заголовок
            title = Label(
                text="Тестовая круговая диаграмма",
                color=get_color_from_hex('#333333'),
                font_size=dp(20),
                bold=True,
                size_hint=(1, None),
                height=dp(40)
            )
            main_layout.add_widget(title)
            
            # Создаем тестовые данные
            test_data = {
                "Сборка": 45,
                "Пайка": 30,
                "Тестирование": 15,
                "Калибровка": 10
            }
            
            # Создаем круговую диаграмму с данными
            chart = PieChart(
                title="Распределение брака по этапам производства",
                data=test_data,
                size_hint=(1, 1)
            )
            
            main_layout.add_widget(chart)
            return main_layout
    
    # Запускаем тестовое приложение
    TestApp().run()
