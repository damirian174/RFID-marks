extends HBoxContainer

@onready var mark_button: Button = $MarginContainer/PanelContainer/VBoxContainer/VBoxContainer/MarkButton
@onready var read_button: Button = $MarginContainer/PanelContainer/VBoxContainer/VBoxContainer/ReadButton

@onready var app: Control = $"../../.."


@onready var property_container: VBoxContainer = $MarginContainer3/ScrollContainer/PanelContainer/PropertyContainer


const PROPERTY_INFO_PANEL = preload("res://scenes/ui/property_info_panel.tscn")
const ERROR_WINDOW = preload("res://scenes/ui/error_window.tscn")


var data_to_write_id: String



func _ready() -> void:
	AppManager.data_access.connect(readwrite_data)
	#print(get_resource_properties(rfid_data.new()))


func readwrite_data(body_with_data: Sticker, mode: AppManager.DATA_MODES):
	#print(mode,AppManager.DATA_MODES)
	if mode == AppManager.DATA_MODES.READ:
		for i: PanelContainer in property_container.get_children():
			i.queue_free()
		if StickerDb.get_data_by_id(body_with_data.data_id) == null:
			#print('data is seeemingly null')
			
			var properties: Dictionary = get_resource_properties(rfid_data.new())
			for property_name in properties:
				var new_property_container: PanelContainer = PROPERTY_INFO_PANEL.instantiate()
				property_container.add_child(new_property_container)
				new_property_container.header = str(property_name)
				new_property_container.value = 'Неизвестно'
				
		else:
			#print('data is not null')
			var properties: Dictionary = get_resource_properties(StickerDb.get_data_by_id(body_with_data.data_id))
			for property_name in properties:
				var new_property_container: PanelContainer = PROPERTY_INFO_PANEL.instantiate()
				property_container.add_child(new_property_container)
				new_property_container.header = property_name
				new_property_container.value = str(properties[property_name])
				
	elif mode == AppManager.DATA_MODES.WRITE:
		body_with_data.data_id = data_to_write_id


func _on_mark_button_pressed() -> void:
	AppManager.set_data_access.emit(AppManager.DATA_MODES.REST)
	var questions: Dictionary = get_resource_properties_and_types(rfid_data.new())
	#print(questions)
	var q_window = QuestionWindow.new(questions)
	
	
	add_child(q_window)
	q_window.submitted.connect(_on_answers)
	q_window.popup_centered()
	


func _on_read_button_pressed() -> void:
	for child in get_children():
		if child is Window:
			child.queue_free()
	AppManager.set_data_access.emit(AppManager.DATA_MODES.READ)

func _on_answers(answers: Dictionary, errors: Dictionary):
	if errors.size() != 0:
		return
	var data_to_write: rfid_data = rfid_data.new()
	
	for property: String in answers:
		data_to_write.set(property,answers[property])
	data_to_write_id = data_to_write.data_id
	#print(data_to_write)
	
	var error: Error = StickerDb.add_data(data_to_write)
	
	if error:
		var error_message: Window = ERROR_WINDOW.instantiate()
		#error_message.label.text = 'Такой идентификационный номер уже существует. Попробуйте '+StickerDb.generate_unique_id()
		#error_message.dialog_text = 'Такой идентификационный номер уже существует. Попробуйте '+StickerDb.generate_unique_id()
		add_child(error_message)
		error_message.label.text = '[center]Такой идентификационный номер уже существует. Попробуйте [color=#FFA500]'+StickerDb.generate_unique_id() + '[/color][/center]'

		#error_message.popup_centered()
	
	else:
		AppManager.set_data_access.emit(AppManager.DATA_MODES.WRITE)

func get_resource_properties(res: Resource) -> Dictionary:
	
	var properties := {}
	for property in res.get_property_list():
		#print(property)
		var property_name: String = property["name"]
		# Filter out built-in properties and methods
		if property_name.begins_with("_"):
			continue
		if property["usage"] & PROPERTY_USAGE_SCRIPT_VARIABLE:
			properties[property_name] = res.get(property_name)
			
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
