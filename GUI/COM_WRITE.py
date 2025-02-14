import serial
import time

def send_to_arduino(data, port="COM8", baudrate=9600, timeout=2):
    """
    Отправляет строку данных на Arduino через Serial.
    :param data: Строка для записи на RFID-карту.
    :param port: Порт, к которому подключен Arduino (например, "COM3" или "/dev/ttyUSB0").
    :param baudrate: Скорость передачи данных (по умолчанию 9600).
    :param timeout: Таймаут соединения.
    """
    try:
        with serial.Serial(port, baudrate, timeout=timeout) as ser:
            time.sleep(2)  # Ждем установления соединения
            ser.write((data + "\n").encode("utf-8"))  # Отправка данных
            print(f"Отправлено: {data}")
    except serial.SerialException as e:
        print(f"Ошибка соединения: {e}")

# Пример использования
if __name__ == "__main__":
    data_to_write = "SN010"  # Данные для записи
    send_to_arduino(data_to_write)
