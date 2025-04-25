@tool extends CSGPolygon3D

@export_tool_button("Generate Circle") var gen: Callable = generate_circle
@export var radius: float = 10.0
@export var point_count: int = 16

func generate_circle():
	var points = PackedVector2Array()

	for i in range(point_count):
		var angle = i * (2 * PI / point_count)
		points.append(Vector2(radius * cos(angle), radius * sin(angle)))

	# Create a StaticBody2D with collision
	var body = StaticBody2D.new()
	var collision = CollisionPolygon2D.new()
	polygon = points
