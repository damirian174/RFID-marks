from PySide6.QtCore import QThread, Signal
import serial
import time
from GetDetail import getDetail

# Настройки порта
arduino_port = "COM3"  # Ваш порт
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
                    data = ser.readline().decode('utf-8').strip()
                    self.data_received.emit(data)
        except serial.SerialException as e:
            print(f"Ошибка при работе с COM портом: {e}")
        finally:
            if ser.is_open:
                ser.close()

    def stop(self):
        self.running = False
