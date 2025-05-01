extends PanelContainer

var current_focused_line_edit: LineEdit = null  # Track focused LineEdit


@onready var panel_container: PanelContainer = $"../PanelContainer"
@onready var main_window: MarginContainer = $"../MainWindow"
@onready var app: Control = $".."


@onready var wrong_label: Label = $PanelContainer/VBoxContainer/VBoxContainer/WrongLabel


func _ready():
	# Connect to virtual keyboard signals
	AppManager.virtual_keyboard_press.connect(_on_virtual_key_pressed)
	# Set up initial LineEdit connections
	_connect_line_edits(self)

func _connect_line_edits(node: Node):
	# Recursively connect focus signals for all LineEdits in container
	for child in node.get_children():
		if child is LineEdit:
			if not child.focus_entered.is_connected(_on_line_edit_focus_changed):
				child.focus_entered.connect(_on_line_edit_focus_changed.bind(child))
		if child.get_child_count() > 0:
			_connect_line_edits(child)

func _on_line_edit_focus_changed(line_edit: LineEdit):
	current_focused_line_edit = line_edit

func _on_virtual_key_pressed(key: String):
	if not current_focused_line_edit or not is_instance_valid(current_focused_line_edit):
		return
	
	var line_edit = current_focused_line_edit
	
	# Handle text input
	if key.length() == 1:
		var regex = RegEx.new()
		regex.compile("[A-Za-zА-Яа-я0-9]")  # Support English/Cyrillic/numbers
		if regex.search(key):
			line_edit.text += key
			line_edit.caret_column = line_edit.text.length()
	
	# Handle special keys
	match key:
		"Enter":
			line_edit.release_focus()
			_on_button_pressed()
		"BackSpace":
			if line_edit.text.length() > 0:
				line_edit.text = line_edit.text.substr(0, line_edit.text.length() - 1)
				line_edit.caret_column = line_edit.text.length()
		"Space":
			line_edit.text += " "
			line_edit.caret_column = line_edit.text.length()


func _on_button_pressed() -> void:
	if HumanDb.worker_exists(current_focused_line_edit.text):
		hide()
		panel_container.show()
		main_window.show()
		app.auth = true
		AppManager.authed.emit()
		current_focused_line_edit.text = ''
		current_focused_line_edit = null
		wrong_label.hide()
		
	else:
		wrong_label.show()

func _on_line_edit_focus_entered() -> void:
	#print('hint keyboard')
	AppManager.hint_keyboard.emit()


func _on_line_edit_focus_exited() -> void:
	AppManager.hint_keyboard.emit()
