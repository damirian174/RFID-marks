extends Control

@onready var mark: HBoxContainer = $MainWindow/TabContainer/Маркировка



@export var debug: bool


func _ready() -> void:
	if debug:
		add_test_window()



func add_test_window():
	var questions: Dictionary = mark.get_resource_properties_and_types(rfid_data.new())
	#print(questions)
	var q_window = QuestionWindow.new(questions)
	
	
	add_child(q_window)
	#q_window.submitted.connect(_on_answers)
	q_window.popup_centered()
