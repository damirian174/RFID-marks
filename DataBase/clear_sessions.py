import asyncio
import asyncpg

async def clear_all_sessions():
    """
    Очистка всех сессий из базы данных.
    """
    try:
        conn = await asyncpg.connect(
            user='dytt',
            password='dyttadmin',
            database='main',
            host='192.168.0.100'
        )
        
        await conn.execute("DELETE FROM sessions;")
        print("Все сессии успешно удалены")
        
    except Exception as e:
        print(f"Ошибка при удалении сессий: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(clear_all_sessions()) 