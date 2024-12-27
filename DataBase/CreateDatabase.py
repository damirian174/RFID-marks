import psycopg2
from psycopg2 import sql

# Запрашиваем у пользователя параметры подключения
print("Введите параметры подключения к PostgreSQL для администратора:")
admin_user = input("Имя администратора: ")
admin_password = input("Пароль администратора: ")
host = input("Адрес сервера (по умолчанию localhost): ") or "localhost"
port = input("Порт (по умолчанию 5432): ") or "5432"

# Запрашиваем данные для нового пользователя
print("\nВведите данные для нового пользователя:")
new_user = input("Имя нового пользователя: ")
new_password = input("Пароль нового пользователя: ")

# Запрашиваем имя создаваемой базы данных
new_database_name = input("\nВведите имя создаваемой базы данных: ")

# Параметры подключения для администратора
admin_conn_params = {
    "dbname": "postgres",  # Подключаемся к базе данных postgres для управления пользователями и базами
    "user": admin_user,
    "password": admin_password,
    "host": host,
    "port": port
}

# Инициализация переменной conn
conn = None

try:
    # Шаг 1: Подключаемся к базе данных postgres как администратор
    conn = psycopg2.connect(**admin_conn_params)
    conn.autocommit = True  # Включаем автокоммит
    with conn.cursor() as cursor:
        # Создаём нового пользователя
        cursor.execute(
            sql.SQL("CREATE USER {} WITH PASSWORD %s").format(
                sql.Identifier(new_user)
            ),
            [new_password]
        )
        print(f"Пользователь '{new_user}' успешно создан.")
        
        # Назначаем привилегии на создание баз данных
        cursor.execute(
            sql.SQL("ALTER USER {} CREATEDB").format(
                sql.Identifier(new_user)
            )
        )
        print(f"Пользователю '{new_user}' даны права на создание баз данных.")

    conn.close()  # Закрываем соединение с базой данных "postgres"

    # Шаг 2: Подключаемся как новый пользователь и создаём базу данных
    new_user_conn_params = {
        "dbname": "postgres",
        "user": new_user,
        "password": new_password,
        "host": host,
        "port": port
    }
    conn = psycopg2.connect(**new_user_conn_params)
    conn.autocommit = True  # Включаем автокоммит
    with conn.cursor() as cursor:
        # Создаём базу данных от имени нового пользователя
        cursor.execute(
            sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(new_database_name)
            )
        )
        print(f"База данных '{new_database_name}' успешно создана от имени пользователя '{new_user}'.")
        
except psycopg2.Error as e:
    print(f"Ошибка: {e}")
finally:
    if conn:
        conn.close()  # Закрываем соединение после использования
