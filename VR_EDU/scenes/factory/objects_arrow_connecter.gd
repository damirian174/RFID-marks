@tool
extends Path3D

## Target objects to connect between
@export var object_a: Node3D
@export var object_b: Node3D

## Line visual properties
@export var line_width: float = 0.1
@export var color: Color = Color.WHITE:
	set(value):
		color = value
		if _material:
			_material.albedo_color = color
@export var point_count: int = 20:
	set(value):
		point_count = clamp(value, 2, 100)
		_should_redraw = true

## Texture properties
@export var line_texture: Texture2D:
	set(value):
		line_texture = value
		if _material:
			_material.albedo_texture = value
@export var texture_scale: Vector2 = Vector2(1, 1):
	set(value):
		texture_scale = value
		if _material:
			_material.uv1_scale = Vector3(texture_scale.x, texture_scale.y, 1)
@export var texture_offset: Vector2 = Vector2.ZERO:
	set(value):
		texture_offset = value
		if _material:
			_material.uv1_offset = Vector3(texture_offset.x, texture_offset.y, 0)

## Material properties
@export_enum("Opaque", "Alpha", "Alpha Scissor", "Alpha Hash") var alpha_mode: int = 1:
	set(value):
		alpha_mode = value
		if _material:
			_configure_alpha_mode()
@export var metallic: float = 0.0:
	set(value):
		metallic = value
		if _material:
			_material.metallic = metallic
@export var roughness: float = 1.0:
	set(value):
		roughness = value
		if _material:
			_material.roughness = roughness

var _mesh_instance: MeshInstance3D
var _immediate_mesh: ImmediateMesh
var _material: StandardMaterial3D
var _prev_a_transform: Transform3D
var _prev_b_transform: Transform3D
var _should_redraw: bool = true

@onready var _camera: Camera3D = get_viewport().get_camera_3d()

func _ready() -> void:
	if not is_inside_tree():
		await ready
	
	if curve.get_point_count() < 2:
		curve.add_point(Vector3.ZERO)
		curve.add_point(Vector3(0, 0, 1))
	
	_mesh_instance = MeshInstance3D.new()
	_mesh_instance.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(_mesh_instance)
	
	_immediate_mesh = ImmediateMesh.new()
	_mesh_instance.mesh = _immediate_mesh
	
	_material = StandardMaterial3D.new()
	_configure_material()
	_mesh_instance.material_override = _material
	
	_capture_transforms()
	update_curve()

func _configure_material() -> void:
	_material.albedo_color = color
	_material.albedo_texture = line_texture
	_material.shading_mode = StandardMaterial3D.SHADING_MODE_UNSHADED
	_material.cull_mode = StandardMaterial3D.CULL_DISABLED
	_material.uv1_scale = Vector3(texture_scale.x, texture_scale.y, 1)
	_material.uv1_offset = Vector3(texture_offset.x, texture_offset.y, 0)
	_material.metallic = metallic
	_material.roughness = roughness
	_configure_alpha_mode()

func _configure_alpha_mode() -> void:
	match alpha_mode:
		0: # Opaque
			_material.transparency = StandardMaterial3D.TRANSPARENCY_DISABLED
		1: # Alpha
			_material.transparency = StandardMaterial3D.TRANSPARENCY_ALPHA
		2: # Alpha Scissor
			_material.transparency = StandardMaterial3D.TRANSPARENCY_ALPHA_SCISSOR
		3: # Alpha Hash
			_material.transparency = StandardMaterial3D.TRANSPARENCY_ALPHA_HASH

# Rest of the code remains the same until _draw_billboarded_curve

func _draw_billboarded_curve() -> void:
	_immediate_mesh.clear_surfaces()
	if not _should_update():
		return
	
	var baked_length: float = curve.get_baked_length()
	var curve_data: Array[Dictionary] = []
	
	for i in point_count:
		var t: float = i / float(point_count - 1)
		var transform: Transform3D = curve.sample_baked_with_rotation(t * baked_length)
		curve_data.append({
			"position": transform.origin,
			"tangent": transform.basis.z
		})
	
	var cam_pos: Vector3 = _camera.global_position
	
	_immediate_mesh.surface_begin(Mesh.PRIMITIVE_TRIANGLE_STRIP, _material)
	
	for data in curve_data:
		var point_pos: Vector3 = data.position
		var tangent: Vector3 = data.tangent
		var to_camera: Vector3 = cam_pos - point_pos
		
		var right: Vector3 = tangent.cross(to_camera)
		if right.length() < 0.001:
			right = tangent.cross(Vector3.UP)
		right = right.normalized() * line_width
		
		var uv_x: float = float(curve_data.find(data)) / (point_count - 1)
		_immediate_mesh.surface_set_uv(Vector2(uv_x, 0))
		_immediate_mesh.surface_add_vertex(point_pos + right)
		
		_immediate_mesh.surface_set_uv(Vector2(uv_x, 1))
		_immediate_mesh.surface_add_vertex(point_pos - right)
	
	_immediate_mesh.surface_end()
