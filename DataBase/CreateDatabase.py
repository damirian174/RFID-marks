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
        # Проверка, существует ли уже пользователь
        cursor.execute(
            sql.SQL("SELECT 1 FROM pg_roles WHERE rolname = %s"),
            [new_user]
        )
        if cursor.fetchone():
            print(f"Пользователь '{new_user}' уже существует.")
        else:
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

        # Проверка, существует ли уже база данных
        cursor.execute(
            sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"),
            [new_database_name]
        )
        if cursor.fetchone():
            print(f"База данных '{new_database_name}' уже существует.")
        else:
            # Создаём базу данных с владельцем new_user
            cursor.execute(
                sql.SQL("CREATE DATABASE {} OWNER {}").format(
                    sql.Identifier(new_database_name),
                    sql.Identifier(new_user)
                )
            )
            print(f"База данных '{new_database_name}' успешно создана с владельцем '{new_user}'.")

    conn.close()  # Закрываем соединение с базой данных "postgres"

except psycopg2.Error as e:
    print(f"Ошибка: {e}")
finally:
    if conn:
        conn.close()  # Закрываем соединение после использования
