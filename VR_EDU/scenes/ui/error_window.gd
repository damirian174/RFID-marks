extends Window


@onready var label: RichTextLabel = $Control/MarginContainer/VBoxContainer/RichTextLabel



func _on_close_requested() -> void:
	
	queue_free.call_deferred()



func _ready() -> void:
	popup_centered()


func _on_button_pressed() -> void:
	queue_free.call_deferred()
