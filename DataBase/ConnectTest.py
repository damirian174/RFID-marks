import psycopg2

# Параметры подключения к серверу PostgreSQL
conn_params = {
    "dbname": "main",  # Подключаемся к базе данных test
    "user": "dytt",  # Имя пользователя
    "password": "dyttadmin",  # Пароль
    "host": "109.191.82.85",  # Адрес сервера (можно заменить на IP-адрес сервера)
    "port": 5432  # Порт PostgreSQL
}

try:
    # Подключаемся к базе данных
    conn = psycopg2.connect(**conn_params)
    conn.autocommit = True

    # Создаём курсор
    cur = conn.cursor()

    # SQL-запрос для извлечения всех данных из таблицы
    select_query = "SELECT * FROM details"y
    cur.execute(select_query)

    # Получение всех строк из результата
    rows = cur.fetchall()
    print(rows)

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
