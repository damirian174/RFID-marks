extends HBoxContainer

@onready var button: Button = $MarginContainer/PanelContainer/VBoxContainer/Button
@onready var app: Control = $"../../.."

@onready var model: Label = $MarginContainer2/VBoxContainer/PanelContainer/VBoxContainer/Model
@onready var broken: Label = $MarginContainer2/VBoxContainer/PanelContainer2/VBoxContainer/Broken
@onready var id: Label = $MarginContainer2/VBoxContainer/PanelContainer3/VBoxContainer/Id
@onready var stage: Label = $MarginContainer2/VBoxContainer/PanelContainer4/VBoxContainer/Stage


var mark_active: bool = false:
	set(value):
		mark_active = value
		button.disabled = not value
		if value:
			model.text = 'МЕТРАН 150'
			broken.text = 'False'
			id.text = 'SN1200'
			stage.text = 'Маркировка'
		else:
			model.text = '...'
			broken.text = '...'
			id.text = '...'
			stage.text = '...'


func _on_button_pressed() -> void:
	app.send_mark_signal()
	mark_active = false
