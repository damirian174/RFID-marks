extends LevelController



@export_group("Object markers")
#@export var stickers: Array[Sticker]
@export var sensor_parts: Array[XRToolsPickable]
@export var container: XRToolsPickable
@export var scanner: MeshInstance3D
@export var computer: Node3D


## Указать на кнопку
@onready var button_hint_marker: Marker3D = $Button/ButtonHintMarker

## Указать на коробку(Положить на стол)
@onready var hand: XRToolsHand = $Player/RaightHand/RightHand


## Указать на коробку(Стикеры)
@onready var sticker_place_markers: Array[Marker3D] = [
	$Container/StickerAreas/StickerArea/StickerPlaceMarker,
	$Container/StickerAreas/StickerArea2/StickerPlaceMarker,
	$Container/StickerAreas/StickerArea3/StickerPlaceMarker,
	$Container/StickerAreas/StickerArea4/StickerPlaceMarker,
]


var sticker_in_hand: Sticker


## Указать на маркировку
@onready var mark_marker: Marker3D = $Computer/MarkMarker


## Указать на авторизацию
@onready var auth_marker: Marker3D = $Computer/AuthMarker


## Указать на клавиатуру
@onready var keyboard_marker: Marker3D = $Computer/KeyboardMarker


## Указать на сканнер
@onready var connector_marker: Marker3D = $Scanner/ScanArea/ConnectorMarker


## Бэйдж который нужно тепнуть
const BAGE = preload("res://scenes/factory/bage.tscn")
@onready var bage_spawn_marker: Marker3D = $bageSpawnMarker
var bage_teleported: bool = false


@onready var stickers: Array[Node] = $Stikers.get_children()
@onready var preferred_sticker: Sticker = $Stikers/Sticker

var attached_sticker: Sticker
var keyboard_hinted: int = 0

@onready var app: Control = $Computer/Viewport2Din3D/Viewport/App


var current_stage: StageManager.MARK = StageManager.MARK.NOTHING:
	set(value):
		current_stage = value
		if mode != MODE.TUTORIAL:
			arrow_connecter.node_a = null
			arrow_connecter.node_b = null
			arrow_pointer.target_node = null
		match current_stage:
			StageManager.MARK.NOTHING:
				arrow_connecter.node_a = null
				arrow_connecter.node_b = null
				arrow_pointer.target_node = null
			StageManager.MARK.PRESS_BUTTON:
				arrow_pointer.target_node = button_hint_marker
				arrow_connecter.node_a = null
				arrow_connecter.node_b = null
			StageManager.MARK.GET_BOX:
				#print('getbox')
				arrow_pointer.target_node = null
				arrow_connecter.node_a = hand
				arrow_connecter.node_b = container
				#print(hand)
			StageManager.MARK.ATTACH_STICKER:
				arrow_connecter.node_a = preferred_sticker.get_child(0)
			StageManager.MARK.PRESS_MARK_BUTTON:
				if not bage_teleported:
					var bage: XRToolsPickable = BAGE.instantiate()
					bage.global_transform = bage_spawn_marker.global_transform
					add_child(bage)
					bage.get_node("Dissolver").dissolve()
					bage_teleported = true
				if (not app.auth) and (keyboard_hinted == 1):
					arrow_connecter.node_a = null
					arrow_connecter.node_b = null
					arrow_pointer.target_node = keyboard_marker
					keyboard_hinted += 1
				
				elif app.auth:
					arrow_connecter.node_a = null
					arrow_connecter.node_b = null
					arrow_pointer.target_node = mark_marker
				else:
					arrow_connecter.node_a = null
					arrow_connecter.node_b = null
					arrow_pointer.target_node = auth_marker
			StageManager.MARK.FILL_PROPERTIES:
				arrow_connecter.node_a = null
				arrow_connecter.node_b = null
				arrow_pointer.target_node = null
			StageManager.MARK.SCAN:
				arrow_pointer.target_node = null
				arrow_connecter.node_a = attached_sticker.get_child(0)
				arrow_connecter.node_b = connector_marker
				

func _ready() -> void:
	#current_stage = StageManager.MARK.PRESS_BUTTON
	if mode == MODE.TUTORIAL:
		app.tutorial = true
	
	for i: Sticker in stickers:
		#print(i)
		i.grabbed.connect(switched_to_sticker)
	
	for i: Marker3D in sticker_place_markers:
		i.get_parent().body_entered.connect(func(_body: Node3D) -> void: current_stage = StageManager.MARK.PRESS_MARK_BUTTON; attached_sticker = _body)
		
	AppManager.authed.connect(_on_authed)
	AppManager.hint_keyboard.connect(_on_keyboard_hint)
	AppManager.submitted_mark_parameters.connect(func() -> void: if attached_sticker: current_stage = StageManager.MARK.SCAN)
	AppManager.started_filling_in.connect(func() -> void: if attached_sticker: current_stage = StageManager.MARK.FILL_PROPERTIES)
	AppManager.data_access.connect(func(body:Sticker, readwrite_mode: AppManager.DATA_MODES):
									if readwrite_mode == AppManager.DATA_MODES.WRITE and attached_sticker:
										mode = MODE.SANDBOX
										current_stage = StageManager.MARK.NOTHING
									)
	
func _on_authed():
	if current_stage == StageManager.MARK.PRESS_MARK_BUTTON:
		current_stage = StageManager.MARK.PRESS_MARK_BUTTON

func _on_interactable_area_button_button_pressed(_button: Variant) -> void:
	if current_stage == StageManager.MARK.PRESS_BUTTON:
		current_stage = StageManager.MARK.GET_BOX


func _on_get_box_area_body_exited(_body: Node3D) -> void:
	if current_stage == StageManager.MARK.GET_BOX:
		current_stage = StageManager.MARK.ATTACH_STICKER


func switched_to_sticker(sticker: Sticker, _by):
	#print(sticker)
	if current_stage == StageManager.MARK.ATTACH_STICKER:
		arrow_connecter.node_a = sticker.get_child(0)


func _process(_delta: float) -> void:
	if current_stage == StageManager.MARK.ATTACH_STICKER:
		var distances: Array[float] = []
		
		for i: Marker3D in sticker_place_markers:
			if not i:
				return
			distances.append(i.global_position.distance_squared_to(arrow_connecter.node_a.global_position))
		
		arrow_connecter.node_b = sticker_place_markers[distances.find(distances.min())]


func _on_keyboard_hint():
	if current_stage == StageManager.MARK.PRESS_MARK_BUTTON:
		keyboard_hinted += 1
		current_stage = StageManager.MARK.PRESS_MARK_BUTTON
		


func _on_start_test_body_entered(body: Node3D) -> void:
	#print(1)
	current_stage = StageManager.MARK.PRESS_BUTTON
	$StartTest.queue_free()
	
