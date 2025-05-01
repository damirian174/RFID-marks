extends MarginContainer

@onready var app: Control = $"../../../.."

@onready var panel_container: PanelContainer = $"../../../../PanelContainer"
@onready var main_window: MarginContainer = $"../../.."
@onready var login: PanelContainer = $"../../../../Login"
@onready var block_input: ColorRect = $"../../../../BlockInput"

var elapsed_seconds: int = 0

func _on_error_pressed() -> void:
	pass # Replace with function body.


func _on_take_a_nap_pressed() -> void:
	app.napping = true
	var window = Window.new()
	window.size = Vector2i(400, 300)
	window.title = "Timed Window"
	window.unresizable = true
	#window.popup_centered()
	
	var center_container = CenterContainer.new()
	center_container.anchor_bottom = 1.0
	center_container.anchor_left = 0.0
	center_container.anchor_right = 1.0
	center_container.anchor_top = 0.0
	center_container.size_flags_vertical = Control.SIZE_EXPAND_FILL
	center_container.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	window.add_child(center_container)
	
	var vbox = VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 20)
	center_container.add_child(vbox)
	
	var label = Label.new()
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.add_theme_font_size_override("font_size", 40)
	label.text = "Вы отошли на:"
	label.add_theme_font_size_override("font_size", 24)
	vbox.add_child(label)
	
	var time_label = Label.new()
	time_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	time_label.add_theme_font_size_override("font_size", 40)
	time_label.text = "00:00"
	time_label.add_theme_font_size_override("font_size", 32)
	vbox.add_child(time_label)
	
	var button = Button.new()
	button.add_theme_font_size_override("font_size", 40)
	button.text = "Продолжить"
	var close: Callable = func(): 
		block_input.hide() 
		window.queue_free()
		app.napping = false
		elapsed_seconds = 0.0
	
	button.pressed.connect(close)
	window.close_requested.connect(close)
	button.add_theme_font_size_override("font_size", 20)
	vbox.add_child(button)
	
	# Timer logic
	var timer = Timer.new()
	
	timer.wait_time = 1.0
	timer.autostart = true
	timer.one_shot = false  # Critical fix here
	timer.timeout.connect(func():
		elapsed_seconds += 1
		#print(elapsed_seconds)
		var minutes = elapsed_seconds / 60
		var seconds = elapsed_seconds % 60
		time_label.text = "%02d:%02d" % [minutes, seconds]
	)
	window.add_child(timer)
	
	block_input.show()
	app.add_child(window)
	window.popup_centered()
	#get_tree().current_scene.add_child(window)



func _on_end_work_pressed() -> void:
	app.tutorial = false
	app.auth = false
	app.time = 0.0
	AppManager.set_data_access.emit(AppManager.DATA_MODES.REST)
	AppManager.authed.emit()
	panel_container.hide()
	main_window.hide()
	login.show()
	


func _on_broke_pressed() -> void:
	pass # Replace with function body.
