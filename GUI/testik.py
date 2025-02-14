import serial
import time

# Настроим последовательный порт для связи с Arduino
arduino = serial.Serial('COM8', 9600)  # Убедитесь, что порт правильный

def send_data_to_arduino(data):
    arduino.write(data.encode())  # Отправляем данные как строку в байтах
    print(f"Данные отправлены на Arduino: {data}")

# Отправляем строку для записи на карту
send_data_to_arduino("Hello RFID")

# Закрываем соединение с Arduino
time.sleep(1)  # Ждем немного, чтобы дать время на выполнение
arduino.close()
