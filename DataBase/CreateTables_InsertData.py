import asyncpg
import asyncio

async def create_and_insert_data():
    conn = await asyncpg.connect(
        user='dytt',
        password='dyttadmin',
        database='main',
        host='109.191.82.85',
        port=5432
    )
    
    try:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS stage (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                serial_number VARCHAR(100) NOT NULL,
                time_start TIMESTAMP NOT NULL,
                time_end TIMESTAMP DEFAULT NULL,
                responsible_user INT DEFAULT NULL,
                CONSTRAINT fk_users_stage FOREIGN KEY (responsible_user) REFERENCES users (id) ON DELETE SET NULL
            );
        """)

        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                surname VARCHAR(100) NOT NULL,
                profession VARCHAR(100) NOT NULL
            );
        """)

        await conn.execute("""
            CREATE TABLE IF NOT EXISTS details (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                serial_number VARCHAR(100) NOT NULL UNIQUE,
                defective BOOLEAN DEFAULT FALSE,
                stage VARCHAR(50),
                pressure_pa NUMERIC,
                temperature NUMERIC,
                form_factor VARCHAR(50),
                sector VARCHAR(100) DEFAULT NULL,
                identified_by INT DEFAULT NULL,
                defect_stage_id INT DEFAULT NULL,
                CONSTRAINT fk_users_details FOREIGN KEY (identified_by) REFERENCES users (id) ON DELETE SET NULL,
                CONSTRAINT fk_stage_defects FOREIGN KEY (defect_stage_id) REFERENCES stage (id) ON DELETE SET NULL
            );
        """)

        await conn.execute("""
            CREATE TABLE IF NOT EXISTS ready_parts (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                serial_name VARCHAR(100) NOT NULL,
                created_by INT NOT NULL,
                CONSTRAINT fk_details_ready FOREIGN KEY (serial_name) REFERENCES details (serial_number) ON DELETE CASCADE,
                CONSTRAINT fk_users_creator FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL
            );
        """)

        await conn.execute("""
            CREATE TABLE IF NOT EXISTS operations (
                id SERIAL PRIMARY KEY,
                user_id INT NOT NULL,
                action VARCHAR(255) NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                related_part INT DEFAULT NULL,
                CONSTRAINT fk_users_operations FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                CONSTRAINT fk_parts_operations FOREIGN KEY (related_part) REFERENCES ready_parts (id) ON DELETE CASCADE
            );
        """)

        await conn.execute("""
            INSERT INTO users (name, surname, profession) VALUES
            ('Иван', 'Иванов', 'Инженер'),
            ('Анна', 'Петрова', 'Техник'),
            ('Олег', 'Сидоров', 'Контролёр');
        """)

        await conn.execute("""
            INSERT INTO stage (name, serial_number, time_start, time_end, responsible_user) VALUES
            ('Сборка', 'SN001', '2025-01-01 09:00:00', '2025-01-01 12:00:00', 1),
            ('Тестирование', 'SN002', '2025-01-01 13:00:00', NULL, 2),
            ('Контроль', 'SN003', '2025-01-02 10:00:00', NULL, 3);
        """)

        await conn.execute("""
            INSERT INTO details (name, serial_number, defective, stage, pressure_pa, temperature, form_factor, sector, identified_by, defect_stage_id) VALUES
            ('Деталь А', 'SN001', FALSE, 'Сборка', 101325, 25, 'Квадрат', 'Сектор 1', NULL, NULL),
            ('Деталь Б', 'SN002', TRUE, 'Тестирование', 101325, 30, 'Круг', 'Сектор 2', 2, 2),
            ('Деталь В', 'SN003', FALSE, 'Сборка', 100000, 20, 'Треугольник', 'Сектор 1', NULL, 3);
        """)

        await conn.execute("""
            INSERT INTO ready_parts (name, serial_name, created_by) VALUES
            ('Готовая деталь А', 'SN001', 1),
            ('Готовая деталь Б', 'SN003', 2);
        """)

        await conn.execute("""
            INSERT INTO operations (user_id, action, timestamp, related_part) VALUES
            (1, 'Создание детали', '2025-01-01 09:00:00', 1),
            (2, 'Обнаружение дефекта', '2025-01-01 13:30:00', NULL),
            (3, 'Создание готовой детали', '2025-01-02 11:00:00', 2);
        """)

        print("Таблицы и тестовые данные успешно созданы.")
    except Exception as e:
        print(f"Ошибка при создании таблиц и добавлении тестовых данных: {e}")
    finally:
        await conn.close()

asyncio.run(create_and_insert_data())
