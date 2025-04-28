@tool
extends Path3D

@export var start_target: NodePath
@export var end_target: NodePath
@export var curvature_strength: float = 0.25 :
	set(value):
		curvature_strength = value
		update_curve()

func _ready():
	if Engine.is_editor_hint():
		update_curve()

func _process(_delta):
	update_curve()

func update_curve():
	var start_node = get_node_or_null(start_target) as Node3D
	var end_node = get_node_or_null(end_target) as Node3D
	
	if not start_node or not end_node:
		return
	
	var new_curve = Curve3D.new()
	
	# Get global positions and convert to local space
	var global_start = start_node.global_transform.origin
	var global_end = end_node.global_transform.origin
	var local_start = to_local(global_start)
	var local_end = to_local(global_end)
	
	# Calculate handle positions in global space
	var distance = global_start.distance_to(global_end)
	var handle_offset = Vector3.UP * curvature_strength * distance
	
	# Convert handles to local space
	var start_handle = to_local(global_start + handle_offset) - local_start
	var end_handle = to_local(global_end + handle_offset) - local_end
	
	# Add points with Bézier handles
	new_curve.add_point(local_start, Vector3.ZERO, start_handle)
	new_curve.add_point(local_end, end_handle, Vector3.ZERO)
	
	curve = new_curve
