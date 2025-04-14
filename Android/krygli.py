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
        '#34495E',  # Темно-синий
        '#D35400',  # Темно-оранжевый
        '#27AE60',  # Темно-зеленый
        '#7F8C8D',  # Серый
    ])
    show_legend = BooleanProperty(True)
    show_values = BooleanProperty(True)
    show_percentages = BooleanProperty(True)
    
    def __init__(self, **kwargs):
        super(PieChart, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(20)
        self.spacing = dp(15)
        self.bind(data=self.update_chart, size=self.update_chart)
        
        # Устанавливаем белый фон
        with self.canvas.before:
            Color(*get_color_from_hex('#FFFFFF'))
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
    
    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        
    def update_chart(self, *args):
        """Обновление диаграммы при изменении данных или размера"""
        self.clear_widgets()
        
        # Создаем контейнер для графика и легенды
        content = BoxLayout(orientation='horizontal', size_hint=(1, 1), spacing=dp(20))
        
        # Создаем карточку для диаграммы
        chart_card = BoxLayout(
            orientation='vertical',
            size_hint=(0.7, 1),
            padding=dp(20),
            spacing=dp(10)
        )
        
        # Добавляем заголовок, если он задан
        if self.title:
            title_label = Label(
                text=self.title,
                color=get_color_from_hex('#333333'),
                font_size=dp(18),
                bold=True,
                size_hint=(1, None),
                height=dp(30)
            )
            chart_card.add_widget(title_label)
        
        # Создаем виджет с круговой диаграммой
        pie_widget = PieWidget(
            data=self.data,
            colors=self.colors,
            show_values=self.show_values,
            show_percentages=self.show_percentages
        )
        chart_card.add_widget(pie_widget)
        content.add_widget(chart_card)
        
        # Добавляем легенду, если нужно
        if self.show_legend:
            legend_card = BoxLayout(
                orientation='vertical',
                size_hint=(0.3, 1),
                padding=dp(20),
                spacing=dp(10)
            )
            
            # Заголовок легенды
            legend_title = Label(
                text="Легенда",
                color=get_color_from_hex('#333333'),
                font_size=dp(16),
                bold=True,
                size_hint=(1, None),
                height=dp(30)
            )
            legend_card.add_widget(legend_title)
            
            # Контейнер для элементов легенды
            legend_items = BoxLayout(
                orientation='vertical',
                spacing=dp(10)
            )
            
            # Добавляем элементы легенды
            total_value = sum(self.data.values()) if self.data else 0
            
            for idx, (key, value) in enumerate(self.data.items()):
                # Выбираем цвет для сегмента
                color_idx = idx % len(self.colors)
                color = self.colors[color_idx]
                
                # Создаем строку легенды
                legend_item = BoxLayout(
                    orientation='horizontal',
                    size_hint=(1, None),
                    height=dp(30),
                    spacing=dp(10)
                )
                
                # Цветной индикатор
                color_box = ColorBox(
                    color=color,
                    size_hint=(None, None),
                    size=(dp(20), dp(20))
                )
                
                # Текст с названием и значением
                percentage = (value / total_value * 100) if total_value > 0 else 0
                label_text = f"{key}"
                if self.show_values:
                    label_text += f": {value}"
                if self.show_percentages:
                    label_text += f" ({percentage:.1f}%)"
                
                text_label = Label(
                    text=label_text,
                    color=get_color_from_hex('#333333'),
                    font_size=dp(14),
                    halign='left',
                    valign='middle',
                    size_hint=(1, 1),
                    text_size=(None, dp(30))
                )
                
                legend_item.add_widget(color_box)
                legend_item.add_widget(text_label)
                legend_items.add_widget(legend_item)
            
            legend_card.add_widget(legend_items)
            content.add_widget(legend_card)
        
        self.add_widget(content)

class PieWidget(Widget):
    """Виджет для рисования круговой диаграммы"""
    data = DictProperty({})
    colors = ListProperty([])
    show_values = BooleanProperty(True)
    show_percentages = BooleanProperty(True)
    
    def __init__(self, **kwargs):
        super(PieWidget, self).__init__(**kwargs)
        self.bind(data=self.draw_pie, size=self.draw_pie, pos=self.draw_pie)
        
        # Устанавливаем белый фон
        with self.canvas.before:
            Color(*get_color_from_hex('#FFFFFF'))
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
    
    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
    
    def draw_pie(self, *args):
        """Отрисовка круговой диаграммы"""
        self.canvas.clear()
        
        if not self.data:
            return
            
        # Адаптивные размеры в зависимости от размера виджета
        min_size = min(self.width, self.height)
        padding = min_size * 0.15  # 15% от минимального размера для отступов
        
        # Определяем центр и радиус круга
        # Учитываем отступы для подписей
        available_size = min_size - (padding * 2)
        radius = available_size * 0.35  # 35% от доступного размера
        
        # Центрируем диаграмму
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2
        
        # Адаптивный размер шрифта
        base_font_size = min_size * 0.03  # 3% от минимального размера
        font_size = max(dp(8), min(dp(14), base_font_size))  # Ограничиваем размер шрифта
        
        # Рассчитываем сумму всех значений
        total = sum(self.data.values())
        
        # Начальный угол (в радианах)
        start_angle = -math.pi / 2  # Начинаем с верхней точки
        
        with self.canvas:
            # Рисуем фоновый круг
            Color(*get_color_from_hex('#FFFFFF'))
            Ellipse(pos=(cx - radius, cy - radius), size=(radius * 2, radius * 2))
            
            # Рисуем сегменты
            for idx, (key, value) in enumerate(self.data.items()):
                if value == 0:
                    continue
                    
                # Вычисляем углы для сегмента
                angle = 2 * math.pi * value / total if total > 0 else 0
                end_angle = start_angle + angle
                
                # Выбираем цвет для сегмента
                color_idx = idx % len(self.colors)
                Color(*get_color_from_hex(self.colors[color_idx]))
                
                # Рисуем сегмент
                Ellipse(
                    pos=(cx - radius, cy - radius),
                    size=(radius * 2, radius * 2),
                    angle_start=math.degrees(start_angle),
                    angle_end=math.degrees(end_angle)
                )
                
                # Рисуем разделительные линии
                Color(*get_color_from_hex('#FFFFFF'), 0.5)
                Line(points=[cx, cy, cx + radius * math.cos(start_angle), cy + radius * math.sin(start_angle)], width=1)
                Line(points=[cx, cy, cx + radius * math.cos(end_angle), cy + radius * math.sin(end_angle)], width=1)
                
                # Вычисляем угол для метки
                label_angle = start_angle + angle / 2
                
                # Значение внутри сегмента
                if self.show_values and radius > dp(50):  # Показываем только если есть место
                    inner_label_distance = radius * 0.6
                    inner_label_x = cx + inner_label_distance * math.cos(label_angle)
                    inner_label_y = cy + inner_label_distance * math.sin(label_angle)
                    
                    value_label = Label(
                        text=str(value),
                        color=get_color_from_hex('#FFFFFF'),
                        font_size=font_size,
                        bold=True,
                        center=(inner_label_x, inner_label_y),
                        size=(dp(40), dp(20))
                    )
                    value_label.texture_update()
                
                # Процент снаружи
                if self.show_percentages:
                    percentage = value / total * 100 if total > 0 else 0
                    
                    # Адаптивное расстояние для внешней метки
                    outer_label_distance = radius * 1.3
                    outer_label_x = cx + outer_label_distance * math.cos(label_angle)
                    outer_label_y = cy + outer_label_distance * math.sin(label_angle)
                    
                    # Размер фона зависит от размера текста
                    percent_text = f"{percentage:.1f}%"
                    bg_width = max(len(percent_text) * font_size * 0.7, dp(40))
                    percent_bg_size = (bg_width, font_size * 2)
                    percent_bg_x = outer_label_x - percent_bg_size[0]/2
                    percent_bg_y = outer_label_y - percent_bg_size[1]/2
                    
                    # Фон для процента
                    Color(*get_color_from_hex(self.colors[color_idx]), 0.2)
                    RoundedRectangle(
                        pos=(percent_bg_x, percent_bg_y),
                        size=percent_bg_size,
                        radius=[dp(3)]
                    )
                    
                    # Метка процента
                    percentage_label = Label(
                        text=percent_text,
                        color=get_color_from_hex('#333333'),
                        font_size=font_size,
                        bold=True,
                        center=(outer_label_x, outer_label_y),
                        size=percent_bg_size
                    )
                    percentage_label.texture_update()
                    
                    # Соединительная линия
                    segment_edge_x = cx + radius * math.cos(label_angle)
                    segment_edge_y = cy + radius * math.sin(label_angle)
                    
                    Color(*get_color_from_hex('#AAAAAA'), 0.5)
                    Line(points=[segment_edge_x, segment_edge_y, outer_label_x, outer_label_y], 
                         width=1, dash_length=3, dash_offset=3)
                
                start_angle = end_angle

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
