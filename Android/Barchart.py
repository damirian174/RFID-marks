from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, StringProperty, ColorProperty
from kivy.metrics import dp
from kivy.graphics import Color, Line, Rectangle, RoundedRectangle, Ellipse
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
import random

class BarChart(BoxLayout):
    """
    Класс для отображения столбчатых диаграмм в премиум-стиле
    """
    x_labels = ListProperty([])
    y_axis_label = StringProperty("")
    bar_spacing = NumericProperty(0.2)
    background_color = ColorProperty(get_color_from_hex('#F5F5F5'))
    
    def __init__(self, **kwargs):
        super(BarChart, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(15)
        self.chart_data = {}
        self.animated = True
        
        # Современная палитра для графиков
        self.colors = [
            get_color_from_hex('#3498DB'),  # Синий
            get_color_from_hex('#E74C3C'),  # Красный
            get_color_from_hex('#2ECC71'),  # Зеленый
            get_color_from_hex('#F39C12'),  # Оранжевый
            get_color_from_hex('#9B59B6'),  # Фиолетовый
            get_color_from_hex('#1ABC9C')   # Бирюзовый
        ]
        
        # Виджет для отображения графика
        self.chart_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.85))
        
        # Область для меток Y и самого графика
        self.y_axis_area = BoxLayout(orientation='horizontal', size_hint=(1, 1))
        
        # Область только для меток оси Y
        self.y_labels_area = BoxLayout(orientation='vertical', size_hint=(0.1, 1))
        
        # Область для графика
        self.chart_widget = Widget(size_hint=(0.9, 1))
        self.chart_widget.bind(size=self._update_chart, pos=self._update_chart)
        
        # Добавляем компоненты
        self.y_axis_area.add_widget(self.y_labels_area)
        self.y_axis_area.add_widget(self.chart_widget)
        self.chart_box.add_widget(self.y_axis_area)
        
        self.add_widget(self.chart_box)
        
        # Подпись названия оси Y
        self.y_axis_title = Label(
            text=self.y_axis_label,
            color=get_color_from_hex('#333333'),
            font_size=dp(16),
            bold=True,
            size_hint=(1, 0.05),
            halign='center'
        )
        self.add_widget(self.y_axis_title)
        
        # Область для подписей оси X
        self.x_labels_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.1),
            padding=(dp(50), 0, 0, 0)
        )
        self.add_widget(self.x_labels_layout)
        
        # Привязываем изменение y_axis_label
        self.bind(y_axis_label=self._update_y_axis_title)
    
    def _update_y_axis_title(self, instance, value):
        self.y_axis_title.text = value
    
    def add_dataset(self, data_dict):
        """
        Добавляет набор данных для отображения с анимацией
        data_dict: словарь, где ключ - название серии данных, значение - список значений
        """
        self.chart_data = data_dict
        self._update_x_labels()
        
        if self.animated:
            # Запускаем анимированное обновление графика
            self._animate_chart()
        else:
            # Обычное обновление без анимации
            self._update_chart()
    
    def _animate_chart(self, *args):
        """Анимированное обновление графика"""
        # Сначала очищаем виджет
        self.chart_widget.canvas.clear()
        self.y_labels_area.clear_widgets()
        
        if not self.chart_data or not self.x_labels:
            return
        
        chart_width = self.chart_widget.width
        chart_height = self.chart_widget.height
        
        # Определяем максимальное значение для масштабирования
        max_value = 0
        for dataset_name, values in self.chart_data.items():
            if values:
                max_value = max(max_value, max(values))
        
        # Если нет данных, устанавливаем максимум как 100
        if max_value == 0:
            max_value = 100
        
        # Определяем шаг для Y-оси
        max_rounded = max(10, (max_value // 10 + 1) * 10)  # Округляем до ближайшего десятка, но не менее 10
        step = max_rounded // 5  # 5 делений
        
        # Добавляем метки Y
        for i in range(6):  # 0, 1, 2, 3, 4, 5
            label_value = i * step
            y_pos = i / 5
            
            y_label = Label(
                text=str(label_value),
                color=get_color_from_hex('#555555'),
                font_size=dp(12),
                bold=True,
                size_hint=(1, None),
                height=dp(20),
                pos_hint={'y': y_pos - 0.05}
            )
            self.y_labels_area.add_widget(y_label)
        
        # Рисуем красивый фон и сетку для графика
        with self.chart_widget.canvas:
            # Фон графика
            Color(*self.background_color)
            Rectangle(pos=(0, 0), size=(chart_width, chart_height))
            
            # Горизонтальные линии сетки
            for i in range(6):
                y_pos = i * chart_height / 5
                Color(0.8, 0.8, 0.8, 0.5)
                Line(points=[0, y_pos, chart_width, y_pos], width=1)
            
            # Вертикальные линии для категорий
            num_categories = len(self.x_labels)
            for i in range(num_categories + 1):
                x_pos = i * chart_width / num_categories
                Color(0.8, 0.8, 0.8, 0.3)
                Line(points=[x_pos, 0, x_pos, chart_height], width=1)
        
        # Рисуем столбцы с анимацией
        num_datasets = len(self.chart_data)
        if num_datasets == 0:
            return
        
        num_categories = len(self.x_labels)
        
        # Данные для анимации
        self.animation_bars = []
        
        # Добавляем столбцы
        dataset_idx = 0
        for dataset_name, values in self.chart_data.items():
            color_idx = dataset_idx % len(self.colors)
            bar_color = self.colors[color_idx]
            
            for i, value in enumerate(values[:num_categories]):
                if value < 0 or i >= num_categories:
                    continue
                
                # Параметры столбца
                bar_x = (i + self.bar_spacing / 2) * chart_width / num_categories
                bar_width = chart_width / num_categories * (1 - self.bar_spacing) / num_datasets
                
                # Если несколько наборов данных, смещаем
                if num_datasets > 1:
                    bar_x += dataset_idx * bar_width
                
                # Окончательная высота столбца
                target_height = chart_height * min(1.0, value / max_rounded)
                
                # Начальная высота для анимации 
                initial_height = 0
                
                # Создаем столбец
                with self.chart_widget.canvas:
                    color = Color(*bar_color)
                    rect = RoundedRectangle(
                        pos=(bar_x, 0),
                        size=(bar_width, initial_height),
                        radius=[dp(3), dp(3), 0, 0]
                    )
                    
                    # Сохраняем для анимации
                    self.animation_bars.append({
                        'rect': rect,
                        'target_height': target_height,
                        'value': value,
                        'bar_x': bar_x,
                        'bar_width': bar_width,
                        'color': color
                    })
            
            dataset_idx += 1
        
        # Добавляем легенду
        self._add_legend(chart_width, chart_height)
        
        # Запускаем анимацию для каждого столбца
        for i, bar_data in enumerate(self.animation_bars):
            anim = Animation(size=(bar_data['bar_width'], bar_data['target_height']), duration=0.5, t='out_back')
            anim.start(bar_data['rect'])
            
            # Добавляем подпись значения, когда анимация закончится
            if bar_data['value'] > 0:
                # Немного задерживаем создание метки, чтобы она появилась после анимации
                Clock.schedule_once(
                    lambda dt, x=bar_data['bar_x'], w=bar_data['bar_width'], h=bar_data['target_height'], v=bar_data['value']:
                    self._add_value_label(x, w, h, v), 
                    0.5
                )
    
    def _add_value_label(self, x, width, height, value):
        """Добавляет подпись значения над столбцом"""
        label = Label(
            text=str(value),
            color=get_color_from_hex('#333333'),
            font_size=dp(12),
            bold=True,
            size=(dp(40), dp(20)),
            center_x=x + width/2,
            center_y=height + dp(10)
        )
        self.chart_widget.add_widget(label)
    
    def _add_legend(self, chart_width, chart_height):
        """Добавляет красивую легенду в верхней части графика"""
        # Создаем виджет для легенды
        legend_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            size=(chart_width * 0.8, dp(30)),
            pos=(chart_width * 0.1, chart_height - dp(40)),
            spacing=dp(15)
        )
        
        # Добавляем элементы легенды
        for i, (name, _) in enumerate(self.chart_data.items()):
            color_idx = i % len(self.colors)
            
            # Элемент легенды
            legend_item = BoxLayout(
                orientation='horizontal',
                spacing=dp(5),
                size_hint=(None, None),
                size=(dp(100), dp(20))
            )
            
            # Цветной индикатор
            color_box = Widget(size_hint=(None, None), size=(dp(15), dp(15)))
            with color_box.canvas:
                Color(*self.colors[color_idx])
                RoundedRectangle(pos=(0, 0), size=(dp(15), dp(15)), radius=[dp(2)])
            
            # Название серии
            name_label = Label(
                text=str(name),
                color=get_color_from_hex('#333333'),
                font_size=dp(12),
                bold=True,
                halign='left',
                valign='middle',
                size_hint=(None, None),
                size=(dp(80), dp(20)),
                text_size=(dp(80), dp(20))
            )
            
            legend_item.add_widget(color_box)
            legend_item.add_widget(name_label)
            legend_layout.add_widget(legend_item)
        
        self.chart_widget.add_widget(legend_layout)
    
    def _update_chart(self, *args):
        """Обновляет график без анимации"""
        if self.animated:
            self._animate_chart()
        else:
            # Реализация без анимации (если понадобится)
            pass
    
    def _update_x_labels(self):
        """Обновляет подписи оси X"""
        self.x_labels_layout.clear_widgets()
        
        if not self.x_labels:
            return
        
        # Добавляем метки X с учетом расстояния до графика
        label_width = self.width / len(self.x_labels)
        
        for i, label_text in enumerate(self.x_labels):
            label = Label(
                text=str(label_text),
                color=get_color_from_hex('#333333'),
                font_size=dp(13),
                bold=True,
                size_hint_x=None,
                width=label_width,
                halign='center',
                text_size=(label_width, None)
            )
            self.x_labels_layout.add_widget(label) 