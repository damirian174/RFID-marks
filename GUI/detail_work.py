from database import database
from error_test import show_error_dialog
from config import work, detail
from datetime import datetime, timedelta
import time

mark_ui_instance = None
work_ui_instance = None
packing_ui_instance = None
test_ui_instance = None

data_detail = None

time_start = None 
time_end = None 

time_stage = None

def GetTime():
    utc = datetime.utcnow()
    time_c = utc + timedelta(hours=5)
    
    date_part = time_c.strftime("%Y-%m-%d") 
    time_part = time_c.strftime("%H:%M:%S")
    
    return {'date': date_part, 'time': time_part}

def getUI(mark_ui, work_ui, packing_ui, test_ui):
    global mark_ui_instance, work_ui_instance, packing_ui_instance, test_ui_instance
    mark_ui_instance = mark_ui
    work_ui_instance = work_ui
    packing_ui_instance = packing_ui
    test_ui_instance = test_ui
    


def start_work(ser, response):
    global time_start
    global work
    global detail
    work = True
    detail = ser
    time_start = GetTime()
    global mark_ui_instance, work_ui_instance, packing_ui_instance, test_ui_instance
    mark_ui_instance.detail(response)
    work_ui_instance.detail(response)
    packing_ui_instance.detail(response)
    test_ui_instance.detail(response)
    # work_ui_instance.running = True  # Это должно теперь работать
    # work_ui_instance.start_timer()

def pause_work():
    work_ui_instance.pause_timer()

def couintine_work():
    work_ui_instance.resume_timer()




def end_work():
    global work
    global detail
    global time_end 
    global data_detail
    global time_stage
    global time_start
    data = False
    work = False
    detail = None 
    time_end = GetTime()
    
    global mark_ui_instance, work_ui_instance, packing_ui_instance, test_ui_instance
    mark_ui_instance.detail(False)
    work_ui_instance.detail(False)
    packing_ui_instance.detail(False)
    test_ui_instance.detail(False)
    work_ui_instance.running = False
    work_ui_instance.stop_timer()  # Остановка таймера
    work_ui_instance.label.setText("00:00:00")  # Сброс отображаемого времени

    # if data_detail["stage"] == "Маркировка":
    #     # print(time_start)
    #     # print(time_end)
    #     # time_stage = {"stage": "Маркировка", "time_start": time_start, "time_end": time_end}
    #     # response_data = {'type': 'updatestage', 'stage': 'Маркировка', 'serial': data_detail["serial_number"], "time": time_stage}
    #     response_data = {'type': 'mark', 'name': '', 'serial': data_detail["serial_number"]}
    #     # print(response_data)
    #     response = database(response_data)

    
def update(name, serial):
    global work
    if work:
        end_work()
    if data_detail == None:
        
        # print(time_start)
        # print(time_end)
        # time_stage = {"stage": "Маркировка", "time_start": time_start, "time_end": time_end}
        # response_data = {'type': 'updatestage', 'stage': 'Маркировка', 'serial': data_detail["serial_number"], "time": time_stage}
        response_data = {'type': 'mark', 'name': 'name', 'serial': serial}
        # print(response_data)
        response = database(response_data)
    
    



def getDetail(serial_number):
    data = {"type": "details", "serial": serial_number}
    global data_detail
    global mark_ui_instance, work_ui_instance
    # data2 = {'name': 'МЕТРАН 150','serial_number': serial_number,'defective':'Да','stage':'Маркировка','sector':'аааа'}

    # mark_ui_instance.detail(data2)
    
    response = database(data)
    data_detail = response
    response = response['data']
    start_work(response["serial_number"], response)
    if "data" in response:
        # Вызываем метод detail через экземпляр интерфейса
        start_work(serial_number, response, work_ui_instance)

    else: 
        show_error_dialog(f"Деталь c серийным номером {serial_number} не найдена, хотите ее Промаркировать? ", "choice")
        if show_error_dialog:
            start_work(serial_number, mark_ui_instance, response)
        else:
            return

        

        
# 0444390041824