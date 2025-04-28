@tool
extends Path3D  # Changed from Node3D to Path3D

class_name PathConnector

@export var dynamic_update: bool = true :
	set(value):
		dynamic_update = value
		update_curve()

@export var node_a: Node3D
@export var node_b: Node3D
@export var handle_length: float = 0.5 :
	set(value):
		handle_length = value
		update_curve()

@export var node_a_offset: Vector3 = Vector3.ZERO :
	set(value):
		node_a_offset = value
		update_curve()

@export var node_b_offset: Vector3 = Vector3.ZERO :
	set(value):
		node_b_offset = value
		update_curve()

var _prev_a_transform: Transform3D
var _prev_b_transform: Transform3D
var _curve: Curve3D

func _ready():
	_curve = curve
	update_curve()
	_store_transforms()

func _physics_process(_delta):
	if should_update():
		update_curve()
		_store_transforms()

func should_update() -> bool:
	if not dynamic_update:
		return false
	if Engine.is_editor_hint():
		return (
			node_a.global_transform != _prev_a_transform || 
			node_b.global_transform != _prev_b_transform
		)
	return true

func _store_transforms():
	if node_a:
		_prev_a_transform = node_a.global_transform
	if node_b:
		_prev_b_transform = node_b.global_transform

func update_curve():
	if !is_instance_valid(node_a) || !is_instance_valid(node_b):
		return
	
	if !_curve:
		_curve = Curve3D.new()
		curve = _curve
	
	# Get positions with offset in path's local space
	var a_pos = _get_offset_position(node_a, node_a_offset)
	var b_pos = _get_offset_position(node_b, node_b_offset)
	
	# Get proper forward directions in path's local space
	var a_forward = _get_local_forward(node_a)
	var b_forward = _get_local_forward(node_b)
	
	# Update or create curve points
	if _curve.point_count < 2:
		_curve.clear_points()
		_curve.add_point(a_pos, Vector3.ZERO, a_forward * handle_length)
		_curve.add_point(b_pos, b_forward * handle_length, Vector3.ZERO)
	else:
		_curve.set_point_position(0, a_pos)
		_curve.set_point_out(0, a_forward * handle_length)
		_curve.set_point_position(1, b_pos)
		_curve.set_point_in(1, b_forward * handle_length)
	
	curve.bake_interval = 0.01
	
	if Engine.is_editor_hint():
		curve = _curve.duplicate()

func _get_offset_position(node: Node3D, offset: Vector3) -> Vector3:
	var global_offset_pos = node.global_position + node.global_transform.basis * offset
	return to_local(global_offset_pos)

func _get_local_forward(node: Node3D) -> Vector3:
	# Convert node's forward direction to this Path3D's local space
	var global_forward = -node.global_transform.basis.z  # Godot's forward is -Z
	return global_transform.basis.inverse() * global_forward
