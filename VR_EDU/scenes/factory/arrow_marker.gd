@tool
extends MeshInstance3D

var tween: Tween
var is_tweening: bool = false

@export var target_node: Node3D:
	set(value):
		var old_target = target_node
		target_node = value
		if value == null:
			visible = false
			if tween:
				tween.kill()
				tween = null
				is_tweening = false
		else:
			visible = true
			if old_target != null and old_target != value:
				# Start tween between previous and new target
				is_tweening = true
				var start_transform = global_transform
				var end_transform = Transform3D(
					value.global_transform.basis,
					value.global_transform.origin + value.global_transform.basis.y * vertical_offset
				)
				
				if tween:
					tween.kill()
				tween = create_tween()
				tween.set_ease(Tween.EASE_IN_OUT)
				tween.set_trans(Tween.TRANS_QUAD)
				tween.tween_method(_update_transform, start_transform, end_transform, 0.5)
				tween.finished.connect(_on_tween_finished)
			else:
				calculate_transform()

@export var vertical_offset: float = 1.0:
	set(value):
		vertical_offset = value
		if target_node:
			calculate_transform()

var _last_target_transform: Transform3D

func _process(_delta: float) -> void:
	if not target_node or is_tweening:
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

func _update_transform(transform: Transform3D):
	global_transform = transform

func _on_tween_finished():
	is_tweening = false
	calculate_transform()  # Ensure final position matches exactly
	tween = null
