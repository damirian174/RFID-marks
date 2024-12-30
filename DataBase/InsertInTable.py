import asyncpg
import asyncio

async def insert_data():
    conn = await asyncpg.connect(
        user='dytt',
        password='dyttadmin',
        database='main',
        host='192.168.3.14',  # IP Raspberry Pi
        port=5432
    )
    
    try:
        # Добавление пользователя
        user_id = await conn.fetchval("""
            INSERT INTO users (name, surname, profession)
            VALUES ('Боб', 'Смит', 'Техник')
            RETURNING id;
        """)
        print(f"Пользователь добавлен с ID: {user_id}")

        # Добавление детали, связанной с пользователем
        detail_id = await conn.fetchval("""
            INSERT INTO details (user_id, name, serial_number, defective, stage, pressure_pa, temperature, form_factor)
            VALUES ($1, 'Компонент B', 'SN002', FALSE, 'Сборка', 101000, 20.5, 'Квадратный')
            RETURNING id;
        """, user_id)
        print(f"Деталь добавлена с ID: {detail_id}")

        # Добавление этапа, связанного с деталью
        stage_id = await conn.fetchval("""
            INSERT INTO stage (detail_id, name, serial_number, time_start)
            VALUES ($1, 'Контроль качества', 'SN002', NOW())
            RETURNING id;
        """, detail_id)
        print(f"Этап добавлен с ID: {stage_id}")

        # Добавление готовой части, связанной с деталью
        ready_part_id = await conn.fetchval("""
            INSERT INTO ready_parts (detail_id, name, serial_name)
            VALUES ($1, 'Готовый компонент B', 'Ready_SN002')
            RETURNING id;
        """, detail_id)
        print(f"Готовая часть добавлена с ID: {ready_part_id}")

        print("Все данные успешно добавлены.")

    except Exception as e:
        print(f"Ошибка при добавлении данных: {e}")
    finally:
        await conn.close()

# Запуск функции
asyncio.run(insert_data())
