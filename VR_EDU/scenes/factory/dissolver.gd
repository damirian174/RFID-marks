extends Node

@onready var bage: XRToolsPickable = $".."

@onready var mesh_instance_3d_2: MeshInstance3D = $"../MeshInstance3D2"
@onready var mesh_instance_3d: MeshInstance3D = $"../MeshInstance3D"
@onready var vasya: MeshInstance3D = $"../vasya"
@onready var _222444: MeshInstance3D = $"../222444"


func dissolve():
	#return
	var materials: Array[ShaderMaterial] = [
		mesh_instance_3d.get_active_material(0),
		mesh_instance_3d_2.get_active_material(0),
		vasya.get_active_material(0),
		_222444.get_active_material(0),
	]
	
	for i: ShaderMaterial in materials:
		var tween: Tween = create_tween()
		tween.tween_method(
			func (value: float):
				i.set_shader_parameter("dissolveSlider",value),
			1.2,
			-0.5,
			5.0
		).set_ease(Tween.EASE_IN).set_trans(Tween.TRANS_SINE)
		tween.tween_callback(func(): bage.gravity_scale = 1.0)
		


func _ready() -> void:
	vasya.get_active_material(0).set_shader_parameter('baseColorTexture',$"../vasya/SubViewport".get_texture())
	_222444.get_active_material(0).set_shader_parameter('baseColorTexture',$"../222444/SubViewport".get_texture())
	
