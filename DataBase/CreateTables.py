import asyncpg
import asyncio

async def create_users_table():
    conn = await asyncpg.connect(
        user='dytt',
        password='dyttadmin',
        database='main',
        host='192.168.3.14',  # IP Raspberry Pi
        port=5432
    )
    
    try:
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
                serial_number VARCHAR(100) NOT NULL,
                defective BOOLEAN DEFAULT FALSE,
                stage VARCHAR(50),
                pressure_pa NUMERIC,
                temperature NUMERIC,
                form_factor VARCHAR(50),
                sector VARCHAR(100) DEFAULT NULL
            );
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS stage (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                serial_number VARCHAR(100) NOT NULL,
                time_start TIMESTAMP NOT NULL,
                time_end TIMESTAMP DEFAULT NULL
            );
        """)
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        await conn.close()

# Run the coroutine
asyncio.run(create_users_table())
