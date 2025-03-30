import socket
import json
from config import serverip, port
from logger import *

def test_connection():
    """
    Проверяет доступность сервера, отправляя тестовый запрос.
    
    Returns:
        bool: True если сервер доступен, False в противном случае
    """
    try:
        # Создаем соединение с сервером
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Устанавливаем таймаут на соединение, чтобы не ждать долго
            client_socket.settimeout(3)
            client_socket.connect((serverip, port))
            
            # Отправляем тестовый JSON-запрос
            test_data = {"type": "test"}
            client_socket.sendall(json.dumps(test_data).encode('utf-8'))
            
            # Получаем ответ от сервера
            response_data = b""
            while True:
                chunk = client_socket.recv(4096)
                if not chunk:  # Если данных больше нет, выходим из цикла
                    break
                response_data += chunk

            # Любой ответ от сервера считаем успешным
            log_event("Сервер доступен")
            return True
    except (socket.error, socket.timeout) as e:
        log_error(f"Ошибка при подключении к серверу: {e}")
        return False
    except Exception as e:
        log_error(f"Непредвиденная ошибка: {e}")
        return False


def database(request_data):
    """
    Устаревшая функция для синхронного запроса к базе данных.
    Рекомендуется использовать DbWorker для асинхронных запросов.
    """
    log_event(f"Запрос: {request_data}")
    if request_data['type'] == 'report':
        return "OK"
    elif request_data['type'] == 'user':
        return {"status": "ok", "surname": "Степанов", "name": "Сергей"}
    elif request_data['type'] == 'details':
        return {'status': 'ok', 'data': {'id': 69, 'name': 'МЕТРАН 150', 'serial_number': 'SN904', 'defective': False, 'stage': 'Сборка', 'sector': None, 'identified_by': None, 'defect_stage_id': None}}
    # try:
    #     # Создаем соединение с сервером
    #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    #         client_socket.connect((serverip, port))
            
    #         # Отправляем JSON-запрос
    #         client_socket.sendall(json.dumps(request_data).encode('utf-8'))
            
    #         # Получаем полный ответ от сервера
    #         response_data = b""
    #         while True:
    #             chunk = client_socket.recv(4096)
    #             if not chunk:  # Если данных больше нет, выходим из цикла
    #                 break
    #             response_data += chunk

    #         response = response_data.decode('utf-8')
    #         try:
    #             worker = json.loads(response)
    #             log_event(f"Ответ: {worker}")
    #             return worker  # Возвращаем объект Python (словарь)
    #         except json.JSONDecodeError:
    #             log_error(f"Ошибка декодирования JSON: {response}")
    #             return None
    # except (socket.error, socket.timeout) as e:
    #     log_error(f"Ошибка при подключении к серверу: {e}")
    #     return None
    # except Exception as e:
    #     log_error(f"Непредвиденная ошибка: {e}")
    #     return None
