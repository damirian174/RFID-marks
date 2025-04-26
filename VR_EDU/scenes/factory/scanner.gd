extends MeshInstance3D


enum STATES {OFF, NOT_ACCEPTING, ACCEPTING_READ, ACCEPTING_WRITE, ACCEPTED}

const colors: Dictionary[STATES,Color] = {
	STATES.OFF: Color.BLACK,
	STATES.NOT_ACCEPTING: Color.RED,
	STATES.ACCEPTING_READ: Color.AQUA,
	STATES.ACCEPTING_WRITE: Color.AQUA,
	STATES.ACCEPTED: Color.GREEN,
}

@onready var material: StandardMaterial3D


var state: STATES = STATES.NOT_ACCEPTING:
	set(new_state):
		#print(STATES)
		state = new_state
		change_color_to(colors[state])
		


func _ready() -> void:
	material = $MeshInstance3D.mesh.material
	AppManager.set_data_access.connect(change_scan_state)
	
	
	
func change_color_to(color: Color):
	if state == STATES.OFF:
		return
	material.albedo_color = color




func change_scan_state(mode: AppManager.DATA_MODES):
	if state == STATES.OFF:
		return
	if mode == AppManager.DATA_MODES.READ:
		#print_debug('scanner is set to read')
		state = STATES.ACCEPTING_READ
	elif mode == AppManager.DATA_MODES.WRITE:
		#print_debug('scanner is set to write')
		state = STATES.ACCEPTING_WRITE


func _on_scan_area_body_entered(body: Node3D) -> void:
	
	if state == STATES.OFF:
		return
	
	if state == STATES.ACCEPTING_READ:
		#print_debug('scanner is reading')
		AppManager.data_access.emit(body.data,AppManager.DATA_MODES.READ)
		state = STATES.NOT_ACCEPTING
	
	elif state == STATES.ACCEPTING_WRITE:
		#print_debug('scanner is writing')
		AppManager.data_access.emit(body.data,AppManager.DATA_MODES.WRITE)
		state = STATES.NOT_ACCEPTING
	
	
	
