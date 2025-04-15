from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line, Rectangle, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.properties import ListProperty, DictProperty, StringProperty, NumericProperty, BooleanProperty, ObjectProperty
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
    digits_font_name = StringProperty("RobotoMono-Regular.ttf")  # Используем Regular вместо Bold, т.к. Bold отсутствует
    
    def __init__(self, **kwargs):
        super(PieChart, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(20)  # Увеличиваем отступы
        self.spacing = dp(10)  # Увеличиваем расстояние между элементами
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
            color=(0.1, 0.1, 0.1, 1),  # Темнее для лучшего контраста
            font_size=dp(20),  # Увеличиваем размер шрифта
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
            show_values=self.show_values,
            show_legend=self.show_legend,
            digits_font_name=self.digits_font_name,
            size_hint=(1, 0.9)
        )
        self.add_widget(chart)

class PieChartWidget(Widget):
    data = DictProperty({})
    colors = ListProperty([])
    show_values = BooleanProperty(True)
    show_legend = BooleanProperty(True)
    digits_font_name = StringProperty("RobotoMono-Regular.ttf")  # Используем Regular вместо Bold
    
    def __init__(self, **kwargs):
        super(PieChartWidget, self).__init__(**kwargs)
        self.bind(size=self.draw_chart)
        self.bind(pos=self.draw_chart)
        self.bind(data=self.draw_chart)
    
    def draw_chart(self, *args):
        self.canvas.after.clear()
        
        if not self.data:
            return
        
        total = sum(self.data.values())
        if total == 0:
            return
        
        # Адаптивные размеры
        min_size = min(self.width, self.height)
        base_radius = min_size * 0.35  # Размер пирога
        radius = max(dp(85), min(dp(170), base_radius))  # Увеличиваем минимальный и максимальный размер
        
        # Адаптивный размер шрифта (экстремально увеличен)
        base_font_size = min_size * 0.04  # Уменьшаем с 0.07 до 0.04
        font_size = max(dp(14), min(dp(18), base_font_size))  # Уменьшаем размер шрифта
        
        # Гигантский размер шрифта для цифр внутри секторов
        value_font_size = font_size * 1.2  # Уменьшаем с 3.0 до 1.2
        
        # Центр диаграммы (адаптивно располагаем в зависимости от наличия легенды)
        if self.show_legend:
            # Если есть легенда, делаем пирог чуть меньше и сдвигаем влево
            center_x = self.x + self.width * 0.35
        else:
            # Если нет легенды, центрируем пирог
            center_x = self.x + self.width / 2
            
        center_y = self.y + self.height / 2
        
        # Рисуем сектора
        angle_start = 0
        keys = []
        angles = []
        
        with self.canvas.after:
            # Рисуем многослойную тень для эффекта глубины
            for offset in range(5, 15, 3):  # Несколько слоев тени
                alpha = 0.25 - (offset - 5) * 0.05  # Уменьшение прозрачности с удалением
                Color(0.1, 0.1, 0.1, alpha)
                Ellipse(
                    pos=(center_x - radius + dp(offset), center_y - radius - dp(offset)),
                    size=(radius * 2, radius * 2)
                )
            
            # Внешняя обводка для всей диаграммы
            Color(0, 0, 0, 0.9)
            Line(
                circle=(center_x, center_y, radius),
                width=dp(3.0)  # Еще толще линия
            )
            
            # Рисуем каждый сектор
            for idx, (label, value) in enumerate(self.data.items()):
                angle_end = angle_start + value / total * 360
                
                # Сохраняем для использования при рисовании меток
                keys.append(label)
                angles.append((angle_start, angle_end))
                
                # Основной цвет сектора
                color = self.colors[idx % len(self.colors)]
                rgb = get_color_from_hex(color)
                
                # Создаем эффект глубины для сектора (градиент)
                # Темный вариант цвета для эффекта градиента
                dark_rgb = [max(0, c * 0.7) for c in rgb[:3]] + [rgb[3]]
                
                # Рисуем сектор
                Color(*rgb)
                Ellipse(
                    pos=(center_x - radius, center_y - radius),
                    size=(radius * 2, radius * 2),
                    angle_start=angle_start,
                    angle_end=angle_end
                )
                
                # Обводка для каждого сектора
                Color(0, 0, 0, 1.0)  # Полная непрозрачность
                Line(
                    points=[
                        center_x, center_y,
                        center_x + radius * math.cos(math.radians(angle_start)),
                        center_y + radius * math.sin(math.radians(angle_start))
                    ],
                    width=dp(2.5)  # Еще толще линия
                )
                
                # Вторая обводка по внешнему краю сектора
                Color(0, 0, 0, 1.0)
                Line(
                    circle=(center_x, center_y, radius),
                    angle_start=angle_start,
                    angle_end=angle_end,
                    width=dp(2.5)
                )
                
                # Рисуем значения внутри секторов, если нужно
                if self.show_values:
                    # Вычисляем угол для размещения текста
                    # (в середине сектора, на 2/3 расстояния от центра)
                    angle_middle = (angle_start + angle_end) / 2
                    text_radius = radius * 0.67  # расстояние от центра до текста
                    text_x = center_x + text_radius * math.cos(math.radians(angle_middle))
                    text_y = center_y + text_radius * math.sin(math.radians(angle_middle))
                    
                    # Форматируем текст для отображения
                    formatted_value = self._format_value(value)
                    # Добавляем процент
                    percent = value / total * 100
                    text_with_percent = f"{formatted_value}\n({percent:.1f}%)"
                    
                    # Размеры фона для текста
                    text_bg_width = dp(50)  # Уменьшаем с 80 до 50
                    text_bg_height = dp(40)  # Уменьшаем с 60 до 40
                    
                    # Основной фон - контрастный цвет к сектору
                    # Если сектор светлый, делаем темный фон и наоборот
                    bg_luma = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
                    if bg_luma > 0.5:
                        # Для светлых секторов делаем полупрозрачный темный фон
                        Color(0.1, 0.1, 0.1, 0.5)  # Уменьшаем непрозрачность с 0.9 до 0.5
                    else:
                        # Для темных секторов делаем полупрозрачный светлый фон
                        Color(0.9, 0.9, 0.9, 0.5)  # Уменьшаем непрозрачность с 0.9 до 0.5
                    
                    # Рисуем текст без фона, только с подходящим цветом для контраста
                    if bg_luma > 0.5:
                        text_color = (0, 0, 0, 1)  # Черный текст для светлого сектора
                    else:
                        text_color = (1, 1, 1, 1)  # Белый текст для темного сектора
                    
                    value_label = Label(
                        text=text_with_percent,
                        pos=(text_x - text_bg_width/2, text_y - text_bg_height/2),
                        size=(text_bg_width, text_bg_height),
                        color=text_color,
                        font_size=value_font_size,
                        font_name=self.digits_font_name,
                        halign='center',
                        valign='middle',
                        bold=True,  # Жирный текст для лучшей читаемости
                        outline_width=1  # Тонкая обводка контрастного цвета для лучшей читаемости
                    )
                
                angle_start = angle_end
        
        # Рисуем легенду, если нужно
        if self.show_legend:
            legend_start_x = center_x + radius + dp(40)  # Увеличиваем отступ от диаграммы
            legend_start_y = center_y + radius - dp(20)
            legend_item_height = dp(40)  # Увеличиваем высоту элементов легенды
            
            with self.canvas.after:
                # Фон для легенды (полупрозрачный прямоугольник с закругленными углами)
                Color(0.95, 0.95, 0.95, 0.9)  # Почти белый, полупрозрачный
                RoundedRectangle(
                    pos=(legend_start_x - dp(20), center_y - radius - dp(20)),
                    size=(self.width * 0.45, self.height * 0.85),
                    radius=[dp(15)]
                )
                
                # Рамка для легенды
                Color(0.3, 0.3, 0.3, 0.8)
                Line(
                    rounded_rectangle=(legend_start_x - dp(20), center_y - radius - dp(20), 
                                      self.width * 0.45, self.height * 0.85, dp(15)),
                    width=dp(2.0)
                )
            
            for idx, (label, value) in enumerate(self.data.items()):
                y_pos = legend_start_y - idx * legend_item_height
                
                # Цвет метки
                color = self.colors[idx % len(self.colors)]
                
                with self.canvas.after:
                    # Цветной квадратик с тенью
                    Color(0.1, 0.1, 0.1, 0.3)  # Тень
                    Rectangle(
                        pos=(legend_start_x + dp(3), y_pos - dp(15) - dp(3)),
                        size=(dp(25), dp(25))
                    )
                    
                    # Цветной квадратик
                    Color(*get_color_from_hex(color))
                    Rectangle(
                        pos=(legend_start_x, y_pos - dp(15)),
                        size=(dp(25), dp(25))  # Увеличиваем размер квадратика
                    )
                    
                    # Обводка квадратика
                    Color(0, 0, 0, 0.9)
                    Line(
                        rectangle=(legend_start_x, y_pos - dp(15), dp(25), dp(25)),
                        width=dp(2.0)  # Толще линия
                    )
                
                # Текст легенды
                percent = value / total * 100
                formatted_value = self._format_value(value)
                legend_text = f"{label}: {formatted_value} ({percent:.1f}%)"
                
                with self.canvas.after:
                    # Фон для текста легенды
                    Color(0.2, 0.2, 0.2, 0.8)
                    RoundedRectangle(
                        pos=(legend_start_x + dp(35), y_pos - dp(20)),
                        size=(self.width * 0.35, dp(35)),  # Увеличиваем высоту
                        radius=[dp(8)]
                    )
                
                legend_label = Label(
                    text=legend_text,
                    pos=(legend_start_x + dp(35), y_pos - dp(20)),
                    size=(self.width * 0.35, dp(35)),
                    color=(1, 1, 1, 1),  # Ярко-белый цвет
                    font_size=font_size * 1.2,  # Увеличиваем размер
                    halign='center',
                    valign='middle',
                    bold=True,  # Жирный текст
                    outline_width=2,  # Добавляем обводку
                    outline_color=(0, 0, 0, 1),  # Черная обводка
                    shorten=True,  # Сокращать текст при необходимости
                    shorten_from='right'  # Сокращать справа
                )
                legend_label.texture_update()
    
    def _format_value(self, value):
        """Форматирует значение для отображения"""
        if value >= 1000000:
            return f"{value/1000000:.1f}M"
        elif value >= 1000:
            return f"{value/1000:.1f}K"
        else:
            return str(int(value))

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
                font_size=dp(24),  # Увеличиваем размер
                bold=True,
                size_hint=(1, None),
                height=dp(50)  # Увеличиваем высоту
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
