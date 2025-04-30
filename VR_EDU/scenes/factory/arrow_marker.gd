@tool
extends MeshInstance3D

@export var target_node: Node3D:
	set(value):
		target_node = value
		if value == null:
			visible = false
		else:
			visible = true
			calculate_transform()

@export var vertical_offset: float = 1.0:
	set(value):
		vertical_offset = value
		if target_node:
			calculate_transform()

var _last_target_transform: Transform3D

func _process(delta: float) -> void:
	if not target_node:
		return
	
	# Only update if transform changed
	if target_node.global_transform != _last_target_transform:
		calculate_transform()


func calculate_transform():
	if not target_node.is_inside_tree():
		return
	# Calculate new position with vertical offset
	var new_position: Vector3 = target_node.global_transform.origin + target_node.global_transform.basis.y * vertical_offset
	# Update our transform while maintaining target rotation
	global_transform = Transform3D(target_node.global_transform.basis, new_position)
	_last_target_transform = target_node.global_transform
