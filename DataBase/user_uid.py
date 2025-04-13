import asyncpg
import asyncio

async def fetch_users(conn):
    try:
        rows = await conn.fetch("SELECT * FROM users")
        for row in rows:
            print(row['id'], row['name'], row['surname'], row['uid'])
    except Exception as e:
        print(f"Error fetching users: {e}")

async def insert_test_data(serial_number):
    conn = None
    try:
        conn = await asyncpg.connect(
            user='dytt',
            password='dyttadmin',
            database='main',
            host='localhost',  # IP Raspberry Pi
            port=5432
        )

        await fetch_users(conn)

    except Exception as e:
        print(f"Error connecting to database: {e}")
    
    finally:
        if conn:
            await conn.close()

asyncio.run(insert_test_data(1))
