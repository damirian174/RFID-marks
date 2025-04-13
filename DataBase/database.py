import asyncpg
import random
import datetime
import time
import json

def serialize_record(record):
    """Рекурсивно преобразует asyncpg.Record или вложенные структуры в словарь."""
    if isinstance(record, asyncpg.Record):
        return dict(record)
    elif isinstance(record, list):
        return [serialize_record(item) for item in record]
    elif isinstance(record, dict):
        return {key: serialize_record(value) for key, value in record.items()}
    else:
        return record

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
                    "id": user["id"],
                    "has_active_session": True
                }
            
            return {
                "name": user["name"],
                "surname": user["surname"],
                "id": user["id"],
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

async def add_sensor(pool, name, serial_number, time, id):
    """
    Добавление датчика с указанием названия и серийного номера.
    """
    try:
        async with pool.acquire() as conn:
            # Создаем структуру данных для поля time
            time_data = {
                "mark": {
                    "time": time,
                    "user": id
                }
            }
            
            # Журналируем входящие параметры
            print(f"add_sensor: params = {name}, {serial_number}, {time}, {id}")
            print(f"time_data = {time_data}")
            
            # Преобразуем словарь в JSON-строку
            time_json = json.dumps(time_data)
            
            query = """
                INSERT INTO details (name, serial_number, stage, time)
                VALUES ($1, $2, $3, $4::jsonb);
            """
            await conn.execute(query, name, serial_number, "Маркировка", time_json)
            return "OK"
    except Exception as e:
        print(f"Ошибка при добавлении датчика: {e}")
        return e

async def update_stage_by_serial(pool, serial_number, new_stage, start=None, end=None, responsible_user=None):
    """
    Изменение stage по серийному номеру.
    Если stage равен "Упаковка", то деталь помещается в доступный сектор хранения.
    Для бракованных деталей (defective = TRUE) обновление этапа запрещено.
    
    Добавляет/обновляет поле time с информацией о времени начала, окончания этапа
    и ответственном пользователе.
    """
    try:
        # Журналируем входящие параметры
        print(f"update_stage_by_serial: params = {serial_number}, {new_stage}, {start}, {end}, {responsible_user}")
        
        async with pool.acquire() as conn:
            # Проверяем, является ли деталь бракованной
            check_query = "SELECT defective, time FROM details WHERE serial_number = $1;"
            row = await conn.fetchrow(check_query, serial_number)
            
            if not row:
                return "Деталь не найдена"
                
            is_defective = row['defective']
            # Преобразуем time из JSONB в словарь
            current_time_data = {}
            
            if row['time']:
                # Обрабатываем случаи, когда данные могут быть в разных форматах
                if isinstance(row['time'], dict):
                    current_time_data = row['time']
                elif isinstance(row['time'], str):
                    try:
                        current_time_data = json.loads(row['time'])
                    except json.JSONDecodeError:
                        current_time_data = {}
            
            if is_defective:
                return "Невозможно изменить этап для бракованной детали"
            
            # Формируем данные для поля time
            stage_key = new_stage.lower()
            
            # Обновляем или создаем запись для текущего этапа
            if stage_key not in current_time_data:
                current_time_data[stage_key] = {}
                
            stage_data = current_time_data[stage_key]
            
            if start:
                stage_data['start'] = start
            if end:
                stage_data['end'] = end
            if responsible_user is not None:
                stage_data['user'] = responsible_user
            
            # Преобразуем словарь в JSON-строку
            time_json = json.dumps(current_time_data)
            
            # Проверяем, является ли новый этап "Упаковка"
            if new_stage == "Упаковка":
                # Получаем доступный сектор
                sector = await get_available_storage_sector(pool)
                
                if not sector:
                    # Если нет доступных секторов, возвращаем ошибку
                    return "Нет доступных секторов для хранения"
                
                # Обновляем этап и устанавливаем сектор хранения
                query = """
                    UPDATE details
                    SET stage = $1, sector = $2, time = $3::jsonb
                    WHERE serial_number = $4;
                """
                await conn.execute(query, "Хранение", f"Сектор {sector['sector_name']}", 
                                  time_json, serial_number)
                
                # Увеличиваем занятость сектора
                await update_sector_occupation(pool, sector['sector_name'])
                
                # Получаем название детали
                detail_query = "SELECT name FROM details WHERE serial_number = $1;"
                detail_name = await conn.fetchval(detail_query, serial_number)
                
                info = f"Деталь {detail_name} (S/N: {serial_number}) помещена на хранение в сектор {sector['sector_name']}"
                print(info)
                return f"OK|{sector['sector_name']}"
            else:
                # Обычное обновление этапа
                query = """
                    UPDATE details
                    SET stage = $1, time = $2::jsonb
                    WHERE serial_number = $3;
                """
                await conn.execute(query, new_stage, time_json, serial_number)
                return "OK"
    except Exception as e:
        print(f"Ошибка при изменении stage: {e}")
        return str(e)

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
    Обновление описания работы для активной сессии пользователя.
    """
    try:
        # Получаем ID пользователя
        user_id = await get_user_id_by_name(pool, name, surname)
        if not user_id:
            return f"Пользователь {name} {surname} не найден"
        
        async with pool.acquire() as conn:
            # Обновляем описание сессии
            update_query = """
                UPDATE sessions
                SET work_description = $1
                WHERE user_id = $2 AND status = 'active';
            """
            await conn.execute(update_query, new_description, user_id)
            return "OK"
    except Exception as e:
        print(f"Ошибка при обновлении описания сессии: {e}")
        return str(e)

async def delete_all_sessions(pool, keep_current=False):
    """
    Удаление всех сессий. Если keep_current=True, то сохраняется текущая активная сессия.
    
    Возвращает:
        tuple: (количество удаленных сессий, сообщение об ошибке или None в случае успеха)
    """
    try:
        async with pool.acquire() as conn:
            if keep_current:
                # Находим текущую активную сессию (последняя по времени начала)
                current_session_query = """
                    SELECT id, user_id 
                    FROM sessions 
                    WHERE status = 'active' 
                    ORDER BY start_time DESC 
                    LIMIT 1;
                """
                current_session = await conn.fetchrow(current_session_query)
                
                if current_session:
                    # Удаляем все активные сессии других пользователей, сохраняя все сессии текущего пользователя
                    delete_query = """
                        DELETE FROM sessions 
                        WHERE user_id != $1 AND status = 'active'
                        RETURNING id;
                    """
                    deleted_sessions = await conn.fetch(delete_query, current_session["user_id"])
                    
                    # Получаем информацию о пользователе текущей сессии для логирования
                    user_info = await get_user_name_by_id(pool, current_session["user_id"])
                    user_str = f"{user_info['surname']} {user_info['name']}" if user_info else f"ID:{current_session['user_id']}"
                    
                    print(f"Удалены все сессии, кроме сессий пользователя {user_str}")
                    return len(deleted_sessions), None
                else:
                    # Удаляем все активные сессии, так как нет текущей активной
                    delete_query = """
                        DELETE FROM sessions 
                        WHERE status = 'active'
                        RETURNING id;
                    """
                    deleted_sessions = await conn.fetch(delete_query)
                    
                    print(f"Удалены все активные сессии (активной сессии не найдено)")
                    return len(deleted_sessions), None
            else:
                # Удаляем все активные сессии
                delete_query = """
                    DELETE FROM sessions 
                    WHERE status = 'active'
                    RETURNING id;
                """
                deleted_sessions = await conn.fetch(delete_query)
                
                print(f"Удалены все активные сессии")
                return len(deleted_sessions), None
    except Exception as e:
        error_msg = f"Ошибка при удалении сессий: {e}"
        print(error_msg)
        return 0, error_msg

async def initialize_storage_sectors(pool):
    """
    Инициализирует секторы хранения, если они еще не существуют.
    Создает сектора 1А, 1Б, 1В, 2А, 2Б, 2В и т.д. до 10
    """
    try:
        async with pool.acquire() as conn:
            # Проверяем, есть ли уже секторы в базе
            exists_query = "SELECT COUNT(*) FROM storage_sectors;"
            count = await conn.fetchval(exists_query)
            
            if count == 0:
                # Создаем секторы от 1 до 10, с вариантами А, Б, В для каждого
                for number in range(1, 11):
                    for letter in ['А', 'Б', 'В']:
                        sector_name = f"{number}{letter}"
                        insert_query = """
                            INSERT INTO storage_sectors (sector_name, occupied_slots, max_capacity)
                            VALUES ($1, 0, 5);
                        """
                        await conn.execute(insert_query, sector_name)
                
                print("Секторы хранения успешно инициализированы")
                return "OK"
            return "Секторы уже существуют"
    except Exception as e:
        error_msg = f"Ошибка при инициализации секторов хранения: {e}"
        print(error_msg)
        return error_msg

async def get_available_storage_sector(pool):
    """
    Находит первый доступный сектор для хранения деталей.
    Доступным считается сектор, в котором занято меньше max_capacity слотов.
    """
    try:
        async with pool.acquire() as conn:
            query = """
                SELECT sector_name, occupied_slots, max_capacity 
                FROM storage_sectors 
                WHERE occupied_slots < max_capacity 
                ORDER BY id 
                LIMIT 1;
            """
            sector = await conn.fetchrow(query)
            
            if sector:
                return sector
            return None
    except Exception as e:
        print(f"Ошибка при поиске доступного сектора: {e}")
        return None

async def update_sector_occupation(pool, sector_name):
    """
    Увеличивает количество занятых слотов в секторе на 1.
    """
    try:
        async with pool.acquire() as conn:
            query = """
                UPDATE storage_sectors
                SET occupied_slots = occupied_slots + 1
                WHERE sector_name = $1
                RETURNING occupied_slots;
            """
            new_occupation = await conn.fetchval(query, sector_name)
            return new_occupation
    except Exception as e:
        print(f"Ошибка при обновлении занятости сектора: {e}")
        return None

async def get_sectors_status(pool):
    """
    Получение информации о занятости всех секторов хранения.
    """
    try:
        async with pool.acquire() as conn:
            query = """
                SELECT sector_name, occupied_slots, max_capacity 
                FROM storage_sectors 
                ORDER BY sector_name;
            """
            sectors = await conn.fetch(query)
            
            if sectors:
                return sectors
            return None
    except Exception as e:
        print(f"Ошибка при получении статуса секторов: {e}")
        return None

async def get_all_defective_details(pool):
    """
    Получение всех деталей с отметкой о браке (defective = TRUE).
    """
    try:
        async with pool.acquire() as conn:
            query = """
                SELECT * FROM details 
                WHERE defective = TRUE 
                ORDER BY id;
            """
            defective_details = await conn.fetch(query)
            
            if defective_details:
                return defective_details
            return None
    except Exception as e:
        print(f"Ошибка при получении бракованных деталей: {e}")
        return None

async def get_user_by_id(pool, user_id):
    """
    Получение данных пользователя по ID.
    """
    try:
        async with pool.acquire() as conn:
            query = "SELECT id, name, surname, profession FROM users WHERE id = $1;"
            user = await conn.fetchrow(query, user_id)
            if user:
                return user  # Вернет Record, который будет сериализован в словарь
            return None
    except Exception as e:
        print(f"Ошибка при получении данных пользователя: {e}")
        return None

# ====== Новые функции для статистики ======

async def get_monthly_production_stats(pool, device_name=None, months=4):
    """
    Получение статистики производства датчиков по месяцам за указанный период.
    
    Args:
        pool: Пул соединений с базой данных
        device_name: Название модели датчика (МЕТРАН 150, МЕТРАН 75, МЕТРАН 55 или None для всех)
        months: Количество месяцев для анализа
        
    Returns:
        Статистика по месяцам: общее количество, количество брака
    """
    try:
        async with pool.acquire() as conn:
            # Запрос для получения статистики по месяцам
            query = """
                WITH part_dates AS (
                    SELECT 
                        d.id,
                        d.name,
                        d.defective,
                        CASE 
                            WHEN d.time ? 'mark' AND (d.time->'mark'->>'time') IS NOT NULL THEN 
                                TO_DATE((d.time->'mark'->>'time')::text, 'YYYY-MM-DD HH24:MI:SS')
                            ELSE NULL
                        END AS creation_date
                    FROM details d
                    WHERE 
                        ($1::text IS NULL OR d.name = $1)
                        AND d.time IS NOT NULL
                )
                SELECT 
                    TO_CHAR(date_trunc('month', creation_date), 'YYYY-MM') AS month,
                    COUNT(*) AS total_count,
                    SUM(CASE WHEN defective THEN 1 ELSE 0 END) AS defective_count
                FROM part_dates
                WHERE 
                    creation_date IS NOT NULL 
                    AND creation_date >= NOW() - INTERVAL '1 month' * $2
                GROUP BY date_trunc('month', creation_date)
                ORDER BY date_trunc('month', creation_date) DESC;
            """
            
            result = await conn.fetch(query, device_name, months)
            return result if result else []
    except Exception as e:
        print(f"Ошибка при получении статистики по месяцам: {e}")
        return []

async def get_defects_by_stage(pool, device_name=None, months=4):
    """
    Получение статистики брака по этапам за указанный период.
    
    Args:
        pool: Пул соединений с базой данных
        device_name: Название модели датчика (МЕТРАН 150, МЕТРАН 75, МЕТРАН 55 или None для всех)
        months: Количество месяцев для анализа
        
    Returns:
        Статистика брака по этапам производства
    """
    try:
        async with pool.acquire() as conn:
            # Запрос для получения статистики брака по этапам
            query = """
                WITH part_dates AS (
                    SELECT 
                        d.id,
                        d.name,
                        d.defective,
                        d.defect_stage_id,
                        d.stage,
                        CASE 
                            WHEN d.time ? 'mark' AND (d.time->'mark'->>'time') IS NOT NULL THEN 
                                TO_DATE((d.time->'mark'->>'time')::text, 'YYYY-MM-DD HH24:MI:SS')
                            ELSE NULL
                        END AS creation_date
                    FROM details d
                    WHERE 
                        ($1::text IS NULL OR d.name = $1)
                        AND d.time IS NOT NULL
                )
                SELECT 
                    COALESCE(defect_stage_id, stage) AS stage,
                    COUNT(*) AS defective_count
                FROM part_dates
                WHERE 
                    creation_date IS NOT NULL 
                    AND creation_date >= NOW() - INTERVAL '1 month' * $2
                    AND defective = TRUE
                GROUP BY COALESCE(defect_stage_id, stage)
                ORDER BY defective_count DESC;
            """
            
            result = await conn.fetch(query, device_name, months)
            return result if result else []
    except Exception as e:
        print(f"Ошибка при получении статистики брака по этапам: {e}")
        return []

async def get_detailed_production_stats(pool, device_name=None, months=4):
    """
    Получение детальной статистики производства датчиков.
    
    Args:
        pool: Пул соединений с базой данных
        device_name: Название модели датчика (МЕТРАН 150, МЕТРАН 75, МЕТРАН 55 или None для всех)
        months: Количество месяцев для анализа
        
    Returns:
        Детальная статистика, включающая общую статистику по месяцам и статистику брака по этапам
    """
    try:
        # Получаем статистику по месяцам
        monthly_stats = await get_monthly_production_stats(pool, device_name, months)
        
        # Получаем статистику брака по этапам
        stage_stats = await get_defects_by_stage(pool, device_name, months)
        
        return {
            "device_name": device_name if device_name else "Все датчики",
            "period_months": months,
            "monthly_stats": serialize_record(monthly_stats),
            "defects_by_stage": serialize_record(stage_stats)
        }
    except Exception as e:
        print(f"Ошибка при получении детальной статистики: {e}")
        return None