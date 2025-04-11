from PySide6.QtCore import QThread, Signal
import serial
import time
from detail_work import getDetail
import re
from logger import *
import config
from error_test import *

# Настройки порта
baud_rate = 9600


class SerialManager:
    _instance = None

    def __new__(cls, port, baud_rate):
        if cls._instance is None:
            cls._instance = super(SerialManager, cls).__new__(cls)
            cls._instance.port = port
            cls._instance.baud_rate = baud_rate
            cls._instance.serial = serial.Serial(port, baud_rate, timeout=1)
        return cls._instance

    def get_serial(self):
        return self.serial

    def close(self):
        if self.serial and self.serial.is_open:
            self.serial.close()
            SerialManager._instance = None

class SerialListener(QThread):
    data_received = Signal(object)

    def __init__(self, serial_manager):
        super().__init__()
        self.serial_manager = serial_manager
        self.ser = serial_manager.get_serial()
        self.running = True

    def run(self):
        try:
            while self.running:
                if self.ser.in_waiting > 0:
                    raw_data = self.ser.readline()
                    log_event(f"Raw data (bytes): {raw_data}")  

                    try:
                        data = raw_data.decode('utf-8').strip()
                        log_event(f"Decoded data (str): {data}")  
                        if "Поднесите карту для записи данных" in data:
                            self.data_received.emit(["WAIT_CARD", data])
                            log_event("Ожидание поднесения карты")
                            continue


                        if not data:
                            log_event("Get NULL")
                            continue  

                        x = data.split(".", maxsplit=1)    
                        if x[0] == "READ_ERROR":
                            log_error("Error with read")
                            self.data_received.emit("READ_ERROR")
                            continue             

                        if x[0] == "WRITE_SUCCESS":
                            log_event("Write secces")
                            self.data_received.emit(["WRITE_SUCCESS", "status"])
                            continue
                        elif x[0] == "WRITE_ERROR":
                            log_error("Error with write")
                            self.data_received.emit("WRITE_ERROR")
                            continue
                        b = x[0].split("_")  
                        log_event(f"Parsed Data: {b}")
                        if b[0] == "Агуагу":
                            log_event("System Arduino init")
                            continue

                        config.user = b

                        if len(b) >= 2:
                            log_event(f"Send data to handle_serial_data: {b}")  
                            self.data_received.emit(b)
                        else:
                            log_error(f"Error, Incorrect data to send: {b}")

                    except UnicodeDecodeError:
                        log_error(f"Decode Error: {raw_data}")
                        continue

        except serial.SerialException as e:
            log_error(f"Error work with COM port: {e}")
    def stop(self):
        self.running = False
