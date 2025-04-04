# Основные модули Kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

# KV язык для базового интерфейса
kv = '''
<BarChartWidget>:
    canvas:
        Color:
            rgba: 0.8, 0.9, 1, 1  # Светло-голубой фон
        Rectangle:
            pos: self.pos
            size: self.size

<BarChartApp>:
    orientation: 'vertical'
    Label:
        text: 'Адаптивный столбчатый график'
        size_hint_y: 0.1
        color: [0.2, 0.2, 0.2, 1]  # Тёмно-серый текст для контраста
        bold: True
    BarChartWidget:
        id: bar_chart
'''

# Данные для графика
data = {'A': 50, 'B': 70, 'C': 30, 'D': 90, 'E': 60}

# Пастельные цвета для каждого столбца (RGB в диапазоне 0-1)
pastel_colors = [
    (0.9, 0.7, 0.7, 1),  # Нежно-розовый
    (0.7, 0.9, 0.7, 1),  # Нежно-зелёный
    (0.7, 0.7, 0.9, 1),  # Нежно-синий
    (0.9, 0.8, 0.7, 1),  # Нежно-персиковый
    (0.8, 0.7, 0.9, 1)   # Нежно-фиолетовый
]

class BarChartWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.update_bars, pos=self.update_bars)
        self.draw_bars()

    def draw_bars(self):
        self.canvas.clear()  # Очищаем канвас перед перерисовкой
        with self.canvas:
            # Фон задан в KV (светло-голубой)
            Color(0.8, 0.9, 1, 1)
            Rectangle(pos=self.pos, size=self.size)

            # Рисуем столбцы
            bar_width = self.width / (len(data) + 1)  # Адаптивная ширина столбцов
            max_height = max(data.values())  # Максимальная высота для масштабирования
            padding = bar_width * 0.2  # Отступ между столбцами

            for i, (label, value) in enumerate(data.items()):
                # Устанавливаем пастельный цвет для каждого столбца
                Color(*pastel_colors[i % len(pastel_colors)])  # Циклическое использование цветов
                bar_height = (value / max_height) * self.height * 0.8  # Масштабируем высоту
                bar_x = self.x + padding + i * bar_width
                bar_y = self.y
                Rectangle(pos=(bar_x, bar_y), size=(bar_width - padding, bar_height))

                # Подписи под столбцами
                lbl = Label(text=label,
                            pos=(bar_x + (bar_width - padding) / 2 - 10, bar_y - 30),
                            size=(20, 20), font_size=16, color=(0.2, 0.2, 0.2, 1))  # Тёмный текст
                self.add_widget(lbl)

                # Значения над столбцами
                val_lbl = Label(text=str(value),
                                pos=(bar_x + (bar_width - padding) / 2 - 10, bar_y + bar_height + 5),
                                size=(20, 20), font_size=14, color=(0.2, 0.2, 0.2, 1))
                self.add_widget(val_lbl)

    def update_bars(self, *args):
        self.draw_bars()  # Перерисовываем при изменении размера

class BarChartApp(BoxLayout):
    pass

class MyApp(App):
    def build(self):
        Builder.load_string(kv)
        return BarChartApp()

if __name__ == '__main__':
    Window.size = (800, 600)  # Начальный размер окна
    MyApp().run()