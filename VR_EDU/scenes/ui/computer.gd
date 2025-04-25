extends Node3D

signal mark_done
@onready var viewport_2_din_3d: XRToolsViewport2DIn3D = $Viewport2Din3D
@onready var mark_test: Node3D = $".."


func _ready() -> void:
	viewport_2_din_3d.get_child(0).get_child(0).mark_ready.connect(change_stage_to_2)
	

func mark_active():
	viewport_2_din_3d.get_child(0).get_child(0).change_mark_to_active()


func change_stage_to_2():
	mark_test.stage = 2
