from database import database
from error_test import show_error_dialog
from config import work, detail

mark_ui_instance = None
work_ui_instance = None
packing_ui_instance = None
test_ui_instance = None

data_detail = None

def getUI(mark_ui, work_ui, packing_ui, test_ui):
    global mark_ui_instance, work_ui_instance, packing_ui_instance, test_ui_instance
    mark_ui_instance = mark_ui
    work_ui_instance = work_ui
    packing_ui_instance = packing_ui
    test_ui_instance = test_ui
    


def start_work(ser, response):
    global work
    global detail
    work = True
    detail = ser
    global mark_ui_instance, work_ui_instance
    mark_ui_instance.detail(response)
    work_ui_instance.running = True  # Это должно теперь работать
    work_ui_instance.start_timer()


def end_work():
    global work
    global detail
    global data_detail
    data = False
    work = False
    detail = None
    global mark_ui_instance, work_ui_instance
    mark_ui_instance.detail(False)
    work_ui_instance.running = False
    work_ui_instance.stop_timer()  # Остановка таймера
    work_ui_instance.label.setText("00:00:00")  # Сброс отображаемого времени
    print(data_detail["stage"])

    if data_detail["stage"] == "Маркировка":
        response_data = {'type': 'updatestage', 'stage': 'Маркировка', 'serial': data_detail["serial_number"]}
        print(response_data)
        # response = database(response_data)

    

    



def getDetail(serial_number):
    # data = {"type": "details", "serial": serial_number}
    global data_detail
    global mark_ui_instance, work_ui_instance
    data2 = {'name': 'МЕТРАН 150','serial_number': serial_number,'defective':'Да','stage':'Маркировка','sector':'аааа'}
    data_detail = data2
    # mark_ui_instance.detail(data2)
    start_work(data2["serial_number"], data2)
    # response = database(data)
    # if "data" in response:
    #     # Вызываем метод detail через экземпляр интерфейса
    #     start_work(serial_number, response, work_ui_instance)

    # else: 
    #     show_error_dialog(f"Деталь c серийным номером {serial_number} не найдена, хотите ее Промаркировать? ")
    #     if show_error_dialog:
    #         start_work(serial_number, mark_ui_instance, response)
    #     else:
    #         return

        

        
# 0444390041824