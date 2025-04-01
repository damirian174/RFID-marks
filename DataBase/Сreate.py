import asyncpg
import asyncio
import uuid

async def generate_unique_uid(conn):
    new_uid = str(uuid.uuid4())[:13]

    while await conn.fetchval("SELECT COUNT(*) FROM users WHERE uid = $1", new_uid) > 0:
        new_uid = str(uuid.uuid4())[:13]

    return new_uid

async def create_and_insert_data():

    
    try:


        # Теперь подключаемся к базе данных main
        conn = await asyncpg.connect(
            user='dytt',
            password='dyttadmin',
            database='main',
            host='192.168.0.100',
            port=5432
        )

        # Создаем таблицы в правильном порядке
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                surname VARCHAR(100) NOT NULL,
                profession VARCHAR(100) NOT NULL,
                uid VARCHAR(13) NOT NULL UNIQUE
            );
        """)

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
            CREATE TABLE IF NOT EXISTS sensors (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                pressure_pa NUMERIC,
                temperature NUMERIC,
                form_factor VARCHAR(50)
            );
        """)

        await conn.execute("""
            CREATE TABLE IF NOT EXISTS details (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                serial_number VARCHAR(100) NOT NULL UNIQUE,
                defective BOOLEAN DEFAULT FALSE,
                stage VARCHAR(50),
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
                CONSTRAINT fk_details_ready FOREIGN KEY (serial_name) REFERENCES details (serial_number) ON DELETE CASCADE
            );
        """)

        await conn.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                text TEXT NOT NULL,
                time TEXT NOT NULL
            );
        """)

        await conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                start_time TEXT,
                work_description TEXT,
                status TEXT DEFAULT 'active',
                notes TEXT
            );
        """)

        print("База данных и таблицы успешно созданы.")
    except Exception as e:
        print(f"Ошибка при создании базы данных и таблиц: {e}")
    finally:
        await conn.close()

asyncio.run(create_and_insert_data())
