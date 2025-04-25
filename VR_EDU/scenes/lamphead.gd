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

func _ready():
	update_curve()
	_store_transforms()

func _physics_process(_delta):
	if should_update():
		
		update_curve()
		_store_transforms()
		#neck.scale = Vector3.ONE / scale
		

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
	
	var curve = path_node.curve
	if not curve:
		return
	
	# Path's local offset from parent
	var path_offset = path_node.position
	
	# Base point calculation
	var base_pos = base.position - path_offset
	var base_handle = base.position + base.transform.basis.y * handle_length - path_offset
	
	# Head point calculation with 3D offset
	var head_back = head.position + head.transform.basis * head_back_offset
	var head_back_pos = head_back - path_offset
	var head_handle = head_back + -head.transform.basis.y * handle_length - path_offset
	
	# Update curve points
	if curve.point_count < 2:
		curve.clear_points()
		curve.add_point(base_pos, Vector3.ZERO, base_handle - base_pos)
		curve.add_point(head_back_pos, head_back_pos - head_handle, Vector3.ZERO)
	else:
		curve.set_point_position(0, base_pos)
		curve.set_point_out(0, base_handle - base_pos)
		curve.set_point_position(1, head_back_pos)
		curve.set_point_in(1, head_back_pos - head_handle)
	
	# Force editor refresh
	if Engine.is_editor_hint():
		path_node.curve = curve.duplicate()
