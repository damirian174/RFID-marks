extends Node3D


@onready var things: Array[Node] = get_children()


func _on_timer_timeout() -> void:
	for i in things:
		var new_tween = i.create_tween()
		new_tween.tween_property(i,"rotation:x",i.rotation.x + 2*PI, 1.0).set_trans(Tween.TRANS_LINEAR)
		
