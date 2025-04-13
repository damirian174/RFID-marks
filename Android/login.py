from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget

Window.clearcolor = (0.96, 0.96, 0.96, 1)  # Светло-серый фон

class CustomTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (1, 1, 1, 1)
        self.padding = [dp(15), dp(12), dp(15), dp(12)]
        self.multiline = False
        self.size_hint_y = None
        self.height = dp(48)  # Базовая высота
        self.error = False
        self.font_size = sp(16)
        self.hint_text_color = (0, 0, 0, 0.3)  # Цвет текста подсказки
        self.foreground_color = (0, 0, 0, 0.75)  # Цвет вводимого текста
        self.line_height = 1.2  # Устанавливаем межстрочный интервал напрямую
        
    def on_error(self, instance, value):
        if value:
            self.background_color = (1, 0.8, 0.8, 1)
            self.hint_text_color = (0.8, 0, 0, 0.5)  # Красноватый цвет подсказки при ошибке
        else:
            self.background_color = (1, 1, 1, 1)
            self.hint_text_color = (0, 0, 0, 0.3)  # Возвращаем обычный цвет подсказки

    def on_size(self, instance, value):
        # Обновляем внутренние отступы при изменении размера
        font_size = self.font_size
        if isinstance(font_size, str):
            font_size = float(font_size.replace('sp', ''))
        
        # Рассчитываем отступы на основе размера шрифта
        base_padding = font_size * 0.8
        horizontal_padding = max(dp(12), min(dp(20), base_padding))
        vertical_padding = max(dp(8), min(dp(15), base_padding * 0.6))
        
        # Применяем отступы
        self.padding = [horizontal_padding, vertical_padding, horizontal_padding, vertical_padding]

class LoginScreen(Screen):
    error_message = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = (0.96, 0.96, 0.96, 1)  # Светло-серый фон
        self.setup_ui()
        Window.bind(on_resize=self._update_layout)
    
    def setup_ui(self):
        # Основной контейнер на весь экран с центрированием
        self.main_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(20)
        )
        
        # Добавляем растягивающийся виджет сверху для центрирования
        self.main_layout.add_widget(Widget())
        
        # Центральный контейнер для формы
        self.center_layout = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            width=dp(400),
            height=dp(400),
            pos_hint={'center_x': 0.5},
            spacing=dp(15),
            padding=[dp(20), dp(20), dp(20), dp(20)]
        )
        
        # Заголовки
        self.title_label = Label(
            text='ВХОД В СИСТЕМУ',
            size_hint_y=None,
            height=dp(40),
            color=(0, 0, 0, 0.87),
            halign='center'
        )
        
        self.subtitle_label = Label(
            text='Метран',
            size_hint_y=None,
            height=dp(50),
            color=(0, 0, 0, 0.87),
            halign='center'
        )
        
        # Поля ввода
        self.username = CustomTextInput(
            hint_text='Логин',
            size_hint=(None, None),
            width=dp(360),
            pos_hint={'center_x': 0.5}
        )
        
        self.password = CustomTextInput(
            hint_text='Пароль',
            password=True,
            size_hint=(None, None),
            width=dp(360),
            pos_hint={'center_x': 0.5}
        )
        
        # Сообщение об ошибке
        self.error_label = Label(
            text=self.error_message,
            color=(1, 0, 0, 1),
            size_hint_y=None,
            height=dp(20),
            halign='center'
        )
        self.bind(error_message=self.error_label.setter('text'))
        
        # Кнопка входа
        self.login_button = Button(
            text='Войти',
            size_hint=(None, None),
            size=(dp(200), dp(48)),
            pos_hint={'center_x': 0.5},
            background_normal='',
            background_color=(0, 0.294, 0.553, 1),
            color=(1, 1, 1, 1)
        )
        self.login_button.bind(on_release=self.login)
        
        # Добавляем виджеты в центральный контейнер
        self.center_layout.add_widget(Widget(size_hint_y=None, height=dp(20)))
        self.center_layout.add_widget(self.title_label)
        self.center_layout.add_widget(self.subtitle_label)
        self.center_layout.add_widget(Widget(size_hint_y=None, height=dp(20)))
        self.center_layout.add_widget(self.username)
        self.center_layout.add_widget(self.password)
        self.center_layout.add_widget(self.error_label)
        self.center_layout.add_widget(self.login_button)
        self.center_layout.add_widget(Widget())
        
        # Добавляем центральный контейнер в основной layout
        self.main_layout.add_widget(self.center_layout)
        
        # Добавляем растягивающийся виджет снизу для центрирования
        self.main_layout.add_widget(Widget())
        
        # Очищаем экран и добавляем основной layout
        self.clear_widgets()
        self.add_widget(self.main_layout)
        
        # Вызываем обновление layout сразу после создания
        self._update_layout(Window, Window.width, Window.height)
    
    def _update_layout(self, *args):
        # Получаем текущие размеры окна
        width = Window.width if len(args) < 2 else args[1]
        height = Window.height if len(args) < 3 else args[2]
        
        # Определяем ориентацию и тип устройства
        is_landscape = width > height
        is_phone = min(width, height) < dp(600)
        is_tablet = dp(600) <= min(width, height) < dp(1024)
        
        # Определяем, является ли высота экрана критически малой
        is_height_critical = height < dp(400)
        
        # Рассчитываем базовые размеры в зависимости от типа устройства и ориентации
        if is_phone:
            if is_landscape:
                form_width = height * 0.8
                base_height = dp(40) if is_height_critical else dp(45)
                spacing = dp(8) if is_height_critical else dp(12)
                padding = dp(10) if is_height_critical else dp(15)
                title_scale = 1.4 if is_height_critical else 1.8
                subtitle_scale = 1.6 if is_height_critical else 2.2
                input_scale = 1.2 if is_height_critical else 1.4
            else:
                form_width = width * 0.95
                base_height = dp(45) if is_height_critical else dp(50)
                spacing = dp(10) if is_height_critical else dp(15)
                padding = dp(15) if is_height_critical else dp(20)
                title_scale = 1.6 if is_height_critical else 2.0
                subtitle_scale = 1.8 if is_height_critical else 2.4
                input_scale = 1.3 if is_height_critical else 1.6
        elif is_tablet:
            if is_landscape:
                form_width = height * 0.7
                base_height = dp(45) if is_height_critical else dp(52)
                spacing = dp(12) if is_height_critical else dp(18)
                padding = dp(15) if is_height_critical else dp(25)
                title_scale = 1.3 if is_height_critical else 1.6
                subtitle_scale = 1.5 if is_height_critical else 2.0
                input_scale = 1.1 if is_height_critical else 1.3
            else:
                form_width = width * 0.7
                base_height = dp(42) if is_height_critical else dp(48)
                spacing = dp(10) if is_height_critical else dp(15)
                padding = dp(15) if is_height_critical else dp(20)
                title_scale = 1.2 if is_height_critical else 1.4
                subtitle_scale = 1.4 if is_height_critical else 1.8
                input_scale = 1.1 if is_height_critical else 1.2
        else:  # Десктоп
            form_width = min(width * 0.5, dp(600))
            base_height = dp(45) if is_height_critical else dp(56)
            spacing = dp(12) if is_height_critical else dp(20)
            padding = dp(15) if is_height_critical else dp(25)
            title_scale = 1.2 if is_height_critical else 1.4
            subtitle_scale = 1.4 if is_height_critical else 1.8
            input_scale = 1.0 if is_height_critical else 1.1
        
        # Рассчитываем минимальную необходимую высоту для контента
        min_content_height = (
            base_height * 1.2 +  # Заголовок
            base_height * 1.5 +  # Подзаголовок
            base_height * 2 +    # Два поля ввода
            base_height +        # Кнопка
            spacing * 6 +        # Отступы между элементами
            padding * 2          # Верхний и нижний padding
        )
        
        # Обновляем размеры контейнера с учетом минимальной высоты
        self.center_layout.width = form_width
        form_height = max(min_content_height, height * (0.7 if is_landscape else 0.6))
        self.center_layout.height = form_height
        self.center_layout.spacing = spacing
        self.center_layout.padding = [padding] * 4
        
        # Рассчитываем размеры элементов
        input_width = form_width - (padding * 2)
        button_width = min(input_width * (0.8 if is_phone else 0.6), dp(300))
        
        # Обновляем размеры полей ввода
        self.username.width = input_width
        self.username.height = base_height
        self.password.width = input_width
        self.password.height = base_height
        
        # Обновляем размеры заголовков с учетом критической высоты
        title_height = base_height * (1.0 if is_height_critical else 1.2)
        subtitle_height = base_height * (1.2 if is_height_critical else 1.5)
        self.title_label.height = title_height
        self.subtitle_label.height = subtitle_height
        
        # Обновляем размеры кнопки
        self.login_button.size = (button_width, base_height)
        
        # Масштабируем шрифты с учетом критической высоты
        min_side = min(width, height)
        if is_phone:
            base_font_size = min_side * (0.035 if is_height_critical else (0.04 if is_landscape else 0.045))
        else:
            base_font_size = min_side * (0.025 if is_height_critical else (0.03 if is_landscape else 0.035))
        
        # Рассчитываем размеры шрифтов с учетом масштаба и ограничений
        max_title_size = sp(24) if is_height_critical else sp(32)
        max_subtitle_size = sp(28) if is_height_critical else sp(40)
        
        # Устанавливаем минимальный размер шрифта для полей ввода
        min_input_size = sp(14)  # Минимальный размер для читаемости
        max_input_size = sp(18) if is_height_critical else sp(22)  # Уменьшили максимальный размер
        
        title_font_size = min(max_title_size, base_font_size * title_scale)
        subtitle_font_size = min(max_subtitle_size, base_font_size * subtitle_scale)
        # Обеспечиваем минимальный размер шрифта для полей ввода
        input_font_size = max(min_input_size, min(max_input_size, base_font_size * input_scale))
        
        # Применяем размеры шрифтов
        self.title_label.font_size = title_font_size
        self.subtitle_label.font_size = subtitle_font_size
        self.username.font_size = input_font_size
        self.password.font_size = input_font_size
        self.error_label.font_size = input_font_size * 0.9
        self.login_button.font_size = input_font_size
        
        # Обновляем отступы полей ввода с учетом размера шрифта
        # Рассчитываем отступы пропорционально размеру шрифта
        base_padding = input_font_size * 0.8  # Базовый отступ относительно размера шрифта
        horizontal_padding = max(dp(12), min(dp(20), base_padding))  # Ограничиваем минимальный и максимальный отступы
        vertical_padding = max(dp(8), min(dp(15), base_padding * 0.6))  # Вертикальный отступ немного меньше
        
        # Применяем отступы к полям ввода
        self.username.padding = [horizontal_padding, vertical_padding, horizontal_padding, vertical_padding]
        self.password.padding = [horizontal_padding, vertical_padding, horizontal_padding, vertical_padding]
        
        # Обновляем высоту полей ввода с учетом размера шрифта
        input_height = max(base_height, input_font_size * 2.5)  # Высота поля минимум в 2.5 раза больше размера шрифта
        self.username.height = input_height
        self.password.height = input_height
    
    def login(self, *args):
        username = self.username.text.strip()
        password = self.password.text.strip()
        
        self.username.error = False
        self.password.error = False
        self.error_message = ""
        
        if not username and not password:
            self.error_message = "Введите логин и пароль"
            self.username.error = True
            self.password.error = True
        elif not username:
            self.error_message = "Введите логин"
            self.username.error = True
        elif not password:
            self.error_message = "Введите пароль"
            self.password.error = True
        else:
            if not self.validate_credentials(username, password):
                self.error_message = "Неверный логин или пароль"
                self.username.error = True
                self.password.error = True
            else:
                self.on_successful_login()
    
    def validate_credentials(self, username, password):
        return username == "admin" and password == "1234"
    
    def on_successful_login(self):
        if hasattr(App.get_running_app(), 'switch_to_main_app'):
            # Если запущено как часть основного приложения
            App.get_running_app().switch_to_main_app()
        else:
            # Если запущено самостоятельно
            from button import MainScreen
            # Создаем и настраиваем главный экран
            main_screen = MainScreen(name='main')
            # Добавляем главный экран в менеджер экранов
            self.manager.add_widget(main_screen)
            # Переходим на главный экран
            self.manager.current = 'main'

# Добавляем класс приложения для самостоятельного запуска
class StandaloneLoginApp(App):
    def build(self):
        Window.maximize()
        # Создаем менеджер экранов
        sm = ScreenManager()
        # Добавляем экран логина
        login_screen = LoginScreen(name='login')
        sm.add_widget(login_screen)
        return sm

# Добавляем блок для самостоятельного запуска
if __name__ == '__main__':
    StandaloneLoginApp().run()