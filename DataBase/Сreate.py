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
                time JSONB NOT NULL,
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

        await conn.execute("""
            CREATE TABLE IF NOT EXISTS storage_sectors (
                id SERIAL PRIMARY KEY,
                sector_name VARCHAR(10) NOT NULL,
                occupied_slots INTEGER DEFAULT 0,
                max_capacity INTEGER DEFAULT 5
            );
        """)

        # Таблица для информации о компании (whitepaper)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS company_info (
                id SERIAL PRIMARY KEY,
                company_name VARCHAR(255) NOT NULL,
                inn VARCHAR(12) NOT NULL UNIQUE,
                logo_path VARCHAR(500) DEFAULT NULL,
                description TEXT DEFAULT NULL,
                address TEXT DEFAULT NULL,
                phone VARCHAR(50) DEFAULT NULL,
                email VARCHAR(100) DEFAULT NULL,
                website VARCHAR(255) DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Таблица для производственных продуктов (whitepaper)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                product_name VARCHAR(255) NOT NULL,
                product_code VARCHAR(100) NOT NULL UNIQUE,
                category VARCHAR(100) NOT NULL,
                description TEXT DEFAULT NULL,
                specifications JSONB DEFAULT NULL,
                price DECIMAL(10,2) DEFAULT NULL,
                currency VARCHAR(3) DEFAULT 'RUB',
                production_capacity INTEGER DEFAULT NULL,
                unit_of_measure VARCHAR(50) DEFAULT 'шт',
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        print("База данных и таблицы успешно созданы.")
    except Exception as e:
        print(f"Ошибка при создании базы данных и таблиц: {e}")
    finally:
        await conn.close()

asyncio.run(create_and_insert_data())
