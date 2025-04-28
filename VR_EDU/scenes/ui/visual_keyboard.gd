extends Window

@onready var digits: HBoxContainer = $Control/Buttons/Digits
@onready var eng_letters: VBoxContainer = $Control/Buttons/EngLetters
@onready var ru_letters: VBoxContainer = $Control/Buttons/RuLetters
@onready var enter: Button = $Control/Buttons/Buttons/Enter
@onready var back_space: Button = $Control/Buttons/Buttons/BackSpace
@onready var space: Button = $Control/Buttons/Buttons/Space


@onready var lang: Button = $Control/Buttons/Buttons/Lang

var conserned_buttons: Array[Button] = []

func _on_close_requested() -> void:
	hide()
	

func _ready() -> void:
	
	
	
	conserned_buttons.append_array(digits.get_children())
	for i in eng_letters.get_children():
		conserned_buttons.append_array(i.get_children())
	for i in ru_letters.get_children():
		conserned_buttons.append_array(i.get_children())
	conserned_buttons.append(enter)
	conserned_buttons.append(back_space)
	conserned_buttons.append(space)
	for button: Button in conserned_buttons:
		button.pressed.connect(func(): AppManager.virtual_keyboard_press.emit(button.text))
	
	conserned_buttons.pop_back()
	conserned_buttons.pop_back()
	conserned_buttons.pop_back()
	
	#AppManager.virtual_keyboard_press.connect(func(key): print(key))
	#popup_centered()

func _on_caps_pressed() -> void:
	for i: Button in conserned_buttons:
		if i.text.to_lower() == i.text:
			i.text = i.text.to_upper()
		else:
			i.text = i.text.to_lower()


func _on_lang_pressed() -> void:
	if lang.text == 'RU':
		lang.text = 'ENG'
		ru_letters.hide()
		eng_letters.show()
	elif lang.text == 'ENG':
		lang.text = 'RU'
		ru_letters.show()
		eng_letters.hide()
