import time
import os
from Work import Ui_MainWindow

def start():
    старт = time.time()
    secondamar_runen = 1
    try:
        while True:
            текущий = time.time()
            прошло = текущий - старт
            часы = int(прошло // 3600)
            минуты = int(прошло // 60)
            секунды = int(прошло % 60)
            os.system('cls' if os.name == 'nt' else 'clear')  # Очистка экрана
            time = f"{часы:02}:{минуты:02}:{секунды:02}"
            Ui_MainWindow.UpdateTime(time)
            time.sleep(0.5)  # Обновление каждые 0.5 секунды

    except KeyboardInterrupt:
        print("\nСекундомер остановлен.")
