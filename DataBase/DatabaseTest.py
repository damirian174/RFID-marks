import psycopg2
from psycopg2 import sql

# Параметры подключения к серверу PostgreSQL
conn_params = {
    "dbname": "postgres",  # Подключаемся к базе данных postgres для создания новой базы
    "user": "postgres",    # Имя пользователя
    "password": "Пороль при установке Postgres",  # Пароль
    "host": "localhost",   # Адрес сервера (можно заменить на IP-адрес сервера)
    "port": 5432           # Порт PostgreSQL
}

# Имя создаваемой базы данных
new_database_name = "new_database"

# Инициализация переменной conn
conn = None

try:
    # Шаг 1: Подключаемся к базе данных postgres
    conn = psycopg2.connect(**conn_params)
    conn.autocommit = True  # Включаем автокоммит
    with conn.cursor() as cursor:
        # Создаём базу данных
        cursor.execute(
            sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(new_database_name)
            )
        )
        print(f"База данных '{new_database_name}' успешно создана.")
    conn.close()  # Закрываем соединение с базой данных "postgres"

    # Шаг 2: Подключаемся к созданной базе данных
    conn_params['dbname'] = new_database_name  # Обновляем параметры на новую базу данных
    conn = psycopg2.connect(**conn_params)
    with conn.cursor() as cursor:
        # Проверим подключение к новой базе
        cursor.execute("SELECT current_database();")
        print(f"Подключились к базе данных: {cursor.fetchone()[0]}")

    # Шаг 3: Настройка доступов для удаленных пользователей
    # Теперь пользователи могут подключиться, используя свои учетные данные и IP-адрес сервера
    print("Теперь другие компьютеры могут подключиться к базе данных по IP-адресу сервера.")

except psycopg2.Error as e:
    print(f"Ошибка при создании базы данных или подключении к ней: {e}")
finally:
    if conn:
        conn.close()  # Закрываем соединение после использования
