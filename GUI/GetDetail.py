from database import database
from error_test import show_error_dialog
from config import work, detail

def start_work(ser, mark_ui_instance, response, work_ui_instance):
    work = True
    detail = ser
    mark_ui_instance.detail(response["data"])
    work_ui_instance.start_timer()



def end_work(work_ui_instance):
    work = False
    detail = None
    work_ui_instance.stop_timer()  # Остановка таймера
    work_ui_instance.label.setText("00:00:00")  # Сброс отображаемого времени



def getDetail(serial_number, mark_ui_instance, work_ui_instance):
    data = {"type": "details", "serial": serial_number}
    # data2 = {'name': 'МЕТРАН 150','serial_number': serial_number,'defective':'Да','stage':'Хуй','sector':'аааа'}
    # mark_ui_instance.detail(data2)
    response = database(data)
    if "data" in response:
        # Вызываем метод detail через экземпляр интерфейса
        start_work(serial_number, mark_ui_instance, response, work_ui_instance)

    else: 
        show_error_dialog(f"Деталь c серийным номером {serial_number} не найдена, хотите ее Промаркировать? ")
        if show_error_dialog:
            start_work(serial_number, mark_ui_instance, response)
        else:
            return

        

        
# 0444390041824