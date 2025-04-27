@tool
class_name Sticker extends XRToolsPickable

@export var data_id: String

const STICKER_SHAPE = preload("res://resources/sticker_shape.tres")
const STICKER_MESH = preload("res://resources/sticker_mesh.tres")

const STICKER_DEFAULT_LAYER: int = 0b0000_0000_0000_0001_1100_0000_0000_0000
const STICKER_PICKED_UP_LAYER: int = 0b0000_0000_0000_0001_1000_0000_0000_0000


func _ready() -> void:
	super()
	var new_meshinstance: MeshInstance3D = MeshInstance3D.new()
	var new_coll: CollisionShape3D = CollisionShape3D.new()
	new_meshinstance.mesh = STICKER_MESH
	new_coll.shape = STICKER_SHAPE
	freeze_mode = RigidBody3D.FREEZE_MODE_KINEMATIC
	
	collision_layer = STICKER_DEFAULT_LAYER
	picked_up_layer = STICKER_PICKED_UP_LAYER
	#set_collision_layer_value(16,true)
	
	add_child(new_meshinstance)
	add_child(new_coll)
	add_to_group("stickers")
	

#func _process(delta: float) -> void:
	#if Engine.is_editor_hint():
		#return
	#
	#print(global_position)
