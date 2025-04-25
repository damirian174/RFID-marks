extends Path3D

@export var object_a: Node3D
@export var object_b: Node3D
@export var line_width: float = 0.1
@export var color: Color = Color.WHITE

var mesh_instance: MeshInstance3D
var immediate_mesh: ImmediateMesh
var material: StandardMaterial3D

func _ready():
	# Verify curve has at least 2 points
	if curve.get_point_count() < 2:
		curve.add_point(Vector3.ZERO)
		curve.add_point(Vector3(0, 0, 1))
	
	# Setup visualization
	mesh_instance = MeshInstance3D.new()
	add_child(mesh_instance)
	
	immediate_mesh = ImmediateMesh.new()
	mesh_instance.mesh = immediate_mesh
	
	material = StandardMaterial3D.new()
	material.albedo_color = color
	material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	material.cull_mode = BaseMaterial3D.CULL_DISABLED
	#material.double_sided = true
	mesh_instance.material_override = material

func _process(_delta):
	if !object_a || !object_b:
		return
	
	# Update path endpoints with object transforms
	update_curve_points()
	
	# Generate points along the curve with rotations
	var curve_data = []
	var baked_length = curve.get_baked_length()
	for i in range(20):
		var t = i / 19.0
		var transform = curve.sample_baked_with_rotation(t * baked_length)
		curve_data.append({
			"position": transform.origin,
			"tangent": transform.basis.z
		})
	
	# Draw the billboarded line
	draw_billboarded_curve(curve_data)

func update_curve_points():
	# Update first point with object_a's transform
	var a_transform = object_a.global_transform
	curve.set_point_position(0, a_transform.origin)
	var a_forward = -a_transform.basis.z * 1.0
	curve.set_point_out(0, a_forward)
	
	# Update last point with object_b's transform
	var last_idx = curve.get_point_count() - 1
	var b_transform = object_b.global_transform
	curve.set_point_position(last_idx, b_transform.origin)
	var b_backward = b_transform.basis.z * 1.0
	curve.set_point_in(last_idx, b_backward)

func draw_billboarded_curve(curve_data: Array):
	immediate_mesh.clear_surfaces()
	immediate_mesh.surface_begin(Mesh.PRIMITIVE_TRIANGLE_STRIP)
	
	var camera = get_viewport().get_camera_3d()
	var cam_pos = camera.global_transform.origin if camera else Vector3.ZERO
	
	for data in curve_data:
		var point_pos = data.position
		var tangent = data.tangent
		var to_camera = cam_pos - point_pos
		
		# Calculate billboarded right vector
		var right = tangent.cross(to_camera)
		if right.length() < 0.001:
			right = tangent.cross(Vector3.UP)
		right = right.normalized() * line_width
		
		immediate_mesh.surface_set_color(color)
		immediate_mesh.surface_add_vertex(point_pos + right)
		immediate_mesh.surface_add_vertex(point_pos - right)
	
	immediate_mesh.surface_end()
