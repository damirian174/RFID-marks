from machine import UART, Pin
import time

# Настройка UART0
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

count = 0

while True:
    data = f"Hello from Pico! Count: {count}\n"
    uart.write(data.encode())  # Отправляем строку, закодированную в байты
    print(f"Pico sent: {data.strip()}")
    count += 1
    time.sleep(1)  # Задержка 1 секунда