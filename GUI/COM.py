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
            try:
                cls._instance.serial = serial.Serial(port, baud_rate, timeout=1)
                log_event(f"SerialManager: Успешно открыт порт {port}")
            except serial.SerialException as e:
                log_error(f"SerialManager: Ошибка открытия порта {port}: {e}")
                cls._instance.serial = None
        return cls._instance

    def get_serial(self):
        return self.serial

    def close(self):
        if hasattr(self, 'serial') and self.serial and self.serial.is_open:
            try:
                self.serial.close()
                log_event(f"SerialManager: Порт {self.port} закрыт")
            except Exception as e:
                log_error(f"SerialManager: Ошибка при закрытии порта {self.port}: {e}")
        SerialManager._instance = None
        
    def reopen(self):
        """Пытается заново открыть порт, если он был закрыт или отключен"""
        if hasattr(self, 'serial') and self.serial:
            if not self.serial.is_open:
                try:
                    self.serial = serial.Serial(self.port, self.baud_rate, timeout=1)
                    log_event(f"SerialManager: Успешно переоткрыт порт {self.port}")
                    return True
                except serial.SerialException as e:
                    log_error(f"SerialManager: Ошибка переоткрытия порта {self.port}: {e}")
        return False

class SerialListener(QThread):
    data_received = Signal(object)
    connection_lost = Signal()  # Сигнал о потере соединения

    def __init__(self, serial_manager):
        super().__init__()
        self.serial_manager = serial_manager
        self.ser = serial_manager.get_serial()
        self.running = True
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        self.reconnect_interval = 2000  # 2 секунды между попытками

    def run(self):
        try:
            while self.running:
                try:
                    # Проверка, что порт открыт
                    if not self.ser or not self.ser.is_open:
                        # Пробуем переоткрыть порт
                        if self.reconnect_attempts < self.max_reconnect_attempts:
                            log_event(f"SerialListener: Попытка переподключения {self.reconnect_attempts+1}/{self.max_reconnect_attempts}")
                            if self.serial_manager.reopen():
                                self.ser = self.serial_manager.get_serial()
                                self.reconnect_attempts = 0
                                log_event("SerialListener: Переподключение успешно")
                            else:
                                self.reconnect_attempts += 1
                                time.sleep(self.reconnect_interval / 1000)
                        else:
                            log_error("SerialListener: Превышено максимальное количество попыток переподключения")
                            self.connection_lost.emit()
                            break
                        continue
                            
                    if self.ser.in_waiting > 0:
                        # Успешное чтение, сбрасываем счетчик попыток
                        self.reconnect_attempts = 0
                        
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
                                log_event("System МЭТР init")
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
                    
                    # Небольшая пауза, чтобы не нагружать CPU
                    time.sleep(0.1)
                        
                except serial.SerialException as e:
                    # Если произошла ошибка при работе с портом (например, устройство отключено)
                    log_error(f"SerialListener: Ошибка COM-порта: {e}")
                    # Пробуем переоткрыть порт
                    self.reconnect_attempts += 1
                    if self.reconnect_attempts >= self.max_reconnect_attempts:
                        log_error("SerialListener: Превышено максимальное количество попыток переподключения")
                        self.connection_lost.emit()
                        break
                    time.sleep(self.reconnect_interval / 1000)

        except Exception as e:
            log_error(f"SerialListener: Неожиданная ошибка: {e}")
            self.connection_lost.emit()
            
    def stop(self):
        self.running = False
