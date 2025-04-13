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
                height=dp(40)  # Базовая высота кнопки
            )
            btn.bind(on_release=lambda x, sn=screen_name: setattr(self.manager, 'current', sn))
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

# Конкретные экраны
class MarkingScreen(BaseScreen):
    def create_content(self):
        self.content_area.clear_widgets()
        self.content_area.add_widget(Label(text='Экран маркировки', font_size=dp(24)))

class AssemblyScreen(BaseScreen):
    def create_content(self):
        self.content_area.clear_widgets()
        self.content_area.add_widget(Label(text='Экран сборки', font_size=dp(24)))

class TestingScreen(BaseScreen):
    def create_content(self):
        self.content_area.clear_widgets()
        self.content_area.add_widget(Label(text='Экран тестирования', font_size=dp(24)))

class PackingScreen(BaseScreen):
    def create_content(self):
        self.content_area.clear_widgets()
        self.content_area.add_widget(Label(text='Экран упаковки', font_size=dp(24)))

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