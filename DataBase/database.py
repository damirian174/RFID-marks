import asyncpg
import random
import datetime
import time

async def generate_unique_uid(pool):
    """
    Генерация уникального UID с использованием пула соединений.
    """
    number = random.randint(1, 999999999)
    
    # Преобразуем число в строку и добавляем ведущие нули, чтобы длина была равна 13 символам
    formatted_number = f"{number:009}"
    
    async with pool.acquire() as conn:
        while await conn.fetchval("SELECT COUNT(*) FROM users WHERE uid = $1", formatted_number) > 0:
            number = random.randint(1, 999999999)
            formatted_number = f"{number:009}"

    return formatted_number

DB_SETTINGS = {
    "user": "dytt",
    "password": "dyttadmin",
    "database": "main",
    "host": "localhost",
    "port": 5432,
}

# Создание пула соединений
async def create_pool():
    return await asyncpg.create_pool(
        **DB_SETTINGS,
        min_size=1,
        max_size=10,
        command_timeout=60
    )

async def get_details_by_serial(pool, serial):
    try:
        async with pool.acquire() as conn:
            query = "SELECT * FROM details WHERE serial_number = $1;"
            detail = await conn.fetchrow(query, serial)
            if detail:
                return detail
            return None
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None

# Получение пользователя по UID
async def get_user_by_uid(pool, uid):
    try:
        async with pool.acquire() as conn:
            # Получаем данные пользователя
            query = "SELECT id, name, surname FROM users WHERE uid = $1;"
            user = await conn.fetchrow(query, uid)
            if not user:
                return None

            # Проверяем наличие активной сессии
            session_query = """
                SELECT COUNT(*) 
                FROM sessions 
                WHERE user_id = $1 AND status = 'active';
            """
            active_sessions = await conn.fetchval(session_query, user["id"])
            
            if active_sessions > 0:
                return {
                    "name": user["name"],
                    "surname": user["surname"],
                    "has_active_session": True
                }
            
            return {
                "name": user["name"],
                "surname": user["surname"],
                "has_active_session": False
            }
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None

async def get_user_id_by_name(pool, name, surname):
    """
    Получение ID пользователя по имени и фамилии.
    """
    try:
        async with pool.acquire() as conn:
            query = "SELECT id FROM users WHERE name = $1 AND surname = $2;"
            user = await conn.fetchrow(query, name, surname)
            if user:
                return user["id"]
            return None
    except Exception as e:
        print(f"Ошибка при получении ID пользователя: {e}")
        return None

async def get_user_name_by_id(pool, user_id):
    """
    Получение имени и фамилии пользователя по ID.
    """
    try:
        async with pool.acquire() as conn:
            query = "SELECT name, surname FROM users WHERE id = $1;"
            user = await conn.fetchrow(query, user_id)
            if user:
                return {"name": user["name"], "surname": user["surname"]}
            return None
    except Exception as e:
        print(f"Ошибка при получении имени пользователя: {e}")
        return None

async def addUserInDb(pool, name, surname, prof):
    try:
        async with pool.acquire() as conn:
            query = "INSERT INTO users (name, surname, profession, uid) VALUES ($1, $2, $3, $4);"
            await conn.execute(query, name, surname, prof, await generate_unique_uid(pool))
            return "OK"
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return e
        
async def addDetail(pool, detail):
    try:
        async with pool.acquire() as conn:
            query = "INSERT INTO details (name, pressure_pa, temperature, form_factor) VALUES ($1, $2, $3, $4);"
            await conn.execute(query, detail["name"], detail["pressure_pa"], detail["temperature"], detail["form_factor"])
            return "OK"
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return e
        
async def getDetails(pool, detail):
    # получение всех деталей где модель равана detail
    try:
        async with pool.acquire() as conn:
            query = "SELECT * FROM details WHERE name = $1;"
            details = await conn.fetch(query, detail)
            if details:
                return details
            return None
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None
        
async def allusers(pool, detail): 
    # получение всех деталей где модель равана detail 
    try: 
        async with pool.acquire() as conn: 
            query = "SELECT * FROM users" 
            users = await conn.fetch(query) 
            if users: 
                return users 
            return None 
    except Exception as e: 
        print(f"Ошибка при выполнении запроса: {e}") 
        return None

async def add_sensor(pool, name, serial_number):
    """
    Добавление датчика с указанием названия и серийного номера.
    """
    try:
        async with pool.acquire() as conn:
            query = """
                INSERT INTO details (name, serial_number, stage)
                VALUES ($1, $2, $3);
            """
            await conn.execute(query, name, serial_number, "Маркировка")
            return "OK"
    except Exception as e:
        print(f"Ошибка при добавлении датчика: {e}")
        return e

async def update_stage_by_serial(pool, serial_number, new_stage):
    """
    Изменение stage по серийному номеру.
    """
    try:
        async with pool.acquire() as conn:
            query = """
                UPDATE details
                SET stage = $1
                WHERE serial_number = $2;
            """
            await conn.execute(query, new_stage, serial_number)
            return "OK"
    except Exception as e:
        print(f"Ошибка при изменении stage: {e}")
        return e


async def get_defective_counts(pool, name):
    """
    Получение количества бракованных, небракованных и всех деталей для указанного имени.
    """
    try:
        async with pool.acquire() as conn:
            # Общее количество деталей с указанным именем
            total_query = "SELECT COUNT(*) FROM details WHERE name = $1;"
            total_count = await conn.fetchval(total_query, name)

            # Количество бракованных деталей с указанным именем
            defective_query = "SELECT COUNT(*) FROM details WHERE name = $1 AND defective = TRUE;"
            defective_count = await conn.fetchval(defective_query, name)

            # Количество небракованных деталей с указанным именем
            non_defective_query = "SELECT COUNT(*) FROM details WHERE name = $1 AND defective = FALSE;"
            non_defective_count = await conn.fetchval(non_defective_query, name)

            return {
                "total": total_count,
                "defective": defective_count,
                "non_defective": non_defective_count
            }
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return None
    
async def kocak(pool, serial):
    try:
        async with pool.acquire() as conn:
            query = """
                UPDATE details
                SET defective = TRUE
                WHERE serial_number = $1;
            """
            await conn.execute(query, serial)
            return "OK"
    except Exception as e:
        print(f"Ошибка при изменении брака: {e}")
        return e

async def add_report(pool, name, text, time):
    """
    Добавление нового отчета в базу данных.
    """
    try:
        async with pool.acquire() as conn:
            query = """
                INSERT INTO reports (name, text, time)
                VALUES ($1, $2, $3);
            """
            await conn.execute(query, name, text, time)
            return "OK"
    except Exception as e:
        print(f"Ошибка при добавлении отчета: {e}")
        return e

async def get_all_reports(pool):
    """
    Получение всех отчетов из базы данных.
    """
    try:
        async with pool.acquire() as conn:
            query = "SELECT * FROM reports ORDER BY time DESC;"
            reports = await conn.fetch(query)
            if reports:
                return reports
            return None
    except Exception as e:
        print(f"Ошибка при получении отчетов: {e}")
        return None

async def delete_report(pool, report_id):
    """
    Удаление отчета по ID.
    """
    try:
        async with pool.acquire() as conn:
            # Преобразуем ID в целое число
            report_id = int(report_id)
            query = "DELETE FROM reports WHERE id = $1;"
            await conn.execute(query, report_id)
            return "OK"
    except ValueError:
        return "Invalid ID format"
    except Exception as e:
        print(f"Ошибка при удалении отчета: {e}")
        return str(e)

async def start_session(pool, name, surname, work_description):
    """
    Начало новой сессии по имени пользователя.
    """
    try:
        user_id = await get_user_id_by_name(pool, name, surname)
        if not user_id:
            return "Пользователь не найден"
            
        async with pool.acquire() as conn:
            # Явно задаем текущее время в правильном формате
            # Используем текущее время с учетом часовой зоны UTC+5
            current_time = time.strftime('%Y-%m-%d %H:%M', time.localtime())
            query = """
                INSERT INTO sessions (user_id, work_description, status, start_time)
                VALUES ($1, $2, 'active', $3);
            """
            await conn.execute(query, user_id, work_description, current_time)
            return "OK"
    except Exception as e:
        print(f"Ошибка при создании сессии: {e}")
        return str(e)

async def end_session(pool, name, surname):
    """
    Завершение и удаление активной сессии пользователя по имени.
    """
    try:
        user_id = await get_user_id_by_name(pool, name, surname)
        if not user_id:
            return "Пользователь не найден"
            
        async with pool.acquire() as conn:
            query = """
                DELETE FROM sessions 
                WHERE user_id = $1 AND status = 'active';
            """
            await conn.execute(query, user_id)
            return "OK"
    except Exception as e:
        print(f"Ошибка при завершении сессии: {e}")
        return str(e)

async def get_all_sessions(pool):
    """
    Получение всех сессий с именами пользователей.
    """
    try:
        async with pool.acquire() as conn:
            query = """
                SELECT 
                    s.id,
                    s.user_id,
                    s.start_time,
                    s.work_description,
                    s.status,
                    s.notes,
                    u.name,
                    u.surname 
                FROM sessions s
                JOIN users u ON s.user_id = u.id
                ORDER BY s.start_time DESC;
            """
            sessions = await conn.fetch(query)
            if sessions:
                # Преобразуем Record в словарь
                formatted_sessions = [dict(session) for session in sessions]
                return formatted_sessions
            return None
    except Exception as e:
        print(f"Ошибка при получении сессий: {e}")
        return None

async def is_session_active(pool, name, surname):
    """
    Проверка наличия активной сессии у пользователя по имени.
    """
    try:
        user_id = await get_user_id_by_name(pool, name, surname)
        if not user_id:
            return False
            
        async with pool.acquire() as conn:
            query = """
                SELECT COUNT(*) 
                FROM sessions 
                WHERE user_id = $1 AND status = 'active';
            """
            count = await conn.fetchval(query, user_id)
            return count > 0
    except Exception as e:
        print(f"Ошибка при проверке сессии: {e}")
        return False

async def update_session_description(pool, name, surname, new_description):
    """
    Изменение описания работы в активной сессии пользователя.
    """
    try:
        user_id = await get_user_id_by_name(pool, name, surname)
        if not user_id:
            return "Пользователь не найден"
            
        async with pool.acquire() as conn:
            query = """
                UPDATE sessions 
                SET work_description = $1
                WHERE user_id = $2 AND status = 'active';
            """
            await conn.execute(query, new_description, user_id)
            return "OK"
    except Exception as e:
        print(f"Ошибка при обновлении описания сессии: {e}")
        return str(e)