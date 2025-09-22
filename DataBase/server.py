import logging
from logging.handlers import RotatingFileHandler
import shutil
import datetime
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Query, Body
import uvicorn

from database import (
    create_pool,
    serialize_record,
    get_user_by_uid,
    get_details_by_serial,
    addUserInDb,
    addDetail,
    getDetails,
    allusers,
    get_defective_counts,
    add_sensor,
    update_stage_by_serial,
    kocak,
    add_report,
    get_all_reports,
    delete_report,
    start_session,
    end_session,
    get_all_sessions,
    is_session_active,
    update_session_description,
    delete_all_sessions,
    initialize_storage_sectors,
    get_sectors_status,
    get_all_defective_details,
    get_user_by_id,
    get_detailed_production_stats,
    get_monthly_production_stats,
    get_defects_by_stage,
)

# Логгер
logger = logging.getLogger('server')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('server.log', maxBytes=10*1024*1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = FastAPI(title="RFID API", version="1.0.0")


async def get_pool():
    pool = getattr(app.state, 'pool', None)
    if pool is None:
        raise HTTPException(status_code=500, detail="Пул соединений не инициализирован")
    return pool


@app.on_event('startup')
async def on_startup():
    logger.info("Создание пула соединений...")
    app.state.pool = await create_pool()
    logger.info("Пул соединений создан.")
    logger.info("Инициализация секторов хранения...")
    storage_init_result = await initialize_storage_sectors(app.state.pool)
    logger.info(f"Результат инициализации секторов: {storage_init_result}")


@app.on_event('shutdown')
async def on_shutdown():
    logger.info("Закрытие пула соединений...")
    pool = getattr(app.state, 'pool', None)
    if pool:
        await pool.close()
        logger.info("Пул соединений закрыт.")


@app.get('/health')
async def health():
    return {"status": "ok"}


# Пользователи
@app.post('/user/by-uid')
async def user_by_uid(uid: str = Body(..., embed=True), pool=Depends(get_pool)):
    user_data = await get_user_by_uid(pool, uid)
    if not user_data:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if user_data.get('has_active_session'):
        return {"status": "error", "message": "У пользователя уже есть активная сессия", "name": user_data['name'], "surname": user_data['surname'], "id": user_data['id']}
    return {"status": "ok", **user_data}


@app.get('/users')
async def get_all_users(pool=Depends(get_pool)):
    data = await allusers(pool)
    return {"status": "ok", "data": serialize_record(data) if data else []}


@app.post('/users')
async def add_user(name: str = Body(...), surname: str = Body(...), prof: str = Body(...), pool=Depends(get_pool)):
    res = await addUserInDb(pool, name, surname, prof)
    if res == 'OK':
        return {"status": "ok"}
    raise HTTPException(status_code=400, detail=str(res))


@app.get('/users/{user_id}')
async def user_by_id(user_id: int, pool=Depends(get_pool)):
    data = await get_user_by_id(pool, user_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"Пользователь с ID {user_id} не найден")
    return {"status": "ok", "data": serialize_record(data)}


# Детали
@app.get('/details/{serial}')
async def details_by_serial(serial: str, pool=Depends(get_pool)):
    data = await get_details_by_serial(pool, serial)
    if not data:
        raise HTTPException(status_code=404, detail="Деталь не найдена")
    return {"status": "ok", "data": serialize_record(data)}


@app.get('/details')
async def details_by_name(name: str = Query(..., alias='detail'), pool=Depends(get_pool)):
    data = await getDetails(pool, name)
    return {"status": "ok", "data": serialize_record(data) if data else []}


@app.post('/details')
async def add_detail(detail: dict = Body(...), pool=Depends(get_pool)):
    res = await addDetail(pool, detail)
    if res == 'OK':
        return {"status": "ok"}
    raise HTTPException(status_code=400, detail=str(res))


@app.post('/details/mark')
async def mark_detail(name: str = Body(...), serial: str = Body(...), time: str = Body(...), id: int = Body(...), pool=Depends(get_pool)):
    res = await add_sensor(pool, name, serial, time, id)
    if res == 'OK':
        return {"status": "ok"}
    raise HTTPException(status_code=400, detail=str(res))


@app.post('/details/{serial}/stage')
async def update_stage(serial: str, stage: str = Body(...), start: Optional[str] = Body(None), end: Optional[str] = Body(None), id: Optional[int] = Body(None), pool=Depends(get_pool)):
    res = await update_stage_by_serial(pool, serial, stage, start, end, id)
    if isinstance(res, str) and res.startswith('OK'):
        if '|' in res:
            sector = res.split('|')[1]
            return {"status": "ok", "sector": sector}
        return {"status": "ok"}
    raise HTTPException(status_code=400, detail=str(res))


@app.post('/details/{serial}/defective')
async def set_defective(serial: str, pool=Depends(get_pool)):
    res = await kocak(pool, serial)
    if res == 'OK':
        return {"status": "ok"}
    raise HTTPException(status_code=400, detail=str(res))


@app.get('/defective/details')
async def all_defective(pool=Depends(get_pool)):
    data = await get_all_defective_details(pool)
    return {"status": "ok", "data": serialize_record(data) if data else []}


# Отчеты
@app.post('/reports')
async def create_report(name: str = Body(...), text: str = Body(...), time: str = Body(...), pool=Depends(get_pool)):
    res = await add_report(pool, name, text, time)
    if res == 'OK':
        return {"status": "ok"}
    raise HTTPException(status_code=400, detail=str(res))


@app.get('/reports')
async def list_reports(pool=Depends(get_pool)):
    data = await get_all_reports(pool)
    return {"status": "ok", "data": serialize_record(data) if data else []}


@app.delete('/reports/{report_id}')
async def remove_report(report_id: int, pool=Depends(get_pool)):
    res = await delete_report(pool, report_id)
    if res == 'OK':
        return {"status": "ok"}
    raise HTTPException(status_code=400, detail=str(res))


# Сессии
@app.post('/sessions/start')
async def session_start(name: str = Body(...), surname: str = Body(...), work_description: str = Body(...), pool=Depends(get_pool)):
    res = await start_session(pool, name, surname, work_description)
    if res == 'OK':
        return {"status": "ok"}
    raise HTTPException(status_code=400, detail=str(res))


@app.post('/sessions/end')
async def session_end(name: str = Body(...), surname: str = Body(...), pool=Depends(get_pool)):
    res = await end_session(pool, name, surname)
    if res == 'OK':
        return {"status": "ok"}
    raise HTTPException(status_code=400, detail=str(res))


@app.get('/sessions')
async def sessions(pool=Depends(get_pool)):
    data = await get_all_sessions(pool)
    return {"status": "ok", "data": serialize_record(data) if data else []}


@app.get('/sessions/active')
async def session_active(name: str = Query(...), surname: str = Query(...), pool=Depends(get_pool)):
    is_active = await is_session_active(pool, name, surname)
    return {"status": "ok", "active": is_active}


@app.patch('/sessions/description')
async def session_update_description(name: str = Body(...), surname: str = Body(...), new_description: str = Body(...), pool=Depends(get_pool)):
    res = await update_session_description(pool, name, surname, new_description)
    if res == 'OK':
        return {"status": "ok"}
    raise HTTPException(status_code=400, detail=str(res))


@app.delete('/sessions')
async def sessions_delete(keepCurrentSession: bool = Query(False), pool=Depends(get_pool)):
    count, error = await delete_all_sessions(pool, keepCurrentSession)
    if error:
        raise HTTPException(status_code=400, detail=str(error))
    return {"status": "ok", "count": count}


# Сектора хранения
@app.get('/sectors')
async def sectors(pool=Depends(get_pool)):
    data = await get_sectors_status(pool)
    return {"status": "ok", "data": serialize_record(data) if data else []}


# Статистика
@app.get('/stats/defective-counts')
async def stats_defective_counts(name: str = Query(...), pool=Depends(get_pool)):
    stats = await get_defective_counts(pool, name)
    if not stats:
        return {"status": "ok", "total": 0, "defective": 0, "non_defective": 0}
    return {"status": "ok", **stats}


@app.get('/stats/production')
async def stats_production(device_name: Optional[str] = Query(None), months: int = Query(4), pool=Depends(get_pool)):
    stats = await get_detailed_production_stats(pool, device_name, months)
    if not stats:
        raise HTTPException(status_code=400, detail="Не удалось получить статистику производства")
    return {"status": "ok", "data": stats}


@app.get('/stats/monthly')
async def stats_monthly(device_name: Optional[str] = Query(None), months: int = Query(4), pool=Depends(get_pool)):
    stats = await get_monthly_production_stats(pool, device_name, months)
    return {"status": "ok", "data": serialize_record(stats) if stats else []}


@app.get('/stats/defects-by-stage')
async def stats_defects_by_stage(device_name: Optional[str] = Query(None), months: int = Query(4), pool=Depends(get_pool)):
    stats = await get_defects_by_stage(pool, device_name, months)
    return {"status": "ok", "data": serialize_record(stats) if stats else []}


# Логи
@app.post('/logs/send-to-usb')
async def send_logs_to_usb():
    moscow_tz = datetime.timezone(datetime.timedelta(hours=3))
    now = datetime.datetime.now(moscow_tz)
    flash_drive_path = f"/media/dytt/ESD-ISO/server_{now.strftime('%Y%m%d_%H%M%S')}.log"
    try:
        shutil.copy('server.log', flash_drive_path)
        logger.info(f"Лог-файл отправлен на флешку: {flash_drive_path}")
        return {"status": "ok", "message": f"Логи отправлены: {flash_drive_path}"}
    except Exception as e:
        logger.error(f"Ошибка при отправке логов: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка при отправке логов: {e}")


if __name__ == '__main__':
    uvicorn.run('server:app', host='0.0.0.0', port=8000, reload=False)


