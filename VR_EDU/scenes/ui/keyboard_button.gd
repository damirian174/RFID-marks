extends Button


@export var keyboard_window: Window

func _on_pressed() -> void:
	keyboard_window.visible = not keyboard_window.visible
