from database import database

def getDetail(serial_number, mark_ui_instance):
    data = {"type": "details", "serial": serial_number}
    # data2 = {'name': 'МЕТРАН 150','serial_number': serial_number,'defective':'Да','stage':'Хуй','sector':'аааа'}
    # mark_ui_instance.detail(data2)
    response = database(data)
    if "data" in response:
        # Вызываем метод detail через экземпляр интерфейса
        mark_ui_instance.detail(response["data"])
# 0444390041824