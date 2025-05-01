extends Window
class_name QuestionWindow

signal submitted(answers: Dictionary, errors: Dictionary)

var questions_container: VBoxContainer
var questions_pre: Dictionary
var current_focused_line_edit: LineEdit = null  # Track focused LineEdit

var questions: Dictionary = {}:
	set(value):
		questions = value
		_create_question_fields()

func _init(initial_questions: Dictionary = {}):
	size = Vector2i(1000.0, 800.0)
	title = "Маркировать детали"
	add_theme_font_size_override('title_font_size', 40)
	close_requested.connect(queue_free)
	questions_pre = initial_questions

func _ready():
	# Create main margin container
	var margin_container = MarginContainer.new()
	margin_container.size_flags_vertical = Control.SIZE_EXPAND_FILL
	margin_container.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	margin_container.anchor_bottom = 1.0
	margin_container.anchor_top = 0.0
	margin_container.anchor_left = 0.0
	margin_container.anchor_right = 1.0
	add_child(margin_container)
	
	# Set margins to 10 on all sides
	margin_container.add_theme_constant_override("margin_top", 10)
	margin_container.add_theme_constant_override("margin_left", 10)
	margin_container.add_theme_constant_override("margin_right", 10)
	margin_container.add_theme_constant_override("margin_bottom", 10)
	
	# Create main container
	var main_vbox = VBoxContainer.new()
	main_vbox.size_flags_vertical = Control.SIZE_EXPAND_FILL
	main_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	margin_container.add_child(main_vbox)
	
	# Create scroll container
	var scroll = ScrollContainer.new()
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	scroll.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	main_vbox.add_child(scroll)
	
	# Create questions container
	questions_container = VBoxContainer.new()
	questions_container.name = "QuestionsContainer"
	questions_container.size_flags_vertical = Control.SIZE_EXPAND_FILL
	questions_container.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.add_child(questions_container)
	
	questions = questions_pre
	
	AppManager.virtual_keyboard_press.connect(_on_virtual_key_pressed)
	
	# Create submit button
	var submit_button = Button.new()
	submit_button.text = "Подтвердить"
	submit_button.pressed.connect(_on_submit_pressed)
	submit_button.add_theme_font_size_override("font_size", 40)
	main_vbox.add_child(submit_button)
	
	_create_question_fields()
	
	# Set initial focus to first LineEdit
	if questions_container.get_child_count() > 0:
		var first_line_edit = questions_container.get_child(0).get_child(1)
		first_line_edit.grab_focus()

func _create_question_fields():
	if !questions_container:
		return
	
	for child in questions_container.get_children():
		child.queue_free()
	
	for question in questions:
		var vbox = VBoxContainer.new()
		
		var label = Label.new()
		label.text = question
		label.add_theme_font_size_override("font_size", 40)
		vbox.add_child(label)
		
		var line_edit = LineEdit.new()
		line_edit.placeholder_text = _get_type_hint(questions[question])
		line_edit.add_theme_font_size_override("font_size", 40)
		line_edit.add_theme_font_size_override("placeholder_font_size", 40)
		line_edit.focus_entered.connect(_on_line_edit_focus_changed.bind(line_edit))
		vbox.add_child(line_edit)
		
		var error_label = Label.new()
		error_label.add_theme_color_override("font_color", Color.RED)
		error_label.add_theme_font_size_override("font_size", 40)
		error_label.hide()
		vbox.add_child(error_label)
		questions_container.add_child(vbox)

func _on_line_edit_focus_changed(line_edit: LineEdit):
	current_focused_line_edit = line_edit

func _get_type_hint(answer_type: int) -> String:
	match answer_type:
		TYPE_INT: return "Введите целое число"
		TYPE_FLOAT: return "Введите число"
		TYPE_STRING: return "Введите текст"
		TYPE_BOOL: return "Введите 'да' или 'нет'"
		_: return "Enter value"

func _validate_input(text: String, answer_type: int) -> Variant:
	var cleaned = text.strip_edges()
	match answer_type:
		TYPE_STRING:
			return cleaned if len(cleaned) > 0 else null
		TYPE_INT:
			return cleaned.to_int() if cleaned.is_valid_int() else null
		TYPE_FLOAT:
			return cleaned.to_float() if cleaned.is_valid_float() else null
		TYPE_BOOL:
			var lower = cleaned.to_lower()
			if lower in ["true", "да", "1"]: return true
			if lower in ["false", "нет", "0"]: return false
			return null
	return null

func _on_submit_pressed():
	var answers = {}
	var errors = {}
	var container = questions_container
	
	for child in container.get_children():
		var question = child.get_child(0).text
		var input = child.get_child(1) as LineEdit
		var error_label = child.get_child(2) as Label
		var answer_type = questions[question]
		
		var value = _validate_input(input.text, answer_type)
		
		if value == null:
			errors[question] = "Неверный формат"
			error_label.text = "Неверный формат для типа: %s" % _get_type_hint(answer_type)
			error_label.show()
		else:
			answers[question] = value
			error_label.hide()
	
	AppManager.submitted_mark_parameters.emit()
	submitted.emit(answers, errors)
	if errors.is_empty():
		hide()

func _on_virtual_key_pressed(key: String) -> void:
	if not current_focused_line_edit or not is_instance_valid(current_focused_line_edit):
		return
	
	var line_edit = current_focused_line_edit
	
	# Handle letters
	if key.length() == 1:
		var regex = RegEx.new()
		regex.compile("[A-Za-zА-Яа-я0-9]")
		if regex.search(key):
			line_edit.text += key
			line_edit.caret_column = len(line_edit.text)
	
	# Handle Enter
	elif key == "Enter":
		_on_submit_pressed()
	
	elif key == "BackSpace":
		if line_edit.text.length() > 0:
			line_edit.text = line_edit.text.substr(0, line_edit.text.length() - 1)
			line_edit.caret_column = len(line_edit.text)
	
	elif key == 'Space':
		line_edit.text += ' '
		line_edit.caret_column = len(line_edit.text)

func _to_string():
	return "[QuestionWindow:%d]" % get_instance_id()
