extends Window
class_name QuestionWindow

signal submitted(answers: Dictionary, errors: Dictionary)

var questions_container: VBoxContainer

var questions_pre: Dictionary

var questions: Dictionary = {}:
	set(value):
		questions = value
		#print(value)
		_create_question_fields()

func _init(initial_questions: Dictionary = {}):
	size = Vector2i(500, 400)
	title = "Маркировать детали"
	close_requested.connect(queue_free)
	questions_pre = initial_questions

func _ready():
	# Create main container
	var main_vbox = VBoxContainer.new()
	main_vbox.size_flags_vertical = Control.SIZE_EXPAND_FILL
	main_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	main_vbox.anchor_bottom = 1.0
	main_vbox.anchor_top = 0.0
	main_vbox.anchor_left = 0.0
	main_vbox.anchor_right = 1.0
	add_child(main_vbox)
	
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
	
	# Create submit button
	var submit_button = Button.new()
	submit_button.text = "Submit Answers"
	submit_button.pressed.connect(_on_submit_pressed)
	submit_button.add_theme_font_size_override("font_size", 25)  # ADDED
	main_vbox.add_child(submit_button)
	
	# Initial field creation
	_create_question_fields()

func _create_question_fields():
	
	if !questions_container:
		return
	
	# Clear old fields
	for child in questions_container.get_children():
		child.queue_free()
	
	# Create new fields
	for question in questions:
		
		var vbox = VBoxContainer.new()
		
		# Question label
		var label = Label.new()
		label.text = question
		label.add_theme_font_size_override("font_size", 25)  # ADDED
		vbox.add_child(label)
		
		# Answer input
		var line_edit = LineEdit.new()
		line_edit.placeholder_text = _get_type_hint(questions[question])
		line_edit.add_theme_font_size_override("font_size", 25)  # ADDED
		line_edit.add_theme_font_size_override("placeholder_font_size", 25)  # ADDED
		vbox.add_child(line_edit)
		
		# Error label
		var error_label = Label.new()
		error_label.add_theme_color_override("font_color", Color.RED)
		error_label.add_theme_font_size_override("font_size", 25)  # ADDED
		error_label.hide()
		vbox.add_child(error_label)
		questions_container.add_child(vbox)

func _get_type_hint(answer_type: int) -> String:
	match answer_type:
		TYPE_INT: return "Enter a whole number (e.g., 42)"
		TYPE_FLOAT: return "Enter a decimal number (e.g., 3.14)"
		TYPE_STRING: return "Enter text"
		TYPE_BOOL: return "Enter 'true' or 'false'"
		_: return "Enter value"

func _validate_input(text: String, answer_type: int) -> Variant:
	var cleaned = text.strip_edges()
	
	match answer_type:
		TYPE_STRING:
			return cleaned
		TYPE_INT:
			return cleaned.to_int() if cleaned.is_valid_int() else null
		TYPE_FLOAT:
			return cleaned.to_float() if cleaned.is_valid_float() else null
		TYPE_BOOL:
			var lower = cleaned.to_lower()
			if lower in ["true", "yes", "1"]: return true
			if lower in ["false", "no", "0"]: return false
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
			errors[question] = "Invalid format"
			error_label.text = "Invalid format for type: %s" % _get_type_hint(answer_type)
			error_label.show()
		else:
			answers[question] = value
			error_label.hide()
	
	submitted.emit(answers, errors)
	if errors.is_empty():
		hide()

func _to_string():
	return "[QuestionWindow:%d]" % get_instance_id()
