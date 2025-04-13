from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle, RoundedRectangle
from functools import partial
import json
import datetime
import random

from barchart import BarChart

# Импортируем необходимые функции из других файлов приложения
from button import send_json_to_server, get_current_time

class StyledLabel(Label):
    """Стилизованная метка с улучшенным дизайном"""
    def __init__(self, **kwargs):
        super(StyledLabel, self).__init__(**kwargs)
        self.color = get_color_from_hex('#333333')
        self.font_size = dp(16)
        self.bold = kwargs.get('bold', False)
        self.halign = 'center'
        self.valign = 'middle'

class StyledButton(Button):
    """Стилизованная кнопка с улучшенным дизайном"""
    def __init__(self, **kwargs):
        bg_color = kwargs.pop('bg_color', '#3498DB') if 'bg_color' in kwargs else '#3498DB'
        super(StyledButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = get_color_from_hex(bg_color)
        self.color = get_color_from_hex('#FFFFFF')
        self.bold = True
        self.font_size = dp(16)

class CardBox(BoxLayout):
    """Бокс в стиле карточки с тенью"""
    def __init__(self, **kwargs):
        super(CardBox, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(15)
        self.spacing = dp(10)
        self.size_hint_y = None
        
        with self.canvas.before:
            # Фон карточки
            Color(*get_color_from_hex('#FFFFFF'))
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(5)])
            
            # Добавляем тень (имитация с помощью фона)
            Color(*get_color_from_hex('#F0F0F0'))
            self.shadow = RoundedRectangle(
                pos=(self.x + dp(3), self.y - dp(3)),
                size=self.size,
                radius=[dp(5)]
            )
        
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.shadow.pos = (self.x + dp(3), self.y - dp(3))
        self.shadow.size = self.size

class StatisticsScreen(Screen):
    def __init__(self, **kwargs):
        super(StatisticsScreen, self).__init__(**kwargs)
        self.name = 'statistics'
        self.current_stats = None
        
        # Устанавливаем фон экрана
        with self.canvas.before:
            Color(*get_color_from_hex('#F5F5F5'))
            self.bg = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.create_ui()
    
    def update_rect(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        
    def create_ui(self):
        # Основной макет
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(15))
        
        # Заголовок
        header_box = BoxLayout(orientation='vertical', size_hint=(1, 0.1), padding=[0, dp(10), 0, dp(10)])
        header = StyledLabel(
            text='Статистика производства датчиков МЕТРАН', 
            font_size=dp(22),
            bold=True
        )
        header_box.add_widget(header)
        main_layout.add_widget(header_box)
        
        # Контейнер с элементами управления
        controls_card = CardBox(orientation='horizontal', size_hint=(1, None), height=dp(80), spacing=dp(15))
        
        # Выбор модели датчика
        model_layout = BoxLayout(orientation='vertical', size_hint=(0.45, 1), spacing=dp(5))
        model_label = StyledLabel(text='Модель датчика', size_hint=(1, 0.3), halign='left', font_size=dp(14))
        self.model_spinner = Spinner(
            text='Все датчики',
            values=('Все датчики', 'МЕТРАН 150', 'МЕТРАН 75', 'МЕТРАН 55'),
            size_hint=(1, 0.7),
            background_normal='',
            background_color=get_color_from_hex('#FFFFFF'),
            color=get_color_from_hex('#333333'),
            bold=True,
            font_size=dp(14)
        )
        model_layout.add_widget(model_label)
        model_layout.add_widget(self.model_spinner)
        controls_card.add_widget(model_layout)
        
        # Выбор периода анализа
        period_layout = BoxLayout(orientation='vertical', size_hint=(0.3, 1), spacing=dp(5))
        period_label = StyledLabel(text='Период', size_hint=(1, 0.3), halign='left', font_size=dp(14))
        self.period_spinner = Spinner(
            text='4 месяца',
            values=('1 месяц', '2 месяца', '3 месяца', '4 месяца', '6 месяцев', '12 месяцев'),
            size_hint=(1, 0.7),
            background_normal='',
            background_color=get_color_from_hex('#FFFFFF'),
            color=get_color_from_hex('#333333'),
            bold=True,
            font_size=dp(14)
        )
        period_layout.add_widget(period_label)
        period_layout.add_widget(self.period_spinner)
        controls_card.add_widget(period_layout)
        
        # Кнопка обновления
        refresh_layout = BoxLayout(orientation='vertical', size_hint=(0.25, 1), padding=[0, dp(12), 0, dp(0)])
        refresh_button = StyledButton(
            text='Обновить',
            size_hint=(1, 0.7),
            bg_color='#2980B9'
        )
        refresh_button.bind(on_press=self.refresh_stats)
        refresh_layout.add_widget(refresh_button)
        controls_card.add_widget(refresh_layout)
        
        main_layout.add_widget(controls_card)
        
        # Создаем прокручиваемую область для диаграмм и таблиц
        scroll_view = ScrollView(size_hint=(1, 0.8))
        self.content_layout = GridLayout(cols=1, spacing=dp(20), size_hint_y=None, padding=[0, dp(10), 0, dp(10)])
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        scroll_view.add_widget(self.content_layout)
        
        main_layout.add_widget(scroll_view)
        
        # Кнопка возврата
        back_button = StyledButton(
            text='Назад',
            size_hint=(1, 0.08),
            bg_color='#E74C3C'
        )
        back_button.bind(on_press=self.go_back)
        main_layout.add_widget(back_button)
        
        self.add_widget(main_layout)
        
        # Загружаем данные при первом отображении экрана
        Clock.schedule_once(lambda dt: self.refresh_stats(None), 0.1)
    
    def refresh_stats(self, instance):
        # Получаем выбранную модель датчика
        device_name = self.model_spinner.text
        if device_name == 'Все датчики':
            device_name = None
        
        # Получаем выбранный период
        period_text = self.period_spinner.text
        months = int(period_text.split()[0])
        
        # Показываем индикатор загрузки
        self.content_layout.clear_widgets()
        loading_card = CardBox(height=dp(100))
        loading_label = StyledLabel(
            text='Загрузка данных...',
            font_size=dp(16)
        )
        loading_card.add_widget(loading_label)
        self.content_layout.add_widget(loading_card)
        
        # Отправляем запрос на сервер
        Clock.schedule_once(partial(self.fetch_stats, device_name, months), 0.1)
    
    def fetch_stats(self, device_name, months, dt):
        # Формируем запрос
        request = {
            "type": "production_stats",
            "months": months,
            "timestamp": get_current_time(),
            "version": "1.0",
            "request_id": str(random.randint(1000, 9999))
        }
        if device_name:
            request["device_name"] = device_name
        
        # Отправляем запрос
        response = send_json_to_server(request)
        
        # Очищаем содержимое
        self.content_layout.clear_widgets()
        
        if response and response.get('status') == 'ok' and 'data' in response:
            # Сохраняем полученные данные
            self.current_stats = response['data']
            
            # Отображаем данные
            self.display_stats()
        else:
            error_message = 'Ошибка при получении данных' if not response else response.get('message', 'Неизвестная ошибка')
            error_card = CardBox(height=dp(100))
            error_label = StyledLabel(
                text=f'Ошибка: {error_message}',
                color=get_color_from_hex('#E74C3C')
            )
            error_card.add_widget(error_label)
            self.content_layout.add_widget(error_card)
    
    def display_stats(self):
        if not self.current_stats:
            return
        
        # Заголовок с названием модели
        title_card = CardBox(height=dp(80))
        device_header = StyledLabel(
            text=f"Статистика для: {self.current_stats['device_name']}",
            font_size=dp(20),
            bold=True
        )
        title_card.add_widget(device_header)
        self.content_layout.add_widget(title_card)
        
        # Отображаем статистику по месяцам
        monthly_stats = self.current_stats.get('monthly_stats', [])
        
        if monthly_stats:
            # Создаем карточку для диаграммы производства
            production_card = CardBox(height=dp(500))
            
            # Заголовок секции
            prod_header = StyledLabel(
                text="Производство по месяцам",
                font_size=dp(18),
                bold=True,
                size_hint=(1, 0.1)
            )
            production_card.add_widget(prod_header)
            
            # Создаем данные для диаграммы производства
            months = []
            total_values = []
            defective_values = []
            
            for stat in monthly_stats:
                month = stat.get('month', '')
                months.append(month)
                total_values.append(stat.get('total_count', 0))
                defective_values.append(stat.get('defective_count', 0))
            
            # Преобразуем данные для диаграммы
            data = {
                'Всего произведено': total_values,
                'Брак': defective_values
            }
            
            # Создаем диаграмму производства
            production_chart = BarChart(
                size_hint=(1, 0.9),
                y_axis_label='Количество датчиков',
                x_labels=months,
                bar_spacing=0.2
            )
            production_chart.add_dataset(data)
            production_card.add_widget(production_chart)
            
            self.content_layout.add_widget(production_card)
            
            # Создаем карточку для таблицы производства
            table_card = CardBox(height=dp(50 * (len(monthly_stats) + 1) + 70))
            
            # Заголовок таблицы
            table_header = StyledLabel(
                text="Данные по месяцам",
                font_size=dp(18),
                bold=True,
                size_hint=(1, None),
                height=dp(40)
            )
            table_card.add_widget(table_header)
            
            # Добавляем таблицу с детальными данными
            monthly_table = GridLayout(cols=3, size_hint=(1, None), height=dp(50 * (len(monthly_stats) + 1)))
            
            # Заголовки столбцов таблицы
            header_bg = get_color_from_hex('#F8F9FA')
            with monthly_table.canvas.before:
                Color(*header_bg)
                self.header_bg_rect = Rectangle(pos=(0, 0), size=(0, dp(50)))
            
            month_header = StyledLabel(text='Месяц', bold=True, size_hint_y=None, height=dp(50))
            total_header = StyledLabel(text='Всего произведено', bold=True, size_hint_y=None, height=dp(50))
            defect_header = StyledLabel(text='Брак', bold=True, size_hint_y=None, height=dp(50))
            
            monthly_table.add_widget(month_header)
            monthly_table.add_widget(total_header)
            monthly_table.add_widget(defect_header)
            
            # Данные таблицы
            for i, stat in enumerate(monthly_stats):
                month = stat.get('month', '')
                total = stat.get('total_count', 0)
                defective = stat.get('defective_count', 0)
                
                # Чередуем цвет фона строк
                if i % 2 == 0:
                    row_bg = get_color_from_hex('#FFFFFF')
                else:
                    row_bg = get_color_from_hex('#F8F9FA')
                
                month_cell = BoxLayout(size_hint_y=None, height=dp(50))
                with month_cell.canvas.before:
                    Color(*row_bg)
                    Rectangle(pos=month_cell.pos, size=month_cell.size)
                month_cell.add_widget(StyledLabel(text=str(month)))
                
                total_cell = BoxLayout(size_hint_y=None, height=dp(50))
                with total_cell.canvas.before:
                    Color(*row_bg)
                    Rectangle(pos=total_cell.pos, size=total_cell.size)
                total_cell.add_widget(StyledLabel(text=str(total)))
                
                defect_cell = BoxLayout(size_hint_y=None, height=dp(50))
                with defect_cell.canvas.before:
                    Color(*row_bg)
                    Rectangle(pos=defect_cell.pos, size=defect_cell.size)
                defect_cell.add_widget(StyledLabel(text=str(defective)))
                
                monthly_table.add_widget(month_cell)
                monthly_table.add_widget(total_cell)
                monthly_table.add_widget(defect_cell)
            
            table_card.add_widget(monthly_table)
            self.content_layout.add_widget(table_card)
            
        else:
            no_data_card = CardBox(height=dp(100))
            no_data_label = StyledLabel(
                text='Нет данных о производстве за выбранный период',
                color=get_color_from_hex('#7F8C8D')
            )
            no_data_card.add_widget(no_data_label)
            self.content_layout.add_widget(no_data_card)
        
        # Отображаем статистику брака по этапам
        defects_by_stage = self.current_stats.get('defects_by_stage', [])
        
        if defects_by_stage:
            # Создаем карточку для диаграммы брака
            defect_card = CardBox(height=dp(500))
            
            # Заголовок секции
            defect_header = StyledLabel(
                text="Распределение брака по этапам",
                font_size=dp(18),
                bold=True,
                size_hint=(1, 0.1)
            )
            defect_card.add_widget(defect_header)
            
            # Создаем данные для диаграммы брака
            stages = []
            defect_counts = []
            
            for defect in defects_by_stage:
                stage = defect.get('stage', '')
                stages.append(stage)
                defect_counts.append(defect.get('defective_count', 0))
            
            # Преобразуем данные для диаграммы
            defect_data = {
                'Брак': defect_counts
            }
            
            # Создаем диаграмму брака
            defect_chart = BarChart(
                size_hint=(1, 0.9),
                y_axis_label='Количество бракованных датчиков',
                x_labels=stages,
                bar_spacing=0.2
            )
            defect_chart.add_dataset(defect_data)
            defect_card.add_widget(defect_chart)
            
            self.content_layout.add_widget(defect_card)
            
            # Создаем карточку для таблицы брака
            defect_table_card = CardBox(height=dp(50 * (len(defects_by_stage) + 1) + 70))
            
            # Заголовок таблицы
            defect_table_header = StyledLabel(
                text="Данные по браку",
                font_size=dp(18),
                bold=True,
                size_hint=(1, None),
                height=dp(40)
            )
            defect_table_card.add_widget(defect_table_header)
            
            # Добавляем таблицу с детальными данными о браке
            defect_table = GridLayout(cols=2, size_hint=(1, None), height=dp(50 * (len(defects_by_stage) + 1)))
            
            # Заголовки столбцов таблицы
            stage_header = StyledLabel(text='Этап', bold=True, size_hint_y=None, height=dp(50))
            count_header = StyledLabel(text='Количество брака', bold=True, size_hint_y=None, height=dp(50))
            
            defect_table.add_widget(stage_header)
            defect_table.add_widget(count_header)
            
            # Данные таблицы
            for i, defect in enumerate(defects_by_stage):
                stage = defect.get('stage', '')
                count = defect.get('defective_count', 0)
                
                # Чередуем цвет фона строк
                if i % 2 == 0:
                    row_bg = get_color_from_hex('#FFFFFF')
                else:
                    row_bg = get_color_from_hex('#F8F9FA')
                
                stage_cell = BoxLayout(size_hint_y=None, height=dp(50))
                with stage_cell.canvas.before:
                    Color(*row_bg)
                    Rectangle(pos=stage_cell.pos, size=stage_cell.size)
                stage_cell.add_widget(StyledLabel(text=str(stage)))
                
                count_cell = BoxLayout(size_hint_y=None, height=dp(50))
                with count_cell.canvas.before:
                    Color(*row_bg)
                    Rectangle(pos=count_cell.pos, size=count_cell.size)
                count_cell.add_widget(StyledLabel(text=str(count)))
                
                defect_table.add_widget(stage_cell)
                defect_table.add_widget(count_cell)
            
            defect_table_card.add_widget(defect_table)
            self.content_layout.add_widget(defect_table_card)
        else:
            no_defects_card = CardBox(height=dp(100))
            no_defects_label = StyledLabel(
                text='Нет данных о браке за выбранный период',
                color=get_color_from_hex('#7F8C8D')
            )
            no_defects_card.add_widget(no_defects_label)
            self.content_layout.add_widget(no_defects_card)
        
        # Добавляем информацию о дате обновления
        update_card = CardBox(height=dp(60))
        update_info = StyledLabel(
            text=f"Обновлено: {get_current_time()}",
            color=get_color_from_hex('#7F8C8D'),
            font_size=dp(14)
        )
        update_card.add_widget(update_info)
        self.content_layout.add_widget(update_card)
    
    def go_back(self, instance):
        self.manager.current = 'main' 