extends Area3D



var active = true
@onready var remote_transform_3d: RemoteTransform3D = $RemoteTransform3D


func _on_body_entered(body: Sticker) -> void:
	if not active:
		return
	for i in get_parent().get_children():
		if i != self:
			i.queue_free.call_deferred()
	active = false
	body.get_parent().remove_child(body)
	add_child(body)
	body.position = Vector3.ZERO
	body.rotation = Vector3.ZERO
	body.set_collision_layer_value(17,false)
	#body.freeze_mode = RigidBody3D.FREEZE_MODE_STATIC
	remote_transform_3d.remote_path = body.get_path()
	body.freeze = true
