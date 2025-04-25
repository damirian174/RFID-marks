extends MeshInstance3D

@onready var material: StandardMaterial3D

func _ready() -> void:
	material = $MeshInstance3D.mesh.material
	
func change_color_to(color: Color):
	material.albedo_color = color




func _on_scan_area_body_entered(body: Node3D) -> void:
	pass # Replace with function body.
