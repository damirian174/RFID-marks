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
from krygli import PieChart
from ctolb import BarChart
from tochka import LineChart
import socket
import json
import time
import datetime

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
    def create_content(self):
        self.content_area.clear_widgets()
        self.content_area.add_widget(Label(text='Экран профиля', font_size=dp(24)))

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