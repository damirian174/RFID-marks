from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, Line
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.core.text import LabelBase  # Для регистрации шрифтов
from krygli import PieChart
from ctolb import BarChart
from tochka import LineChart
import socket
import json
import time
import datetime
import os
import shutil
from PIL import Image as PILImage

# Функция для отправки JSON-запросов на сервер
def send_json_to_server(json_data):
    try:
        # Настройки сервера
        host = '194.48.250.96'  # Локальный сервер для тестирования
        port = 12345        # Порт сервера
        
        # Логирование отправляемого запроса
        print(f"[DEBUG] Отправка запроса: {json_data}")
        
        # Создаем сокет
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Устанавливаем таймаут в 10 секунд
            s.settimeout(10.0)
            
            try:
                # Подключаемся к серверу
                s.connect((host, port))
                
                # Преобразуем данные в JSON и отправляем
                json_string = json.dumps(json_data, ensure_ascii=False)
                s.sendall(json_string.encode('utf-8'))
                
                # Получаем ответ
                data = s.recv(4096)
                
                # Преобразуем ответ из JSON
                response = json.loads(data.decode('utf-8'))
                print(f"[DEBUG] Получен ответ: {response}")
                return response
            except socket.timeout:
                print("Ошибка: Превышено время ожидания соединения с сервером")
                return {"status": "error", "message": "Таймаут соединения с сервером"}
            except socket.error as e:
                print(f"Ошибка сокета: {e}")
                return {"status": "error", "message": f"Ошибка соединения: {e}"}
            except json.JSONDecodeError as e:
                print(f"Ошибка декодирования JSON: {e}")
                return {"status": "error", "message": "Ошибка формата данных от сервера"}
            except Exception as e:
                print(f"Неизвестная ошибка: {e}")
                return {"status": "error", "message": f"Неизвестная ошибка: {e}"}
            finally:
                try:
                    s.close()
                except:
                    pass
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        return {"status": "error", "message": f"Критическая ошибка: {e}"}

# Функция для получения текущего времени в отформатированном виде
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='horizontal')
        
        # Навигационная панель с возможностью прокрутки
        self.nav_panel = BoxLayout(
            orientation='vertical',
            size_hint_x=None,
            width=App.get_running_app().nav_panel_width,
            spacing=dp(5),
            padding=[dp(10), dp(15), dp(10), dp(15)]
        )
        
        with self.nav_panel.canvas.before:
            Color(0, 0.294, 0.553, 1)  # Синий цвет
            self.bg_rect = Rectangle(pos=self.nav_panel.pos, size=self.nav_panel.size)
        
        self.nav_panel.bind(pos=self.update_rect, size=self.update_rect)
        
        # Контентная область
        self.content_area = BoxLayout(orientation='vertical')
        with self.content_area.canvas.before:
            Color(0.95, 0.97, 1.0, 1.0)  # Светло-голубой
            self.content_rect = Rectangle(pos=self.content_area.pos, size=self.content_area.size)
        
        self.content_area.bind(pos=self.update_content_rect, size=self.update_content_rect)
        
        self.main_layout.add_widget(self.nav_panel)
        self.main_layout.add_widget(self.content_area)
        self.add_widget(self.main_layout)
        
        Window.bind(on_resize=self.on_window_resize)
        self.create_nav_buttons()
        self.create_content()
    
    def update_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
    
    def update_content_rect(self, instance, value):
        self.content_rect.pos = instance.pos
        self.content_rect.size = instance.size
    
    def on_window_resize(self, window, width, height):
        app = App.get_running_app()
        is_landscape = width > height
        is_phone = min(width, height) < dp(600)
        is_tablet = dp(600) <= min(width, height) < dp(1024)
        is_height_critical = height < dp(500)  # Определяем критически малую высоту
        
        # Адаптивная ширина панели навигации
        if is_phone:
            if is_landscape:
                self.nav_panel.width = min(dp(140), width * 0.2)
            else:
                self.nav_panel.width = min(dp(160), width * 0.4)
        elif is_tablet:
            if is_landscape:
                self.nav_panel.width = min(dp(180), width * 0.22)
            else:
                self.nav_panel.width = min(dp(200), width * 0.3)
        else:  # Десктоп
            self.nav_panel.width = min(dp(250), width * 0.25)
        
        # Обновляем размеры кнопок и отступы
        self._update_nav_elements(is_height_critical)
    
    def _update_nav_elements(self, is_height_critical=False):
        is_landscape = Window.width > Window.height
        is_phone = min(Window.width, Window.height) < dp(600)
        is_tablet = dp(600) <= min(Window.width, Window.height) < dp(1024)
        
        # Базовые размеры для разных состояний
        if is_height_critical:
            # Сильно уменьшенные размеры для критически малой высоты
            button_height = dp(30) if is_phone else dp(35)
            title_height = dp(35)
            spacing = dp(2)
            padding = dp(5)
            font_size = dp(10) if is_phone else dp(12)
            title_font_size = dp(14)
        else:
            # Нормальные размеры
            if is_phone:
                if is_landscape:
                    button_height = dp(35)
                    title_height = dp(40)
                    spacing = dp(4)
                    padding = dp(8)
                    font_size = dp(12)
                    title_font_size = dp(16)
                else:
                    button_height = dp(45)
                    title_height = dp(50)
                    spacing = dp(8)
                    padding = dp(10)
                    font_size = dp(14)
                    title_font_size = dp(18)
            elif is_tablet:
                if is_landscape:
                    button_height = dp(40)
                    title_height = dp(45)
                    spacing = dp(6)
                    padding = dp(10)
                    font_size = dp(14)
                    title_font_size = dp(18)
                else:
                    button_height = dp(50)
                    title_height = dp(55)
                    spacing = dp(8)
                    padding = dp(12)
                    font_size = dp(16)
                    title_font_size = dp(20)
            else:  # Десктоп
                button_height = dp(55)
                title_height = dp(60)
                spacing = dp(10)
                padding = dp(15)
                font_size = dp(18)
                title_font_size = dp(24)
        
        # Рассчитываем минимальную необходимую высоту для всех элементов
        total_elements = 8  # Заголовок + 6 кнопок навигации + кнопка выхода
        min_total_height = (button_height * (total_elements - 1)) + title_height + (spacing * (total_elements + 1))
        
        # Если общая высота элементов больше доступной высоты, уменьшаем размеры
        if min_total_height > Window.height:
            scale_factor = Window.height / min_total_height
            button_height = max(dp(25), int(button_height * scale_factor))
            title_height = max(dp(30), int(title_height * scale_factor))
            spacing = max(dp(2), int(spacing * scale_factor))
            font_size = max(dp(10), int(font_size * scale_factor))
            title_font_size = max(dp(12), int(title_font_size * scale_factor))
        
        # Обновляем отступы панели
        self.nav_panel.spacing = spacing
        self.nav_panel.padding = [padding, padding, padding, padding]
        
        # Обновляем размеры заголовка
        if hasattr(self, 'title_label'):
            self.title_label.height = title_height
            self.title_label.font_size = title_font_size
        
        # Обновляем размеры кнопок
        for child in self.nav_panel.children:
            if isinstance(child, Button):
                child.height = button_height
                child.font_size = font_size
    
    def create_nav_buttons(self):
        # Заголовок
        self.title_label = Label(
            text='Метран',
            bold=True,
            size_hint_y=None,
            height=dp(50),
            color=(1, 1, 1, 1)
        )
        self.nav_panel.add_widget(self.title_label)
        
        # Добавляем разделитель
        self.nav_panel.add_widget(Widget(size_hint_y=None, height=dp(5)))  # Уменьшенный разделитель
        
        # Кнопки навигации
        nav_buttons = [
            ('Маркировка', 'marking'),
            ('Сборка', 'assembly'),
            ('Тестирование', 'testing'),
            ('Упаковка', 'packing'),
            ('Общее', 'general'),
            ('Статистика', 'statistics'),
            ('Профиль', 'profile')
        ]
        
        # Создаем контейнер для кнопок с отступами
        buttons_container = BoxLayout(
            orientation='vertical',
            spacing=dp(4),  # Уменьшенный отступ между кнопками
            size_hint_y=None
        )
        buttons_container.bind(minimum_height=buttons_container.setter('height'))
        
        for text, screen_name in nav_buttons:
            btn = Button(
                text=text,
                background_normal='',
                background_color=(0.1, 0.4, 0.8, 1),
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height=dp(45),
                font_size=dp(14)
            )
            
            # Сохраняем имя экрана в свойствах кнопки для дальнейшего использования
            btn.screen_name = screen_name
            
            # Устанавливаем обработчик нажатия
            btn.bind(on_press=self.on_nav_button_press)
            
            buttons_container.add_widget(btn)
        
        # Добавляем контейнер с кнопками
        self.nav_panel.add_widget(buttons_container)
        
        # Добавляем растягивающийся виджет перед кнопкой выхода
        self.nav_panel.add_widget(Widget())
        
        # Кнопка выхода
        exit_btn = Button(
            text='Выход',
            background_normal='',
            background_color=(0.3, 0.3, 0.3, 1),
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(40)  # Базовая высота кнопки
        )
        exit_btn.bind(on_release=lambda x: App.get_running_app().stop())
        self.nav_panel.add_widget(exit_btn)
        
        # Обновляем размеры элементов
        self._update_nav_elements()
    
    def create_content(self):
        self.content_area.add_widget(Label(text='Основной контент', font_size=dp(24)))

    def on_nav_button_press(self, button):
        # Получаем имя экрана из свойств кнопки
        screen_name = button.screen_name
        
        # Если это главный экран, обрабатываем навигацию
        if hasattr(self, 'sm') and isinstance(self, MainScreen):
            self.on_nav_button_press(screen_name)
        else:
            # Если это один из подэкранов, передаем событие главному экрану
            main_screen = self.manager.parent
            if hasattr(main_screen, 'on_nav_button_press'):
                main_screen.on_nav_button_press(screen_name)

# Конкретные экраны
class MarkingScreen(BaseScreen):
    def create_content(self):
        self.content_area.clear_widgets()
        
        # Создаем основной контейнер с прокруткой
        scroll_view = ScrollView(
            size_hint=(1, 1),
            bar_width=dp(10),
            bar_color=(0.2, 0.4, 0.8, 0.8),
            bar_inactive_color=(0.2, 0.4, 0.8, 0.3),
            scroll_type=['bars', 'content']
        )
        
        # Основной контейнер для контента
        main_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(20),
            padding=dp(20)
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        # Определяем тип устройства и размеры
        is_phone = min(Window.width, Window.height) < dp(600)
        is_tablet = dp(600) <= min(Window.width, Window.height) < dp(1024)
        
        # Адаптивные размеры для разных устройств
        if is_phone:
            chart_height = dp(250)
            top_panel_height = dp(40)
            button_height = dp(40)
            font_size = dp(14)
        elif is_tablet:
            chart_height = dp(300)
            top_panel_height = dp(50)
            button_height = dp(45)
            font_size = dp(16)
        else:  # Desktop
            chart_height = dp(350)
            top_panel_height = dp(60)
            button_height = dp(50)
            font_size = dp(18)
        
        # Верхняя панель с выпадающим списком
        top_panel = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=top_panel_height,
            spacing=dp(10)
        )
        
        # Выпадающий список работников
        self.worker_dropdown = Spinner(
            text='Выберите работника',
            values=['Работник 1', 'Работник 2', 'Работник 3'],
            size_hint=(None, 1),
            width=dp(200),
            font_size=font_size
        )
        self.worker_dropdown.bind(text=self.on_worker_selected)
        
        top_panel.add_widget(self.worker_dropdown)
        top_panel.add_widget(Widget())  # Растягивающийся виджет
        
        main_layout.add_widget(top_panel)
        
        # Контейнер для графиков
        charts_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            spacing=dp(20)
        )
        charts_container.bind(minimum_height=charts_container.setter('height'))
        
        # Первая круговая диаграмма
        pie_data1 = {
            "Сборка": 45,
            "Пайка": 30,
            "Тестирование": 15,
            "Калибровка": 10
        }
        pie_chart1 = PieChart(
            title="Распределение брака по этапам производства",
            data=pie_data1,
            size_hint=(1, None),
            height=chart_height
        )
        charts_container.add_widget(pie_chart1)
        
        # Столбчатая диаграмма
        bar_data = {
            'МЕТРАН 150': 60,
            'МЕТРАН 75': 110,
            'МЕТРАН 55': 150,
            'Датчик давления': 230
        }
        bar_chart = BarChart(
            title="Статистика по датчикам",
            data=bar_data,
            size_hint=(1, None),
            height=chart_height
        )
        charts_container.add_widget(bar_chart)
        
        # Точечная диаграмма
        line_data = {
            'Метран 150': [(1, 15), (2, 25), (3, 45), (4, 60)],
            'Метран 75': [(1, 10), (2, 30), (3, 50), (4, 80)],
            'Метран 55': [(1, 12), (2, 28), (3, 48), (4, 70)]
        }
        line_chart = LineChart(
            title="Динамика производства за последние 4 месяца",
            data=line_data,
            size_hint=(1, None),
            height=chart_height
        )
        charts_container.add_widget(line_chart)
        
        main_layout.add_widget(charts_container)
        
        # Добавляем отступ перед кнопками
        main_layout.add_widget(Widget(size_hint_y=None, height=dp(20)))
        
        # Контейнер для кнопок экспорта
        export_buttons = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=button_height,
            spacing=dp(20),
            padding=[dp(20), 0, dp(20), 0]
        )
        
        # Кнопка экспорта в Excel
        excel_btn = Button(
            text='Экспорт в Excel',
            size_hint=(0.5, 1),
            background_normal='',
            background_color=(0.2, 0.6, 0.2, 1),
            font_size=font_size
        )
        
        # Кнопка отправки на почту
        email_btn = Button(
            text='Отправить на почту',
            size_hint=(0.5, 1),
            background_normal='',
            background_color=(0.2, 0.4, 0.8, 1),
            font_size=font_size
        )
        
        export_buttons.add_widget(excel_btn)
        export_buttons.add_widget(email_btn)
        
        main_layout.add_widget(export_buttons)
        
        # Добавляем отступ внизу
        main_layout.add_widget(Widget(size_hint_y=None, height=dp(20)))
        
        scroll_view.add_widget(main_layout)
        self.content_area.add_widget(scroll_view)
    
    def on_worker_selected(self, spinner, text):
        # Здесь будет логика обновления графиков при выборе работника
        pass

class AssemblyScreen(BaseScreen):
    def create_content(self):
        self.content_area.clear_widgets()
        
        # Создаем основной контейнер с прокруткой
        scroll_view = ScrollView(
            size_hint=(1, 1),
            bar_width=dp(10),
            bar_color=(0.2, 0.4, 0.8, 0.8),
            bar_inactive_color=(0.2, 0.4, 0.8, 0.3),
            scroll_type=['bars', 'content']
        )
        
        # Основной контейнер для контента
        main_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(20),
            padding=dp(20)
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        # Определяем тип устройства и размеры
        is_phone = min(Window.width, Window.height) < dp(600)
        is_tablet = dp(600) <= min(Window.width, Window.height) < dp(1024)
        
        # Адаптивные размеры для разных устройств
        if is_phone:
            chart_height = dp(250)
            top_panel_height = dp(40)
            button_height = dp(40)
            font_size = dp(14)
        elif is_tablet:
            chart_height = dp(300)
            top_panel_height = dp(50)
            button_height = dp(45)
            font_size = dp(16)
        else:  # Desktop
            chart_height = dp(350)
            top_panel_height = dp(60)
            button_height = dp(50)
            font_size = dp(18)
        
        # Верхняя панель с выпадающим списком
        top_panel = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=top_panel_height,
            spacing=dp(10)
        )
        
        # Выпадающий список работников
        self.worker_dropdown = Spinner(
            text='Выберите работника',
            values=['Работник 1', 'Работник 2', 'Работник 3'],
            size_hint=(None, 1),
            width=dp(200),
            font_size=font_size
        )
        self.worker_dropdown.bind(text=self.on_worker_selected)
        
        top_panel.add_widget(self.worker_dropdown)
        top_panel.add_widget(Widget())  # Растягивающийся виджет
        
        main_layout.add_widget(top_panel)
        
        # Контейнер для графиков
        charts_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            spacing=dp(20)
        )
        charts_container.bind(minimum_height=charts_container.setter('height'))
        
        # Круговая диаграмма
        pie_data = {
            "Успешные": 75,
            "Брак": 15,
            "На доработке": 10
        }
        pie_chart = PieChart(
            title="Статистика сборки",
            data=pie_data,
            size_hint=(1, None),
            height=chart_height
        )
        charts_container.add_widget(pie_chart)
        
        # Столбчатая диаграмма
        bar_data = {
            'МЕТРАН 150': 60,
            'МЕТРАН 75': 110,
            'МЕТРАН 55': 150,
            'Датчик давления': 230
        }
        bar_chart = BarChart(
            title="Статистика по датчикам",
            data=bar_data,
            size_hint=(1, None),
            height=chart_height
        )
        charts_container.add_widget(bar_chart)
        
        # Точечная диаграмма
        line_data = {
            'Метран 150': [(1, 15), (2, 25), (3, 45), (4, 60)],
            'Метран 75': [(1, 10), (2, 30), (3, 50), (4, 80)],
            'Метран 55': [(1, 12), (2, 28), (3, 48), (4, 70)]
        }
        line_chart = LineChart(
            title="Динамика сборки за последние 4 месяца",
            data=line_data,
            size_hint=(1, None),
            height=chart_height
        )
        charts_container.add_widget(line_chart)
        
        main_layout.add_widget(charts_container)
        
        # Добавляем отступ перед кнопками
        main_layout.add_widget(Widget(size_hint_y=None, height=dp(20)))
        
        # Контейнер для кнопок экспорта
        export_buttons = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=button_height,
            spacing=dp(20),
            padding=[dp(20), 0, dp(20), 0]
        )
        
        # Кнопка экспорта в Excel
        excel_btn = Button(
            text='Экспорт в Excel',
            size_hint=(0.5, 1),
            background_normal='',
            background_color=(0.2, 0.6, 0.2, 1),
            font_size=font_size
        )
        
        # Кнопка отправки на почту
        email_btn = Button(
            text='Отправить на почту',
            size_hint=(0.5, 1),
            background_normal='',
            background_color=(0.2, 0.4, 0.8, 1),
            font_size=font_size
        )
        
        export_buttons.add_widget(excel_btn)
        export_buttons.add_widget(email_btn)
        
        main_layout.add_widget(export_buttons)
        
        # Добавляем отступ внизу
        main_layout.add_widget(Widget(size_hint_y=None, height=dp(20)))
        
        scroll_view.add_widget(main_layout)
        self.content_area.add_widget(scroll_view)
    
    def on_worker_selected(self, spinner, text):
        # Здесь будет логика обновления графиков при выборе работника
        pass

class TestingScreen(BaseScreen):
    def create_content(self):
        self.content_area.clear_widgets()
        
        # Создаем основной контейнер с прокруткой
        scroll_view = ScrollView(
            size_hint=(1, 1),
            bar_width=dp(10),
            bar_color=(0.2, 0.4, 0.8, 0.8),
            bar_inactive_color=(0.2, 0.4, 0.8, 0.3),
            scroll_type=['bars', 'content']
        )
        
        # Основной контейнер для контента
        main_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(20),
            padding=dp(20)
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        # Определяем тип устройства и размеры
        is_phone = min(Window.width, Window.height) < dp(600)
        is_tablet = dp(600) <= min(Window.width, Window.height) < dp(1024)
        
        # Адаптивные размеры для разных устройств
        if is_phone:
            chart_height = dp(250)
            top_panel_height = dp(40)
            button_height = dp(40)
            font_size = dp(14)
        elif is_tablet:
            chart_height = dp(300)
            top_panel_height = dp(50)
            button_height = dp(45)
            font_size = dp(16)
        else:  # Desktop
            chart_height = dp(350)
            top_panel_height = dp(60)
            button_height = dp(50)
            font_size = dp(18)
        
        # Верхняя панель с выпадающим списком
        top_panel = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=top_panel_height,
            spacing=dp(10)
        )
        
        # Выпадающий список работников
        self.worker_dropdown = Spinner(
            text='Выберите работника',
            values=['Работник 1', 'Работник 2', 'Работник 3'],
            size_hint=(None, 1),
            width=dp(200),
            font_size=font_size
        )
        self.worker_dropdown.bind(text=self.on_worker_selected)
        
        top_panel.add_widget(self.worker_dropdown)
        top_panel.add_widget(Widget())  # Растягивающийся виджет
        
        main_layout.add_widget(top_panel)
        
        # Контейнер для графиков
        charts_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            spacing=dp(20)
        )
        charts_container.bind(minimum_height=charts_container.setter('height'))
        
        # Круговая диаграмма
        pie_data = {
            "Успешные": 85,
            "Брак": 10,
            "На доработке": 5
        }
        pie_chart = PieChart(
            title="Статистика тестирования",
            data=pie_data,
            size_hint=(1, None),
            height=chart_height
        )
        charts_container.add_widget(pie_chart)
        
        # Столбчатая диаграмма
        bar_data = {
            'МЕТРАН 150': 45,
            'МЕТРАН 75': 90,
            'МЕТРАН 55': 120,
            'Датчик давления': 180
        }
        bar_chart = BarChart(
            title="Статистика по датчикам",
            data=bar_data,
            size_hint=(1, None),
            height=chart_height
        )
        charts_container.add_widget(bar_chart)
        
        # Точечная диаграмма
        line_data = {
            'Метран 150': [(1, 20), (2, 35), (3, 40), (4, 45)],
            'Метран 75': [(1, 25), (2, 40), (3, 45), (4, 90)],
            'Метран 55': [(1, 30), (2, 45), (3, 50), (4, 120)]
        }
        line_chart = LineChart(
            title="Динамика тестирования за последние 4 месяца",
            data=line_data,
            size_hint=(1, None),
            height=chart_height
        )
        charts_container.add_widget(line_chart)
        
        main_layout.add_widget(charts_container)
        
        # Добавляем отступ перед кнопками
        main_layout.add_widget(Widget(size_hint_y=None, height=dp(20)))
        
        # Контейнер для кнопок экспорта
        export_buttons = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=button_height,
            spacing=dp(20),
            padding=[dp(20), 0, dp(20), 0]
        )
        
        # Кнопка экспорта в Excel
        excel_btn = Button(
            text='Экспорт в Excel',
            size_hint=(0.5, 1),
            background_normal='',
            background_color=(0.2, 0.6, 0.2, 1),
            font_size=font_size
        )
        
        # Кнопка отправки на почту
        email_btn = Button(
            text='Отправить на почту',
            size_hint=(0.5, 1),
            background_normal='',
            background_color=(0.2, 0.4, 0.8, 1),
            font_size=font_size
        )
        
        export_buttons.add_widget(excel_btn)
        export_buttons.add_widget(email_btn)
        
        main_layout.add_widget(export_buttons)
        
        # Добавляем отступ внизу
        main_layout.add_widget(Widget(size_hint_y=None, height=dp(20)))
        
        scroll_view.add_widget(main_layout)
        self.content_area.add_widget(scroll_view)
    
    def on_worker_selected(self, spinner, text):
        # Здесь будет логика обновления графиков при выборе работника
        pass

class PackingScreen(BaseScreen):
    def create_content(self):
        self.content_area.clear_widgets()
        
        # Создаем основной контейнер с прокруткой
        scroll_view = ScrollView(
            size_hint=(1, 1),
            bar_width=dp(10),
            bar_color=(0.2, 0.4, 0.8, 0.8),
            bar_inactive_color=(0.2, 0.4, 0.8, 0.3),
            scroll_type=['bars', 'content']
        )
        
        # Основной контейнер для контента
        main_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(20),
            padding=dp(20)
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        # Определяем тип устройства и размеры
        is_phone = min(Window.width, Window.height) < dp(600)
        is_tablet = dp(600) <= min(Window.width, Window.height) < dp(1024)
        
        # Адаптивные размеры для разных устройств
        if is_phone:
            chart_height = dp(250)
            top_panel_height = dp(40)
            button_height = dp(40)
            font_size = dp(14)
        elif is_tablet:
            chart_height = dp(300)
            top_panel_height = dp(50)
            button_height = dp(45)
            font_size = dp(16)
        else:  # Desktop
            chart_height = dp(350)
            top_panel_height = dp(60)
            button_height = dp(50)
            font_size = dp(18)
        
        # Верхняя панель с выпадающим списком
        top_panel = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=top_panel_height,
            spacing=dp(10)
        )
        
        # Выпадающий список работников
        self.worker_dropdown = Spinner(
            text='Выберите работника',
            values=['Работник 1', 'Работник 2', 'Работник 3'],
            size_hint=(None, 1),
            width=dp(200),
            font_size=font_size
        )
        self.worker_dropdown.bind(text=self.on_worker_selected)
        
        top_panel.add_widget(self.worker_dropdown)
        top_panel.add_widget(Widget())  # Растягивающийся виджет
        
        main_layout.add_widget(top_panel)
        
        # Контейнер для графиков
        charts_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            spacing=dp(20)
        )
        charts_container.bind(minimum_height=charts_container.setter('height'))
        
        # Круговая диаграмма
        pie_data = {
            "Успешные": 90,
            "Брак": 5,
            "На доработке": 5
        }
        pie_chart = PieChart(
            title="Статистика упаковки",
            data=pie_data,
            size_hint=(1, None),
            height=chart_height
        )
        charts_container.add_widget(pie_chart)
        
        # Столбчатая диаграмма
        bar_data = {
            'МЕТРАН 150': 40,
            'МЕТРАН 75': 80,
            'МЕТРАН 55': 100,
            'Датчик давления': 150
        }
        bar_chart = BarChart(
            title="Статистика по датчикам",
            data=bar_data,
            size_hint=(1, None),
            height=chart_height
        )
        charts_container.add_widget(bar_chart)
        
        # Точечная диаграмма
        line_data = {
            'Метран 150': [(1, 25), (2, 30), (3, 35), (4, 40)],
            'Метран 75': [(1, 30), (2, 40), (3, 50), (4, 80)],
            'Метран 55': [(1, 35), (2, 45), (3, 60), (4, 100)]
        }
        line_chart = LineChart(
            title="Динамика упаковки за последние 4 месяца",
            data=line_data,
            size_hint=(1, None),
            height=chart_height
        )
        charts_container.add_widget(line_chart)
        
        main_layout.add_widget(charts_container)
        
        # Добавляем отступ перед кнопками
        main_layout.add_widget(Widget(size_hint_y=None, height=dp(20)))
        
        # Контейнер для кнопок экспорта
        export_buttons = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=button_height,
            spacing=dp(20),
            padding=[dp(20), 0, dp(20), 0]
        )
        
        # Кнопка экспорта в Excel
        excel_btn = Button(
            text='Экспорт в Excel',
            size_hint=(0.5, 1),
            background_normal='',
            background_color=(0.2, 0.6, 0.2, 1),
            font_size=font_size
        )
        
        # Кнопка отправки на почту
        email_btn = Button(
            text='Отправить на почту',
            size_hint=(0.5, 1),
            background_normal='',
            background_color=(0.2, 0.4, 0.8, 1),
            font_size=font_size
        )
        
        export_buttons.add_widget(excel_btn)
        export_buttons.add_widget(email_btn)
        
        main_layout.add_widget(export_buttons)
        
        # Добавляем отступ внизу
        main_layout.add_widget(Widget(size_hint_y=None, height=dp(20)))
        
        scroll_view.add_widget(main_layout)
        self.content_area.add_widget(scroll_view)
    
    def on_worker_selected(self, spinner, text):
        # Здесь будет логика обновления графиков при выборе работника
        pass

class GeneralScreen(BaseScreen):
    def create_content(self):
        self.content_area.clear_widgets()
        self.content_area.add_widget(Label(text='Общий экран', font_size=dp(24)))

class ProfileScreen(BaseScreen):
    def __init__(self, **kwargs):
        # Инициализируем атрибуты до вызова super().__init__
        # Путь к папке с кэшем для хранения фотографий пользователя
        self.cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')
        # Создаем директорию, если не существует
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        
        # Путь к аватару пользователя
        self.avatar_path = os.path.join(self.cache_dir, 'user_avatar.jpg')
        # Флаг наличия изображения
        self.has_avatar = os.path.exists(self.avatar_path)
        
        # Теперь вызываем инициализацию базового класса
        super().__init__(**kwargs)
        
    def create_content(self):
        self.content_area.clear_widgets()
        
        # Создаем основной контейнер с прокруткой
        scroll_view = ScrollView(
            size_hint=(1, 1),
            bar_width=dp(10),
            bar_color=(0.2, 0.4, 0.8, 0.8),
            bar_inactive_color=(0.2, 0.4, 0.8, 0.3),
            scroll_type=['bars', 'content']
        )
        
        # Основной контейнер для контента
        main_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(20),
            padding=dp(20)
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        # Определяем тип устройства и размеры
        is_phone = min(Window.width, Window.height) < dp(600)
        is_tablet = dp(600) <= min(Window.width, Window.height) < dp(1024)
        
        # Адаптивные размеры для разных устройств
        if is_phone:
            profile_section_height = dp(150)
            stats_section_height = dp(200)
            button_height = dp(40)
            font_size = dp(14)
            title_font_size = dp(18)
            info_font_size = dp(12)
        elif is_tablet:
            profile_section_height = dp(200)
            stats_section_height = dp(250)
            button_height = dp(45)
            font_size = dp(16)
            title_font_size = dp(22)
            info_font_size = dp(14)
        else:  # Desktop
            profile_section_height = dp(250)
            stats_section_height = dp(300)
            button_height = dp(50)
            font_size = dp(18)
            title_font_size = dp(26)
            info_font_size = dp(16)
        
        # ====================== СЕКЦИЯ ПРОФИЛЯ ======================
        profile_section = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=profile_section_height,
            spacing=dp(20)
        )
        
        # Панель с аватаром (изображение или заглушка)
        avatar_panel = BoxLayout(
            orientation='vertical',
            size_hint=(None, 1),
            width=profile_section_height * 0.8,
            padding=dp(5)
        )
        
        with avatar_panel.canvas.before:
            Color(0.2, 0.4, 0.8, 1)  # Синий цвет для фона аватара
            self.avatar_rect = Rectangle(pos=avatar_panel.pos, size=avatar_panel.size)
        
        avatar_panel.bind(pos=self.update_rect, size=self.update_rect)
        
        # Создаем контейнер для изображения и кнопки
        avatar_container = BoxLayout(
            orientation='vertical',
            spacing=dp(5)
        )
        
        # Проверяем, был ли инициализирован атрибут has_avatar
        if not hasattr(self, 'has_avatar'):
            # Если нет, инициализируем его
            self.cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')
            if not os.path.exists(self.cache_dir):
                os.makedirs(self.cache_dir)
            self.avatar_path = os.path.join(self.cache_dir, 'user_avatar.jpg')
            self.has_avatar = os.path.exists(self.avatar_path)
        
        # Если есть сохраненный аватар, показываем его
        if self.has_avatar:
            self.avatar_image = Image(
                source=self.avatar_path,
                size_hint=(1, 0.8)
            )
        else:
            # Иначе показываем заглушку
            self.avatar_image = Label(
                text='Фото',
                color=(1, 1, 1, 1),
                font_size=font_size,
                size_hint=(1, 0.8)
            )
        
        # Кнопка для загрузки фото
        upload_photo_btn = Button(
            text='Загрузить фото',
            size_hint=(1, 0.2),
            font_size=dp(10),
            background_normal='',
            background_color=(0.3, 0.6, 0.9, 1)
        )
        upload_photo_btn.bind(on_release=self.show_filechooser)
        
        avatar_container.add_widget(self.avatar_image)
        avatar_container.add_widget(upload_photo_btn)
        avatar_panel.add_widget(avatar_container)
        
        # Информация о пользователе
        user_info_panel = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1),
            spacing=dp(5),
            padding=dp(10)
        )
        
        with user_info_panel.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Светло-серый фон
            Rectangle(pos=user_info_panel.pos, size=user_info_panel.size)
        
        user_info_panel.bind(pos=self.update_rect, size=self.update_rect)
        
        # Имя пользователя
        name_label = Label(
            text='Петрова Елена Сергеевна',
            color=(0, 0, 0, 1),
            font_size=title_font_size,
            bold=True,
            size_hint=(1, None),
            height=dp(40),
            halign='left'
        )
        name_label.bind(size=lambda s, w: setattr(s, 'text_size', w))
        
        # Должность
        position_label = Label(
            text='Глава отдела кадров',
            color=(0.3, 0.3, 0.3, 1),
            font_size=font_size,
            size_hint=(1, None),
            height=dp(30),
            halign='left'
        )
        position_label.bind(size=lambda s, w: setattr(s, 'text_size', w))
        
        # Контактная информация
        contact_info = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(80),
            spacing=dp(5)
        )
        
        email_label = Label(
            text='Email: petrova.hr@metran.ru',
            color=(0.3, 0.3, 0.3, 1),
            font_size=info_font_size,
            size_hint=(1, None),
            height=dp(20),
            halign='left'
        )
        email_label.bind(size=lambda s, w: setattr(s, 'text_size', w))
        
        phone_label = Label(
            text='Телефон: +7 (351) 799-51-51',
            color=(0.3, 0.3, 0.3, 1),
            font_size=info_font_size,
            size_hint=(1, None),
            height=dp(20),
            halign='left'
        )
        phone_label.bind(size=lambda s, w: setattr(s, 'text_size', w))
        
        department_label = Label(
            text='Отдел: Управление персоналом',
            color=(0.3, 0.3, 0.3, 1),
            font_size=info_font_size,
            size_hint=(1, None),
            height=dp(20),
            halign='left'
        )
        department_label.bind(size=lambda s, w: setattr(s, 'text_size', w))
        
        # Добавляем все виджеты в контактную информацию
        contact_info.add_widget(email_label)
        contact_info.add_widget(phone_label)
        contact_info.add_widget(department_label)
        
        # Добавляем все виджеты на панель информации
        user_info_panel.add_widget(name_label)
        user_info_panel.add_widget(position_label)
        user_info_panel.add_widget(contact_info)
        user_info_panel.add_widget(Widget())  # Растягивающийся виджет для заполнения пространства
        
        # Добавляем панели на секцию профиля
        profile_section.add_widget(avatar_panel)
        profile_section.add_widget(user_info_panel)
        
        # Добавляем секцию профиля в основной макет
        main_layout.add_widget(profile_section)
        
        # ====================== СЕКЦИЯ СТАТИСТИКИ HR ======================
        # Заголовок секции
        stats_title = Label(
            text='Статистика отдела кадров',
            color=(0, 0, 0, 1),
            font_size=title_font_size,
            size_hint=(1, None),
            height=dp(40),
            halign='left'
        )
        stats_title.bind(size=lambda s, w: setattr(s, 'text_size', w))
        
        main_layout.add_widget(stats_title)
        
        # Контейнер для статистики
        stats_container = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=stats_section_height,
            spacing=dp(20)
        )
        
        # Левая панель статистики
        left_stats = BoxLayout(
            orientation='vertical',
            size_hint=(0.5, 1),
            spacing=dp(10)
        )
        
        with left_stats.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Светло-серый фон
            Rectangle(pos=left_stats.pos, size=left_stats.size)
        
        left_stats.bind(pos=self.update_rect, size=self.update_rect)
        
        # Заголовок левой панели
        left_stats_title = Label(
            text='Показатели персонала',
            color=(0.2, 0.4, 0.8, 1),
            font_size=font_size,
            bold=True,
            size_hint=(1, None),
            height=dp(30)
        )
        
        # Статистика для левой панели
        stats_items_left = [
            ('Всего сотрудников:', '245'),
            ('Новых сотрудников (30 дн):', '12'),
            ('Текучесть кадров:', '5%'),
            ('Средний стаж:', '4.3 года')
        ]
        
        left_stats.add_widget(left_stats_title)
        
        for label_text, value_text in stats_items_left:
            item_layout = BoxLayout(
                orientation='horizontal',
                size_hint=(1, None),
                height=dp(30)
            )
            
            label = Label(
                text=label_text,
                color=(0.3, 0.3, 0.3, 1),
                font_size=info_font_size,
                size_hint=(0.7, 1),
                halign='left'
            )
            label.bind(size=lambda s, w: setattr(s, 'text_size', w))
            
            value = Label(
                text=value_text,
                color=(0, 0, 0, 1),
                font_size=info_font_size,
                bold=True,
                size_hint=(0.3, 1),
                halign='right'
            )
            value.bind(size=lambda s, w: setattr(s, 'text_size', w))
            
            item_layout.add_widget(label)
            item_layout.add_widget(value)
            left_stats.add_widget(item_layout)
        
        # Правая панель статистики
        right_stats = BoxLayout(
            orientation='vertical',
            size_hint=(0.5, 1),
            spacing=dp(10)
        )
        
        with right_stats.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Светло-серый фон
            Rectangle(pos=right_stats.pos, size=right_stats.size)
        
        right_stats.bind(pos=self.update_rect, size=self.update_rect)
        
        # Заголовок правой панели
        right_stats_title = Label(
            text='Эффективность HR',
            color=(0.2, 0.4, 0.8, 1),
            font_size=font_size,
            bold=True,
            size_hint=(1, None),
            height=dp(30)
        )
        
        # Статистика для правой панели
        stats_items_right = [
            ('Закрытые вакансии (мес):', '18'),
            ('Время закрытия вакансии:', '14 дн'),
            ('Удовлетворенность:', '92%'),
            ('Выполнение KPI:', '97%')
        ]
        
        right_stats.add_widget(right_stats_title)
        
        for label_text, value_text in stats_items_right:
            item_layout = BoxLayout(
                orientation='horizontal',
                size_hint=(1, None),
                height=dp(30)
            )
            
            label = Label(
                text=label_text,
                color=(0.3, 0.3, 0.3, 1),
                font_size=info_font_size,
                size_hint=(0.7, 1),
                halign='left'
            )
            label.bind(size=lambda s, w: setattr(s, 'text_size', w))
            
            value = Label(
                text=value_text,
                color=(0, 0, 0, 1),
                font_size=info_font_size,
                bold=True,
                size_hint=(0.3, 1),
                halign='right'
            )
            value.bind(size=lambda s, w: setattr(s, 'text_size', w))
            
            item_layout.add_widget(label)
            item_layout.add_widget(value)
            right_stats.add_widget(item_layout)
        
        # Добавляем панели статистики в контейнер
        stats_container.add_widget(left_stats)
        stats_container.add_widget(right_stats)
        
        # Добавляем контейнер статистики в основной макет
        main_layout.add_widget(stats_container)
        
        # ====================== СЕКЦИЯ МЕНЮ HR ======================
        # Заголовок секции
        menu_title = Label(
            text='Управление персоналом',
            color=(0, 0, 0, 1),
            font_size=title_font_size,
            size_hint=(1, None),
            height=dp(40),
            halign='left'
        )
        menu_title.bind(size=lambda s, w: setattr(s, 'text_size', w))
        
        main_layout.add_widget(menu_title)
        
        # Контейнер для кнопок меню
        menu_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(230),
            spacing=dp(10)
        )
        
        # Список пунктов меню
        menu_items = [
            ('Управление сотрудниками', (0.2, 0.5, 0.2, 1)),
            ('Обработка заявок', (0.2, 0.4, 0.8, 1)),
            ('Отчеты и аналитика', (0.6, 0.3, 0.1, 1)),
            ('Управление обучением', (0.5, 0.2, 0.7, 1))
        ]
        
        for text, bg_color in menu_items:
            btn = Button(
                text=text,
                background_normal='',
                background_color=bg_color,
                color=(1, 1, 1, 1),
                size_hint=(1, None),
                height=button_height,
                font_size=font_size
            )
            menu_container.add_widget(btn)
        
        main_layout.add_widget(menu_container)
        
        # ====================== СЕКЦИЯ НАСТРОЕК ПРОФИЛЯ ======================
        # Заголовок секции
        settings_title = Label(
            text='Настройки профиля',
            color=(0, 0, 0, 1),
            font_size=title_font_size,
            size_hint=(1, None),
            height=dp(40),
            halign='left'
        )
        settings_title.bind(size=lambda s, w: setattr(s, 'text_size', w))
        
        main_layout.add_widget(settings_title)
        
        # Контейнер для кнопок настроек
        settings_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(170),
            spacing=dp(10)
        )
        
        # Список настроек
        settings = [
            ('Изменить личные данные', (0.2, 0.4, 0.8, 1)),
            ('Настройки уведомлений', (0.2, 0.4, 0.8, 1)),
            ('Настройки приватности', (0.2, 0.4, 0.8, 1))
        ]
        
        for text, bg_color in settings:
            btn = Button(
                text=text,
                background_normal='',
                background_color=bg_color,
                color=(1, 1, 1, 1),
                size_hint=(1, None),
                height=button_height,
                font_size=font_size
            )
            settings_container.add_widget(btn)
        
        main_layout.add_widget(settings_container)
        
        # Добавляем отступ перед кнопками
        main_layout.add_widget(Widget(size_hint_y=None, height=dp(20)))
        
        # Добавляем кнопку выхода из профиля
        logout_btn = Button(
            text='Выйти из аккаунта',
            background_normal='',
            background_color=(0.8, 0.2, 0.2, 1),  # Красный цвет для кнопки выхода
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=button_height,
            font_size=font_size
        )
        
        main_layout.add_widget(logout_btn)
        
        # Добавляем отступ внизу
        main_layout.add_widget(Widget(size_hint_y=None, height=dp(20)))
        
        scroll_view.add_widget(main_layout)
        self.content_area.add_widget(scroll_view)
    
    def show_filechooser(self, instance):
        # Создаем всплывающее окно с выбором файла
        content = BoxLayout(orientation='vertical', spacing=dp(5))
        
        # Заголовок
        title_label = Label(
            text='Выберите изображение',
            size_hint_y=None,
            height=dp(30)
        )
        
        # Выбор файла
        file_chooser = FileChooserIconView(
            filters=['*.png', '*.jpg', '*.jpeg'],
            path=os.path.expanduser('~')  # Начинаем с домашней директории
        )
        
        # Кнопки управления
        buttons = BoxLayout(
            size_hint_y=None,
            height=dp(40),
            spacing=dp(5)
        )
        
        # Кнопка отмены
        cancel_btn = Button(text='Отмена')
        cancel_btn.bind(on_release=lambda x: popup.dismiss())
        
        # Кнопка выбора
        select_btn = Button(text='Выбрать')
        select_btn.bind(on_release=lambda x: self.select_image(file_chooser.selection, popup))
        
        # Добавляем кнопки в контейнер
        buttons.add_widget(cancel_btn)
        buttons.add_widget(select_btn)
        
        # Собираем все в контейнер
        content.add_widget(title_label)
        content.add_widget(file_chooser)
        content.add_widget(buttons)
        
        # Создаем и показываем всплывающее окно
        popup = Popup(
            title='Выбор изображения',
            content=content,
            size_hint=(0.9, 0.9)
        )
        popup.open()
    
    def select_image(self, selection, popup):
        if selection:
            try:
                # Получаем путь к выбранному файлу
                selected_file = selection[0]
                
                # Копируем и масштабируем изображение
                self.process_and_save_image(selected_file)
                
                # Обновляем виджет с изображением
                if isinstance(self.avatar_image, Label):
                    # Если это метка (заглушка), удаляем её и создаем Image
                    container = self.avatar_image.parent
                    container.remove_widget(self.avatar_image)
                    self.avatar_image = Image(
                        source=self.avatar_path,
                        size_hint=(1, 0.8)
                    )
                    container.add_widget(self.avatar_image, index=1)
                else:
                    # Если изображение уже существует, обновляем источник
                    self.avatar_image.source = self.avatar_path
                    # Перезагружаем изображение, чтобы отобразить изменения
                    self.avatar_image.reload()
                
                # Устанавливаем флаг наличия аватара
                self.has_avatar = True
                
                # Закрываем всплывающее окно
                popup.dismiss()
                
                # Показываем уведомление об успешной загрузке
                self.show_notification('Изображение успешно загружено')
            except Exception as e:
                # Показываем уведомление об ошибке
                self.show_notification(f'Ошибка загрузки изображения: {str(e)}')
    
    def process_and_save_image(self, file_path):
        # Открываем изображение с использованием PIL
        img = PILImage.open(file_path)
        
        # Определяем максимальный размер для аватара
        max_size = (300, 300)
        
        # Масштабируем изображение с сохранением пропорций
        img.thumbnail(max_size, PILImage.LANCZOS)
        
        # Сохраняем изображение
        img.save(self.avatar_path, 'JPEG', quality=85)
    
    def show_notification(self, message):
        # Создаем простое всплывающее уведомление
        content = BoxLayout(orientation='vertical', padding=dp(10))
        
        # Текст уведомления
        msg_label = Label(
            text=message,
            size_hint_y=None,
            height=dp(40)
        )
        
        # Кнопка закрытия
        close_btn = Button(
            text='OK',
            size_hint_y=None,
            height=dp(40)
        )
        
        # Добавляем элементы в контейнер
        content.add_widget(msg_label)
        content.add_widget(close_btn)
        
        # Создаем всплывающее окно
        popup = Popup(
            title='Уведомление',
            content=content,
            size_hint=(0.7, None),
            height=dp(150)
        )
        
        # Привязываем функцию закрытия к кнопке
        close_btn.bind(on_release=popup.dismiss)
        
        # Показываем уведомление
        popup.open()
        
    def update_rect(self, instance, value):
        # Обновляем фоновый прямоугольник при изменении размеров
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
        elif hasattr(self, 'avatar_rect'):
            self.avatar_rect.pos = instance.pos
            self.avatar_rect.size = instance.size

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = ScreenManager()
        
        # Добавляем все экраны
        self.sm.add_widget(MarkingScreen(name='marking'))
        self.sm.add_widget(AssemblyScreen(name='assembly'))
        self.sm.add_widget(TestingScreen(name='testing'))
        self.sm.add_widget(PackingScreen(name='packing'))
        self.sm.add_widget(GeneralScreen(name='general'))
        self.sm.add_widget(ProfileScreen(name='profile'))
        
        # Устанавливаем начальный экран
        self.sm.current = 'marking'
        
        self.add_widget(self.sm)
    
    def on_nav_button_press(self, button_name):
        if button_name == 'statistics':
            # Переключаемся на экран статистики в главном ScreenManager
            app = App.get_running_app()
            app.sm.current = 'statistics'
        else:
            # Стандартная обработка для других кнопок
            if button_name in self.sm.screen_names:
                self.sm.current = button_name

# Добавляем класс приложения для самостоятельного запуска
class StandaloneButtonApp(App):
    def build(self):
        # Регистрируем шрифт для цифр
        fonts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
        
        # Создаем директорию для шрифтов, если она не существует
        if not os.path.exists(fonts_path):
            os.makedirs(fonts_path)
            
        # Комментируем регистрацию шрифта, будем использовать стандартный Roboto
        # try:
        #     LabelBase.register(name='RobotoMono-Regular', 
        #                      fn_regular=os.path.join(fonts_path, 'RobotoMono-Regular.ttf'))
        # except Exception as e:
        #     print(f"Ошибка при регистрации шрифта: {e}")
        
        # Получаем размеры экрана
        screen_width = Window.width
        screen_height = Window.height
        
        # Настройки для разных типов устройств
        if screen_width < dp(600):  # Телефон
            self.nav_panel_width = dp(160)
            self.font_size = dp(14)
            self.button_height = dp(45)
        elif screen_width < dp(900):  # Планшет среднего размера
            self.nav_panel_width = dp(200)
            self.font_size = dp(16)
            self.button_height = dp(50)
        else:  # Большой планшет или десктоп
            self.nav_panel_width = dp(250)
            self.font_size = dp(18)
            self.button_height = dp(55)
        
        Window.maximize()
        return MainScreen()

# Добавляем блок для самостоятельного запуска
if __name__ == '__main__':
    StandaloneButtonApp().run()