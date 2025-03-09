import socket
import json
from config import serverip, port
from logger import *


def database(request_data):
    if request_data['type'] == 'report':
        return "OK"
    try:
        # Создаем соединение с сервером
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((serverip, port))
            
            # Отправляем JSON-запрос
            client_socket.sendall(json.dumps(request_data).encode('utf-8'))
            
            # Получаем полный ответ от сервера
            response_data = b""
            while True:
                chunk = client_socket.recv(4096)
                if not chunk:  # Если данных больше нет, выходим из цикла
                    break
                response_data += chunk
            
            # Декодируем и преобразуем ответ
            response = response_data.decode('utf-8')
            try:
                worker = json.loads(response)
                log_event(f"Запрос: {request_data}")
                log_event(f"Ответ: {worker}")
                return worker  # Возвращаем объект Python (словарь)
            except json.JSONDecodeError:
                log_error(f"Ошибка декодирования JSON: {response}")
                return None
    except (socket.error, socket.timeout) as e:
        log_error(f"Ошибка при подключении к серверу: {e}")
        return None
    except Exception as e:
        log_error(f"Непредвиденная ошибка: {e}")
        return None
