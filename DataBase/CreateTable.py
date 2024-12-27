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

# SQL-запрос для создания таблицы
create_table_query = """
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    position VARCHAR(100),
    hire_date DATE DEFAULT CURRENT_DATE,
    CONSTRAINT unique_employee UNIQUE (name, position, hire_date)
);
"""

# SQL-запрос для вставки или обновления данных
insert_or_update_query = """
    INSERT INTO employees (name, position, hire_date)
    VALUES (%s, %s, %s)
    ON CONFLICT (name, position, hire_date) 
    DO UPDATE SET 
        name = EXCLUDED.name, 
        position = EXCLUDED.position,
        hire_date = EXCLUDED.hire_date;
"""

try:
    # Подключаемся к базе данных
    conn = psycopg2.connect(**conn_params)
    conn.autocommit = True

    # Создаём курсор
    cur = conn.cursor()

    # Создаём таблицу, если её ещё нет
    cur.execute(create_table_query)
    print("Таблица 'employees' создана или уже существует.")

    # Ввод данных вручную
    print("\nВведите данные для добавления в таблицу. Чтобы завершить, введите 'stop'.")

    while True:
        name = input("Имя сотрудника (или 'stop' для завершения): ")
        if name.lower() == "stop":
            break
        position = input("Должность: ")
        hire_date = input("Дата найма (YYYY-MM-DD, или пусто для текущей даты): ") or None

        # Вставляем или обновляем данные в таблицу
        cur.execute(insert_or_update_query, (name, position, hire_date))
        print(f"Данные сотрудника {name} добавлены или обновлены.")

    # Вывод всех данных из таблицы
    select_query = "SELECT * FROM employees;"
    cur.execute(select_query)
    rows = cur.fetchall()

    print("\nДанные в таблице 'employees':")
    for row in rows:
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
