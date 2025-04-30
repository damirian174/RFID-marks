extends Node3D


@export var max_speed: float = 2.0
@export var accel: float = 1.0
@export var on: bool = false

var speed: float


@onready var area_3d: Area3D = $Area3D
@onready var material: StandardMaterial3D = $Belt.get_active_material(0)

func _physics_process(delta: float) -> void:
	material.uv1_offset.x += speed * delta / 5.0
	speed = clamp(speed, 0.0, max_speed)
	
	if not on:
		speed -= accel * delta
		
		
		return
	speed += accel * delta
	speed = clamp(speed, 0.0, max_speed)
	#$Belt/StaticBody3D.physics_material_override.friction = lerp(1.0, 0.0,speed/max_speed)
	
	# Convert local direction to global space
	var global_dir = global_transform.basis * Vector3.FORWARD
	for body in area_3d.get_overlapping_bodies():
		if body is RigidBody3D:
			#body.linear_velocity = lerp(body.linear_velocity, speed * -global_dir * 5, 0.5 * delta)
			var force = global_dir * -speed * body.mass * 200
			#print(force)
			body.apply_central_force(force * delta)




func _on_interactable_area_button_button_pressed(_button: Variant) -> void:
	on = not on
