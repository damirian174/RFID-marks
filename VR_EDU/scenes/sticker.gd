@tool
class_name Sticker extends XRToolsPickable

const STICKER_SHAPE = preload("res://resources/sticker_shape.tres")
const STICKER_MESH = preload("res://resources/sticker_mesh.tres")


func _ready() -> void:
	super()
	var new_meshinstance: MeshInstance3D = MeshInstance3D.new()
	var new_coll: CollisionShape3D = CollisionShape3D.new()
	new_meshinstance.mesh = STICKER_MESH
	new_coll.shape = STICKER_SHAPE
	freeze_mode = RigidBody3D.FREEZE_MODE_KINEMATIC
	collision_layer = DEFAULT_LAYER
	add_child(new_meshinstance)
	add_child(new_coll)
	add_to_group("stickers")
	
