import asyncio
import json
import asyncpg
import logging
from logging.handlers import RotatingFileHandler
import datetime
import shutil

from database import *

MAX_CONNECTIONS = 100
semaphore = asyncio.Semaphore(MAX_CONNECTIONS)

# Настройка логгера
logger = logging.getLogger('server')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('server.log', maxBytes=10*1024*1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

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

async def daily_log_transfer():
    """Фоновая задача, которая каждый день в 00:00 по МСК копирует лог-файл на флешку."""
    while True:
        moscow_tz = datetime.timezone(datetime.timedelta(hours=3))
        now = datetime.datetime.now(moscow_tz)
        tomorrow = now.date() + datetime.timedelta(days=1)
        midnight = datetime.datetime.combine(tomorrow, datetime.time.min, tzinfo=moscow_tz)
        seconds_until_midnight = (midnight - now).total_seconds()
        await asyncio.sleep(seconds_until_midnight)
        
        log_filename = f"server_{now.strftime('%Y%m%d')}.log"
        flash_drive_path = f"/media/dytt/ESD-ISO/server_{now.strftime('%Y%m%d_%H%M%S')}.log"

        
        try:
            shutil.copy('server.log', flash_drive_path)
            logger.info(f"Лог-файл скопирован на флешку: {flash_drive_path}")
            # Опционально можно очистить лог-файл после копирования:
            # with open('server.log', 'w'): pass
        except Exception as e:
            logger.error(f"Ошибка при копировании лог-файла: {e}")

async def handle_client(reader, writer, pool):
    """Обработчик клиентских запросов с логированием."""
    client_address = writer.get_extra_info('peername')
    logger.info(f"Подключился клиент: {client_address}")

    async with semaphore:
        try:
            data = await reader.read(4096)
            if not data:
                logger.warning(f"Клиент {client_address} отправил пустые данные.")
                writer.close()
                await writer.wait_closed()
                return

            message = data.decode('utf-8')
            logger.info(f"Получено от {client_address}: {message}")

            try:
                json_data = json.loads(message)
                logger.info(f"Получено (JSON): {json_data}")
                
                response = {"status": "error", "message": "Invalid request"}
                
                if json_data.get("type") == "user" and "uid" in json_data:
                    user_data = await get_user_by_uid(pool, json_data["uid"])
                    if user_data:
                        if user_data.get("has_active_session"):
                            response = {
                                "status": "error",
                                "message": "У пользователя уже есть активная сессия",
                                "name": user_data['name'],
                                "surname": user_data['surname']
                                                    }
                        else:
                            response = {
                                "status": "ok",
                                "name": user_data['name'],
                                "surname": user_data['surname'],
                                "id": user_data['id']
                            }
                    else:
                        response = {"status": "error", "message": "User not found"}
                
                elif json_data.get("type") == "details" and "serial" in json_data:
                    details_data = await get_details_by_serial(pool, json_data["serial"])
                    if details_data:
                        response = {"status": "ok", "data": serialize_record(details_data)}
                    else:
                        response = {"status": "error", "message": "Details not found"}

                elif json_data.get("type") == "addUser":
                    add = await addUserInDb(pool, json_data["name"], json_data["surname"], json_data["prof"])
                    if add == 'OK':
                        response = {"status": "ok"}
                    else:
                        response = {"status": "error", "message": add}

                elif json_data.get("type") == "addDetail": 
                    add = await addDetail(pool, json_data) 
                    if add == 'OK': 
                        response = {"status": "ok"} 
                    else: 
                        response = {"status": "error", "message": add}

                elif json_data.get("type") == "allDetails":
                    data = await getDetails(pool, json_data['detail'])
                    if data:
                        response = {"status": "ok", "data": serialize_record(data)}
                    else:
                        response = {"status": "error", "message": "Details not found"}

                elif json_data.get("type") == "allUsers":
                    data = await allusers(pool)
                    if data:
                        response = {"status": "ok", "data": serialize_record(data)}
                    else:
                        response = {"status": "error", "message": "Users not found"}

                elif json_data.get("type") == "getstats":
                    stats = await get_defective_counts(pool, json_data['name'])
                    if stats:
                        response = {"status": "ok", "total": stats["total"],
                                    "defective": stats["defective"],
                                    "non_defective": stats["non_defective"]}
                    else:
                        response = {"status": "error", "message": "Failed to retrieve statistics"}

                elif json_data.get("type") == "mark":
                    data = await add_sensor(pool, json_data["name"], json_data["serial"], json_data["time"], json_data["id"])
                    if data:
                        response = {"status": "ok"}
                    else:
                        response = {"status": "error", "message": "Failed to mark"}

                elif json_data.get("type") == "updatestage":
                    # Обязательные поля
                    serial = json_data.get('serial')
                    stage = json_data.get('stage')
                    
                    # Опциональные поля с проверкой типов
                    start = json_data.get('start')
                    end = json_data.get('end')
                    responsible_user = json_data.get('id')
                    
                    if not serial or not stage:
                        response = {"status": "error", "message": "Отсутствуют обязательные параметры serial или stage"}
                    else:
                        try:
                            data = await update_stage_by_serial(
                                pool, 
                                serial, 
                                stage, 
                                start, 
                                end, 
                                responsible_user
                            )
                            if "OK" in data:
                                # Проверяем, был ли назначен сектор хранения
                                if "|" in data:
                                    sector = data.split("|")[1]
                                    response = {"status": "ok", "sector": sector}
                                else:
                                    response = {"status": "ok"}
                            else:
                                response = {"status": "error", "message": data}
                        except Exception as e:
                            logger.error(f"Ошибка при обновлении этапа: {e}")
                            response = {"status": "error", "message": str(e)}

                elif json_data.get("type") == "kocak":
                    data = await kocak(pool, json_data['serial'])
                    if data:
                        response = {"status": "ok"}
                    else:
                        response = {"status": "error", "message": "Брак не смог"}

                elif json_data.get("type") == "report":
                    data = await add_report(pool, json_data['name'], json_data['text'], json_data['time'])
                    if data == "OK":
                        response = {"status": "ok"}
                    else:
                        response = {"status": "error", "message": data}

                elif json_data.get("type") == "getreports":
                    data = await get_all_reports(pool)
                    if data:
                        response = {"status": "ok", "data": serialize_record(data)}
                    else:
                        response = {"status": "error", "message": "Отчеты не найдены"}

                elif json_data.get("type") == "deleteReport":
                    data = await delete_report(pool, json_data['id'])
                    if data == "OK":
                        response = {"status": "ok"}
                    else:
                        response = {"status": "error", "message": data}

                elif json_data.get("type") == "startSession":
                    data = await start_session(pool, json_data['name'], json_data['surname'], json_data['work_description'])
                    if data == "OK":
                        response = {"status": "ok"}
                    else:
                        response = {"status": "error", "message": data}

                elif json_data.get("type") == "endSession":
                    data = await end_session(pool, json_data['name'], json_data['surname'])
                    if data == "OK":
                        response = {"status": "ok"}
                    else:
                        response = {"status": "error", "message": data}

                elif json_data.get("type") == "getSessions":
                    data = await get_all_sessions(pool)
                    if data:
                        response = {"status": "ok", "data": serialize_record(data)}
                    else:
                        response = {"status": "error", "message": "Сессии не найдены"}

                elif json_data.get("type") == "isSessionActive":
                    is_active = await is_session_active(pool, json_data['name'], json_data['surname'])
                    response = {"status": "ok", "active": is_active}

                elif json_data.get("type") == "updateSessionDescription":
                    data = await update_session_description(pool, json_data['name'], json_data['surname'], json_data['new_description'])
                    if data == "OK":
                        response = {"status": "ok"}
                    else:
                        response = {"status": "error", "message": data}
                
                elif json_data.get("type") == "deleteAllSessions":
                    keep_current = json_data.get("keepCurrentSession", False)
                    logger.info(f"Запрос на удаление всех сессий, кроме текущей: {keep_current}")
                    
                    count, error = await delete_all_sessions(pool, keep_current)
                    if error:
                        response = {"status": "error", "message": error}
                    else:
                        response = {"status": "ok", "count": count}
                        logger.info(f"Удалено сессий: {count}")

                # Новая ветка для запроса логов
                elif json_data.get("type") == "logs":
                    moscow_tz = datetime.timezone(datetime.timedelta(hours=3))
                    now = datetime.datetime.now(moscow_tz)
                    log_filename = f"server_{now.strftime('%Y%m%d_%H%M%S')}.log"
                    flash_drive_path = f"/media/dytt/ESD-ISO/server_{now.strftime('%Y%m%d_%H%M%S')}.log"
                    try:
                        shutil.copy('server.log', flash_drive_path)
                        logger.info(f"Лог-файл отправлен на флешку: {flash_drive_path}")
                        response = {"status": "ok", "message": f"Логи отправлены: {flash_drive_path}"}
                    except Exception as e:
                        logger.error(f"Ошибка при отправке логов: {e}")
                        response = {"status": "error", "message": f"Ошибка при отправке логов: {e}"}
                
                elif json_data.get("type") == "getSectorsStatus":
                    data = await get_sectors_status(pool)
                    if data:
                        response = {"status": "ok", "data": serialize_record(data)}
                    else:
                        response = {"status": "error", "message": "Информация о секторах не найдена"}
                elif json_data.get("type") == "test":
                    response = {"status": "ok"}
                
                elif json_data.get("type") == "alldefective":
                    data = await get_all_defective_details(pool)
                    if data:
                        response = {"status": "ok", "data": serialize_record(data)}
                    else:
                        response = {"status": "error", "message": "Бракованные детали не найдены"}
                
                elif json_data.get("type") == "userById" and "id" in json_data:
                    user_id = json_data["id"]
                    user_data = await get_user_by_id(pool, user_id)
                    if user_data:
                        response = {"status": "ok", "data": serialize_record(user_data)}
                    else:
                        response = {"status": "error", "message": f"Пользователь с ID {user_id} не найден"}
                
                elif json_data.get("type") == "production_stats":
                    # Получение статистики производства по конкретной модели датчика
                    device_name = json_data.get("device_name")  # Может быть None для получения статистики по всем датчикам
                    months = json_data.get("months", 4)  # По умолчанию за 4 месяца
                    
                    stats = await get_detailed_production_stats(pool, device_name, months)
                    if stats:
                        response = {"status": "ok", "data": stats}
                    else:
                        response = {"status": "error", "message": "Не удалось получить статистику производства"}
                
                elif json_data.get("type") == "monthly_stats":
                    # Получение только статистики по месяцам
                    device_name = json_data.get("device_name")
                    months = json_data.get("months", 4)
                    
                    stats = await get_monthly_production_stats(pool, device_name, months)
                    if stats:
                        response = {"status": "ok", "data": serialize_record(stats)}
                    else:
                        response = {"status": "error", "message": "Не удалось получить статистику по месяцам"}
                
                elif json_data.get("type") == "defects_by_stage":
                    # Получение только статистики брака по этапам
                    device_name = json_data.get("device_name")
                    months = json_data.get("months", 4)
                    
                    stats = await get_defects_by_stage(pool, device_name, months)
                    if stats:
                        response = {"status": "ok", "data": serialize_record(stats)}
                    else:
                        response = {"status": "error", "message": "Не удалось получить статистику брака по этапам"}

            except json.JSONDecodeError:
                response = {"status": "error", "message": "Invalid JSON"}
            except KeyError as e:
                response = {"status": "error", "message": f"Missing key in JSON: {e}"}
            
            writer.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            await writer.drain()

        except Exception as e:
            logger.error(f"Ошибка при обработке клиента {client_address}: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
            logger.info(f"Соединение с {client_address} закрыто")

async def start_server(host='0.0.0.0', port=12345):
    logger.info("Создание пула соединений...")
    pool = await create_pool()
    logger.info("Пул соединений создан.")
    
    # Инициализация секторов хранения
    logger.info("Инициализация секторов хранения...")
    storage_init_result = await initialize_storage_sectors(pool)
    logger.info(f"Результат инициализации секторов: {storage_init_result}")
    
    # Запуск фоновой задачи для ежедневного копирования логов
    asyncio.create_task(daily_log_transfer())
    
    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, pool),
        host,
        port
    )
    addr = server.sockets[0].getsockname()
    logger.info(f"JSON-сервер запущен на {addr}")
    
    try:
        async with server:
            await server.serve_forever()
    finally:
        logger.info("Закрытие пула соединений...")
        await pool.close()
        logger.info("Пул соединений закрыт.")

if __name__ == "__main__":
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        logger.info("Сервер остановлен")
