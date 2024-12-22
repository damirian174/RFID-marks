import psycopg2
import datetime  # type: ignore # Добавляем импорт встроенного модуля datetime


# Имя базы данных к которой подключаемся
new_database_name = "test"

# Параметры подключения
conn_params = {
    "dbname": new_database_name,  # Подключаемся к базе данных
    "user": "postgres",    # Имя пользователя
    "password": "Пороль при установке Postgres",  # Пароль
    "host": "localhost",   # Адрес сервера
    "port": 5432           # Порт PostgreSQL
}
conn = psycopg2.connect(**conn_params)

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

try:
    # Подключаемся к базе данных
    conn = psycopg2.connect(**conn_params)
    conn.autocommit = True

    # Создаём курсор
    cur = conn.cursor()

    # Создание таблицы
    cur.execute(create_table_query)
    print("Таблица 'employees' создана или уже существует")

    # Данные для вставки
    employee_data = [
        ('John Doe', 'Software Engineer', '2024-01-01'),
        ('Jane Doe', 'Data Analyst', '2022-01-05'),
        ('Walter White', 'Chemist', '2010-04-23'),
        ('Am Test', "Test", '2024-12-22')
    ]

    # Вставка данных с проверкой на уникальность
    insert_query = """
        INSERT INTO employees (name, position, hire_date)
        VALUES (%s, %s, %s)
        ON CONFLICT (name, position, hire_date) DO NOTHING;
    """
    cur.executemany(insert_query, employee_data)
    print("Данные вставлены")

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

except psycopg2.Error as e:
    print(f"Ошибка: {e}")
finally:
    # Закрытие соединения
    if cur:
        cur.close()
    if conn:
        conn.close()