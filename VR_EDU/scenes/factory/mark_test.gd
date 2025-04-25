extends Node3D

@onready var коробка_с_отверстиями: MeshInstance3D = $КоробкаСОтверстиями
@onready var computer: Node3D = $Computer


var stage: int = 0:
	set(value):
		stage = value
		if value == 1:
			коробка_с_отверстиями.change_color_to(Color.ORANGE)
			computer.mark_active()
		elif value == 2:
			коробка_с_отверстиями.change_color_to(Color.GREEN)
			await get_tree().create_timer(2.0).timeout
			print('i was green')
			коробка_с_отверстиями.change_color_to(Color.RED)
