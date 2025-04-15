from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.core.text import LabelBase  # Для регистрации шрифтов
import os

from login import LoginScreen
from button import MainScreen
from statistics import StatisticsScreen

class MetranApp(App):
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
        
        # Устанавливаем полноэкранный режим
        Window.maximize()
        
        # Определяем тип устройства на основе размера экрана
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
        
        # Создаем менеджер экранов
        self.sm = ScreenManager()
        
        # Добавляем экран логина
        self.login_screen = LoginScreen(name='login')
        self.sm.add_widget(self.login_screen)
        
        # Добавляем главный экран
        self.main_screen = MainScreen(name='main')
        self.sm.add_widget(self.main_screen)
        
        # Добавляем экран статистики
        self.statistics_screen = StatisticsScreen(name='statistics')
        self.sm.add_widget(self.statistics_screen)
        
        # Устанавливаем начальный экран как экран логина
        self.sm.current = 'login'
        
        return self.sm
    
    def switch_to_main_app(self):
        self.sm.current = 'main'

if __name__ == '__main__':
    MetranApp().run()