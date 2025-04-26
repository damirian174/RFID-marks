extends Node

enum DATA_MODES {WRITE, READ}

signal marking_stage_changed(active: bool)
signal data_access(data: rfid_data, mode: DATA_MODES)
