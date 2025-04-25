@tool
extends Node3D

@onready var neck: CSGPolygon3D = $Neck

@export var dynamic_update: bool = true :
	set(value):
		dynamic_update = value
		update_curve()

@export var base: Node3D
@export var head: Node3D
@export var path_node: Path3D
@export var handle_length: float = 0.5 :
	set(value):
		handle_length = value
		update_curve()

@export var head_back_offset: Vector3 = Vector3(0, 0, -0.1) :
	set(value):
		head_back_offset = value
		update_curve()

var _prev_base_transform: Transform3D
var _prev_head_transform: Transform3D
var _curve: Curve3D
var _path_offset: Vector3

func _ready():
	_curve = path_node.curve
	_path_offset = path_node.position
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
			base.transform != _prev_base_transform || 
			head.transform != _prev_head_transform
		)
	return true

func _store_transforms():
	_prev_base_transform = base.transform
	_prev_head_transform = head.transform

func update_curve():
	if not is_instance_valid(base) or not is_instance_valid(head) or not is_instance_valid(path_node):
		return
	
	if !_curve:
		_curve = Curve3D.new()
		path_node.curve = _curve
	
	# Cache frequently used values
	var base_pos = base.position - _path_offset
	var base_basis_y = base.transform.basis.y
	var head_basis = head.transform.basis
	
	# Calculate head position with single basis operation
	var head_back = head.position + head_basis * head_back_offset
	var head_back_pos = head_back - _path_offset
	var head_basis_y = head_basis.y
	
	# Update curve points with direct handle calculations
	if _curve.point_count < 2:
		_curve.clear_points()
		_curve.add_point(base_pos, Vector3.ZERO, base_basis_y * handle_length)
		_curve.add_point(head_back_pos, head_basis_y * handle_length, Vector3.ZERO)
	else:
		_curve.set_point_position(0, base_pos)
		_curve.set_point_out(0, base_basis_y * handle_length)
		_curve.set_point_position(1, head_back_pos)
		_curve.set_point_in(1, head_basis_y * handle_length)
	
	# Optimized editor refresh
	if Engine.is_editor_hint():
		path_node.curve = _curve.duplicate()
