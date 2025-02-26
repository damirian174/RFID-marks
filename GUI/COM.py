from PySide6.QtCore import QThread, Signal
import serial
import time
from detail_work import getDetail
import re


# Настройки порта
baud_rate = 9600

class SerialListener(QThread):
    data_received = Signal(str)

    def __init__(self, port, baud_rate):
        super().__init__()
        self.port = port
        self.baud_rate = baud_rate
        self.running = True

    def run(self):
        try:
            ser = serial.Serial(self.port, self.baud_rate)
            while self.running:
                if ser.in_waiting > 0:
                    # Чтение сырых данных
                    raw_data = ser.readline()
                    print(f"Raw data: {raw_data}")  # Логирование сырых данных

                    try:
                        # Попытка декодирования в UTF-8
                        data = raw_data.decode('utf-8').strip()
                        x = data.split(" ")
                        self.data_received.emit(x[0])
                    except UnicodeDecodeError:
                        # Если декодирование не удалось, используем замену недопустимых символов
                        data = raw_data.decode('utf-8', errors='replace').strip()
                        print(f"Decoded with errors: {data}")  # Логирование данных с ошибками
                        x = data.split(" ")
                        self.data_received.emit(x[0])
                    
        except serial.SerialException as e:
            print(f"Ошибка при работе с COM портом: {e}")
        finally:
            if ser.is_open:
                ser.close()

    def stop(self):
        self.running = False