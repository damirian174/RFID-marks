extends Control

@onready var mark: HBoxContainer = $MainWindow/TabContainer/Маркировка

var time: float = 0.0

@export var debug: bool
@onready var time_labels: Array[Label] = [
	$"MainWindow/TabContainer/Маркировка/MarginContainer/PanelContainer/VBoxContainer/Time",
]

func _ready() -> void:
	if debug:
		add_test_window()


func _process(delta: float) -> void:
	time += delta
	
	for label: Label in time_labels:
		label.text = format_mmss()


func format_mmss() -> String:
	return "%02d:%02d" % [int(time) / 60, int(time) % 60]


func add_test_window():
	var questions: Dictionary = mark.get_resource_properties_and_types(rfid_data.new())
	#print(questions)
	var q_window = QuestionWindow.new(questions)
	
	
	add_child(q_window)
	#q_window.submitted.connect(_on_answers)
	q_window.popup_centered()
