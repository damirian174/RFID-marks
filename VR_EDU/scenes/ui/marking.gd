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



#func _ready() -> void:
	#AppManager.data_read.connect()




func _on_button_pressed() -> void:
	if StageManager.current_stage == StageManager.MARK_STAGES.PRESS_MARK_BUTTON:
		StageManager.current_stage = StageManager.MARK_STAGES.SCAN
		AppManager.marking_stage_changed.emit(false)
