import asyncpg
import asyncio

async def fetch_related_data():
    conn = await asyncpg.connect(
        user='dytt',
        password='dyttadmin',
        database='main',
        host='192.168.3.14',  # IP Raspberry Pi
        port=5432
    )
    
    try:
        # Выполняем запрос для получения связанных данных
        query = """
        SELECT 
            users.name AS user_name,
            users.surname AS user_surname,
            details.name AS detail_name,
            details.serial_number AS detail_serial,
            stage.name AS stage_name,
            stage.time_start AS stage_start_time,
            ready_parts.name AS ready_part_name,
            ready_parts.serial_name AS ready_serial_name
        FROM 
            details
        LEFT JOIN 
            users ON details.user_id = users.id
        LEFT JOIN 
            stage ON stage.detail_id = details.id
        LEFT JOIN 
            ready_parts ON ready_parts.detail_id = details.id;
        """
        results = await conn.fetch(query)

        # Форматируем и выводим результаты
        for record in results:
            print(f"""
            User: {record['user_name']} {record['user_surname']}
            Detail: {record['detail_name']} (Serial: {record['detail_serial']})
            Stage: {record['stage_name']} (Start Time: {record['stage_start_time']})
            Ready Part: {record['ready_part_name']} (Serial: {record['ready_serial_name']})
            """)
    except Exception as e:
        print(f"Error fetching related data: {e}")
    finally:
        await conn.close()

# Запускаем функцию
asyncio.run(fetch_related_data())
