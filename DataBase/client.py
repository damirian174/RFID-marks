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
    SERVER_HOST = "194.48.250.96"
    SERVER_PORT = 12345
    
    # Тестовый запрос на получение пользователя по UID
    users = [
        {
            "type": "addUser",
            "name": "Иван",
            "surname": "Иванов",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Алексей",
            "surname": "Петров",
            "prof": "Программист"
        },
        {
            "type": "addUser",
            "name": "Николай",
            "surname": "Сидоров",
            "prof": "Менеджер"
        },
        {
            "type": "addUser",
            "name": "Сергей",
            "surname": "Кузнецов",
            "prof": "Бухгалтер"
        },
        {
            "type": "addUser",
            "name": "Андрей",
            "surname": "Михайлов",
            "prof": "Маркетолог"
        }
    ]

    
    # Выполнение запросов
    print("=== Тест: Получение пользователя ===")
    for i in users:
        test_server(SERVER_HOST, SERVER_PORT, i)
        
    
