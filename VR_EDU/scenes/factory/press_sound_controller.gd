extends Node

@onready var press_sound: AudioStreamPlayer3D = $"../PressSound"
@onready var un_press_sound: AudioStreamPlayer3D = $"../UnPressSound"



func _on_interactable_area_button_button_pressed(button: Variant) -> void:
	press_sound.play()


func _on_interactable_area_button_button_released(button: Variant) -> void:
	un_press_sound.play()
