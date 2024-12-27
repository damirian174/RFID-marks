import psycopg2
import datetime  # type: ignore

# Параметры подключения к серверу PostgreSQL
conn_params = {
    "dbname": "",  # Подключаемся к базе данных test
    "user": "",  # Имя пользователя
    "password": "",  # Пароль
    "host": "",  # Адрес сервера (можно заменить на IP-адрес сервера)
    "port": 5432  # Порт PostgreSQL
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
