extends Node

enum DATA_MODES {WRITE, READ}

signal set_data_access(mode: DATA_MODES)
signal data_access(data: rfid_data, mode: DATA_MODES)
