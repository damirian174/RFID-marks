from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.properties import BooleanProperty, StringProperty

Window.clearcolor = (0.96, 0.96, 0.96, 1)  # Светло-серый фон

class LoginScreen(Screen):
    error_message = StringProperty("")
    
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.bind(size=self._update_layout)
        self._update_layout()
    
    def _update_layout(self, *args):
        # Обновляем размеры при изменении размера экрана
        if self.width < 600:  # Мобильные устройства
            self.ids.title_label.font_size = sp(24)
            self.ids.username.font_size = sp(14)
            self.ids.password.font_size = sp(14)
            self.ids.error_label.font_size = sp(12)
            self.ids.login_button.font_size = sp(14)
        else:  # Планшеты и десктопы
            self.ids.title_label.font_size = sp(28)
            self.ids.username.font_size = sp(16)
            self.ids.password.font_size = sp(16)
            self.ids.error_label.font_size = sp(14)
            self.ids.login_button.font_size = sp(16)
    
    def login(self):
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()
        
        self.ids.username.error = False
        self.ids.password.error = False
        self.error_message = ""
        
        if not username and not password:
            self.error_message = "Введите логин и пароль"
            self.ids.username.error = True
            self.ids.password.error = True
        elif not username:
            self.error_message = "Введите логин"
            self.ids.username.error = True
        elif not password:
            self.error_message = "Введите пароль"
            self.ids.password.error = True
        else:
            if not self.validate_credentials(username, password):
                self.error_message = "Неверный логин или пароль"
                self.ids.username.error = True
                self.ids.password.error = True
            else:
                self.on_successful_login()
    
    def validate_credentials(self, username, password):
        # Замените на реальную проверку
        return username == "admin" and password == "1234"
    
    def on_successful_login(self):
        print("Успешный вход!")
        # self.manager.current = 'main_screen'

class LoginApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        return sm

if __name__ == '__main__':
    LoginApp().run()