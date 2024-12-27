import psycopg2
import datetime

# Запрашиваем у пользователя параметры подключения
print("Введите параметры подключения к PostgreSQL:")
database_name = input("Имя базы данных: ")
user = input("Имя пользователя: ")
password = input("Пароль: ")
host = input("Адрес сервера (по умолчанию localhost): ") or "localhost"
port = input("Порт (по умолчанию 5432): ") or "5432"

# Параметры подключения к серверу PostgreSQL
conn_params = {
    "dbname": database_name,
    "user": user,
    "password": password,
    "host": host,
    "port": port
}

try:
    # Подключаемся к базе данных
    conn = psycopg2.connect(**conn_params)
    conn.autocommit = True

    # Создаём курсор
    cur = conn.cursor()

    # SQL-запрос для извлечения всех данных из таблицы
    select_query = "SELECT * FROM employees;"
    cur.execute(select_query)

    # Получение всех строк из результата
    rows = cur.fetchall()

    # Печать данных
    print("Данные в таблице:")
    for row in rows:
        # Преобразуем дату в строку
        formatted_row = tuple(
            str(item) if isinstance(item, (datetime.date, datetime.datetime)) else item
            for item in row
        )
        print(formatted_row)

except psycopg2.OperationalError as e:
    print(f"Ошибка подключения: {e}")
except psycopg2.Error as e:
    print(f"Ошибка PostgreSQL: {e}")
except Exception as e:
    print(f"Неизвестная ошибка: {e}")
finally:
    # Закрываем курсор и соединение, если они были созданы
    if 'cur' in locals() and cur:
        cur.close()
        print("Курсор закрыт.")
    if 'conn' in locals() and conn:
        conn.close()
        print("Соединение закрыто.")
