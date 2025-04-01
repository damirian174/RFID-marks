import socket
import json

def test_server(host, port, request_data):
    """Функция для отправки запроса и получения ответа от сервера."""
    try:
        # Создаем соединение с сервером
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            
            # Отправляем JSON-запрос
            client_socket.sendall(json.dumps(request_data).encode('utf-8'))
            
            # Получаем ответ от сервера
            response = client_socket.recv(4096).decode('utf-8')
            
            # Выводим ответ сервера
            print(f"Запрос: {request_data}")
            print(f"Ответ: {response}")
    except Exception as e:
        print(f"Ошибка при подключении к серверу: {e}")

if __name__ == "__main__":
    SERVER_HOST = "192.168.0.100"
    SERVER_PORT = 12345
    
    # Тестовый запрос на получение пользователя по UID
    users = [
        {
            "type": "getreports"
        }
    ]

    
    # Выполнение запросов
    print("=== Тест: Получение пользователя ===")
    for i in users:
        test_server(SERVER_HOST, SERVER_PORT, i)
        
    
