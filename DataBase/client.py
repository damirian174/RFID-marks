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
            "type": "addUser",
            "name": "Иван",
            "surname": "Иванов",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Петр", 
            "surname": "Петров",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Сергей",
            "surname": "Сергеев", 
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Александр",
            "surname": "Александров",
            "prof": "Инженер"
        },
        {
            "type": "addUser", 
            "name": "Михаил",
            "surname": "Михайлов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Николай",
            "surname": "Николаев",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Дмитрий",
            "surname": "Дмитриев",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Андрей",
            "surname": "Андреев",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Владимир",
            "surname": "Владимиров",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Юрий",
            "surname": "Юрьев",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Виктор",
            "surname": "Викторов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Олег",
            "surname": "Олегов",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Павел",
            "surname": "Павлов",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Роман",
            "surname": "Романов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Борис",
            "surname": "Борисов",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Григорий",
            "surname": "Григорьев",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Евгений",
            "surname": "Евгеньев",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Константин",
            "surname": "Константинов",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Леонид",
            "surname": "Леонидов",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Максим",
            "surname": "Максимов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Руслан",
            "surname": "Русланов",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Станислав",
            "surname": "Станиславов",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Тимофей",
            "surname": "Тимофеев",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Федор",
            "surname": "Федоров",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Эдуард",
            "surname": "Эдуардов",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Ярослав",
            "surname": "Ярославов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Антон",
            "surname": "Антонов",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Валерий",
            "surname": "Валерьев",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Геннадий",
            "surname": "Геннадьев",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Денис",
            "surname": "Денисов",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Егор",
            "surname": "Егоров",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Захар",
            "surname": "Захаров",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Игорь",
            "surname": "Игорев",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Кирилл",
            "surname": "Кириллов",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Лев",
            "surname": "Львов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Марк",
            "surname": "Марков",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Никита",
            "surname": "Никитин",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Олег",
            "surname": "Олегов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Платон",
            "surname": "Платонов",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Родион",
            "surname": "Родионов",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Семен",
            "surname": "Семенов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Тарас",
            "surname": "Тарасов",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Ульян",
            "surname": "Ульянов",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Филипп",
            "surname": "Филиппов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Харитон",
            "surname": "Харитонов",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Цезарь",
            "surname": "Цезарев",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Чеслав",
            "surname": "Чеславов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Шамиль",
            "surname": "Шамилев",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Эльдар",
            "surname": "Эльдаров",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Юлиан",
            "surname": "Юлианов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Яков",
            "surname": "Яковлев",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Артем",
            "surname": "Артемов",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Богдан",
            "surname": "Богданов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Вадим",
            "surname": "Вадимов",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Глеб",
            "surname": "Глебов",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Давид",
            "surname": "Давидов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Елисей",
            "surname": "Елисеев",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Жорж",
            "surname": "Жоржев",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Зиновий",
            "surname": "Зиновьев",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Иннокентий",
            "surname": "Иннокентьев",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Казимир",
            "surname": "Казимиров",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Лаврентий",
            "surname": "Лаврентьев",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Макар",
            "surname": "Макаров",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Назар",
            "surname": "Назаров",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Оскар",
            "surname": "Оскаров",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Прохор",
            "surname": "Прохоров",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Радий",
            "surname": "Радиев",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Савва",
            "surname": "Саввин",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Тихон",
            "surname": "Тихонов",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Устин",
            "surname": "Устинов",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Фрол",
            "surname": "Фролов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Христофор",
            "surname": "Христофоров",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Цезарь",
            "surname": "Цезарев",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Чеслав",
            "surname": "Чеславов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Шамиль",
            "surname": "Шамилев",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Эмиль",
            "surname": "Эмильев",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Юстин",
            "surname": "Юстинов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Ян",
            "surname": "Янов",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Аркадий",
            "surname": "Аркадьев",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Бронислав",
            "surname": "Брониславов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Валентин",
            "surname": "Валентинов",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Гавриил",
            "surname": "Гавриилов",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Даниил",
            "surname": "Даниилов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Евстафий",
            "surname": "Евстафьев",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Жан",
            "surname": "Жанов",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Зенон",
            "surname": "Зенонов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Илларион",
            "surname": "Илларионов",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Клим",
            "surname": "Климов",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Лукьян",
            "surname": "Лукьянов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Матвей",
            "surname": "Матвеев",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Наум",
            "surname": "Наумов",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Остап",
            "surname": "Остапов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Пантелей",
            "surname": "Пантелеев",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Рафаил",
            "surname": "Рафаилов",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Святослав",
            "surname": "Святославов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Трофим",
            "surname": "Трофимов",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Феликс",
            "surname": "Феликсов",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Харлампий",
            "surname": "Харлампиев",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Эраст",
            "surname": "Эрастов",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Юрий",
            "surname": "Юрьев",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Яромир",
            "surname": "Яромиров",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Аристарх",
            "surname": "Аристархов",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Болеслав",
            "surname": "Болеславов",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Вениамин",
            "surname": "Вениаминов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Герман",
            "surname": "Германов",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Демьян",
            "surname": "Демьянов",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Ермолай",
            "surname": "Ермолаев",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Захарий",
            "surname": "Захарьев",
            "prof": "Оператор"
        },
        {
            "type": "addUser",
            "name": "Измаил",
            "surname": "Измаилов",
            "prof": "Инженер"
        },
        {
            "type": "addUser",
            "name": "Карл",
            "surname": "Карлов",
            "prof": "Техник"
        },
        {
            "type": "addUser",
            "name": "Леонтий",
            "surname": "Леонтьев",
            "prof": "Оператор"
        }
    ]

    
    # Выполнение запросов
    print("=== Тест: Получение пользователя ===")
    for i in users:
        test_server(SERVER_HOST, SERVER_PORT, i)
        
    
