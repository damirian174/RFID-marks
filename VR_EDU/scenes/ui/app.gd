extends Control

@onready var маркировка: HBoxContainer = $MainWindow/TabContainer/Маркировка
signal mark_ready

func send_mark_signal():
	mark_ready.emit()

func change_mark_to_active():
	маркировка.mark_active = true
