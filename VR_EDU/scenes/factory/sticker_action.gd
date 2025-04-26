extends Area3D

@onready var mark_test: Node3D = $"../.."
@onready var container: XRToolsPickable = $".."



func _on_body_entered(body: Node3D) -> void:
	
	if not body.is_in_group("stickers") and true:
		return
	#print(body)
	mark_test.stage = 1.0
	body.queue_free.call_deferred()
	$"../MeshInstance3D2".visible = true
	queue_free.call_deferred()
