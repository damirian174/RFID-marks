extends HBoxContainer

@onready var mark_button: Button = $MarginContainer/PanelContainer/VBoxContainer/VBoxContainer/MarkButton
@onready var read_button: Button = $MarginContainer/PanelContainer/VBoxContainer/VBoxContainer/ReadButton

@onready var app: Control = $"../../.."

@onready var property_container: VBoxContainer = $MarginContainer2/ScrollContainer/PropertyContainer

const PROPERTY_INFO_PANEL = preload("res://scenes/ui/property_info_panel.tscn")



var data_to_write: rfid_data



func _ready() -> void:
	AppManager.data_access.connect(readwrite_data)
	#print(get_resource_properties(rfid_data.new()))


func readwrite_data(data: rfid_data, mode: AppManager.DATA_MODES):
	#print(mode,AppManager.DATA_MODES)
	if mode == AppManager.DATA_MODES.READ:
		#print_debug('reading instead')
		if data == null:
			var properties: Dictionary = get_resource_properties(rfid_data.new())
			for property_name in properties:
				var new_property_container: PanelContainer = PROPERTY_INFO_PANEL.instantiate()
				property_container.add_child(new_property_container)
				new_property_container.header = str(property_name)
				new_property_container.value = 'Неизвестно'
				
		else:
			var properties: Dictionary[String, Variant] = get_resource_properties(data)
			for property_name in properties:
				var new_property_container: PanelContainer = PROPERTY_INFO_PANEL.instantiate()
				property_container.add_child(new_property_container)
				new_property_container.header = property_name
				new_property_container.value = properties[property_name]
				
	elif mode == AppManager.DATA_MODES.WRITE:
		data = data_to_write






func _on_mark_button_pressed() -> void:
	var questions: Dictionary = get_resource_properties_and_types(rfid_data.new())
	#print(questions)
	var q_window = QuestionWindow.new(questions)
	
	
	add_child(q_window)
	q_window.submitted.connect(_on_answers)
	q_window.popup_centered()
	


func _on_read_button_pressed() -> void:
	AppManager.set_data_access.emit(AppManager.DATA_MODES.READ)

func _on_answers(answers: Dictionary, errors: Dictionary):
	if errors.size() != 0:
		return
	data_to_write = rfid_data.new()
	for property: String in answers:
		data_to_write.set(property,answers[property])
	#print_debug('sending a signal to start writing')
	AppManager.set_data_access.emit(AppManager.DATA_MODES.WRITE)

func get_resource_properties(res: Resource) -> Dictionary:
	
	var properties := {}
	for property in res.get_property_list():
		#print(property)
		var name: String = property["name"]
		# Filter out built-in properties and methods
		if name.begins_with("_"):
			continue
		if property["usage"] & PROPERTY_USAGE_SCRIPT_VARIABLE:
			properties[name] = res.get(name)
			
	return properties


func get_resource_properties_and_types(resource: Resource) -> Dictionary:
	var properties := {}
	
	for prop in resource.get_property_list():
		var usage: int = prop.get("usage", 0)
		# Skip category/group entries and non-String/int properties
		if (usage & PROPERTY_USAGE_SCRIPT_VARIABLE):
			
			var prop_name: String = prop["name"]
			var type: int = prop["type"]
			
			# Only handle String and int types
			match type:
				TYPE_STRING, TYPE_INT,TYPE_BOOL:
					properties[prop_name] = type
				_:
					continue  # Skip other types entirely
	
	return properties
