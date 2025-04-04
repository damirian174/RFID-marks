from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.utils import platform

Builder.load_string('''
<AdaptiveButton@Button>:
    font_size: root.height * 0.3
    padding: (dp(10), (dp(10))

<NavigationPanel>:
    orientation: 'vertical'
    size_hint_x: None
    width: root.panel_width
    spacing: dp(10)
    padding: dp(10)
    canvas.before:
        Color:
            rgba: 0, 0.294, 0.553, 1  # HEX #004B8D
        Rectangle:
            pos: self.pos
            size: self.size
    
    AdaptiveButton:
        text: 'Маркировка'
        background_normal: ''
        background_color: 0, 0.4, 0.7, 1
        color: 1, 1, 1, 1
        on_release: app.root.navigate('marking')
    
    AdaptiveButton:
        text: 'Сборка'
        background_normal: ''
        background_color: 0, 0.4, 0.7, 1
        color: 1, 1, 1, 1
        on_release: app.root.navigate('assembly')
    
    AdaptiveButton:
        text: 'Тестирование'
        background_normal: ''
        background_color: 0, 0.4, 0.7, 1
        color: 1, 1, 1, 1
        on_release: app.root.navigate('testing')
    
    AdaptiveButton:
        text: 'Упаковка'
        background_normal: ''
        background_color: 0, 0.4, 0.7, 1
        color: 1, 1, 1, 1
        on_release: app.root.navigate('packing')
    
    AdaptiveButton:
        text: 'Общее'
        background_normal: ''
        background_color: 0, 0.4, 0.7, 1
        color: 1, 1, 1, 1
        on_release: app.root.navigate('general')
    
    AdaptiveButton:
        text: 'Профиль'
        background_normal: ''
        background_color: 0, 0.4, 0.7, 1
        color: 1, 1, 1, 1
        on_release: app.root.navigate('profile')
    
    Widget:
        size_hint_y: 1
    
    AdaptiveButton:
        text: 'Выход'
        size_hint_y: None
        height: dp(50)
        background_normal: ''
        background_color: 0.8, 0.2, 0.2, 1
        color: 1, 1, 1, 1

<BaseScreen>:
    BoxLayout:
        orientation: 'horizontal'
        spacing: 0
        
        NavigationPanel:
            panel_width: root.panel_width
        
        BoxLayout:
            orientation: 'vertical'
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
''')

class NavigationPanel(BoxLayout):
    pass

class BaseScreen(Screen):
    panel_width = NumericProperty(dp(200))  # Начальная ширина панели
    
    def on_size(self, *args):
        # Адаптируем ширину панели в зависимости от ориентации и размера экрана
        if Window.width < Window.height:  # Портретная ориентация
            self.panel_width = min(dp(200), Window.width * 0.4)
        else:  # Альбомная ориентация
            self.panel_width = min(dp(250), Window.width * 0.25)

class MarkingScreen(BaseScreen):
    pass

class AssemblyScreen(BaseScreen):
    pass

class TestingScreen(BaseScreen):
    pass

class PackingScreen(BaseScreen):
    pass

class GeneralScreen(BaseScreen):
    pass

class ProfileScreen(BaseScreen):
    pass

class MainAppLayout(BoxLayout):
    screen_manager = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(MarkingScreen(name='marking'))
        self.screen_manager.add_widget(AssemblyScreen(name='assembly'))
        self.screen_manager.add_widget(TestingScreen(name='testing'))
        self.screen_manager.add_widget(PackingScreen(name='packing'))
        self.screen_manager.add_widget(GeneralScreen(name='general'))
        self.screen_manager.add_widget(ProfileScreen(name='profile'))
        self.add_widget(self.screen_manager)
    
    def navigate(self, screen_name):
        self.screen_manager.current = screen_name

class MyApp(App):
    def build(self):
        # Настройки для разных платформ
        if platform == 'android' or platform == 'ios':
            from kivy.config import Config
            Config.set('kivy', 'exit_on_escape', '0')
            
        Window.bind(on_resize=self.on_window_resize)
        return MainAppLayout()
    
    def on_window_resize(self, window, width, height):
        # Обновляем размеры при изменении окна
        for screen in self.root.screen_manager.screens:
            screen.on_size()

if __name__ == '__main__':
    MyApp().run()