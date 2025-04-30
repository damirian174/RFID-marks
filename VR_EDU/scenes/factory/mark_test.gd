extends LevelController



@export_group("Object markers")
#@export var stickers: Array[Sticker]
@export var sensor_parts:Array[XRToolsPickable]
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

## Указать на клавиатуру
@onready var keyboard_marker: Marker3D = $Computer/KeyboardMarker


## Указать на сканнер
@onready var connector_marker: Marker3D = $Scanner/ScanArea/ConnectorMarker

@onready var stickers: Array[Node] = $Stikers.get_children()
@onready var preferred_sticker: Sticker = $Stikers/Sticker

var attached_sticker: Sticker


var current_stage: StageManager.MARK = StageManager.MARK.NOTHING:
	set(value):
		current_stage = value
		if mode != MODE.TUTORIAL:
			return
		match current_stage:
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
				arrow_connecter.node_a = preferred_sticker
			StageManager.MARK.PRESS_MARK_BUTTON:
				arrow_connecter.node_a = null
				arrow_connecter.node_b = null
				arrow_pointer.target_node = mark_marker
				


func _ready() -> void:
	current_stage = StageManager.MARK.PRESS_BUTTON
	for i: Sticker in stickers:
		#print(i)
		i.grabbed.connect(switched_to_sticker)
	
	for i: Marker3D in sticker_place_markers:
		i.get_parent().body_entered.connect(func(body: Node3D) -> void: current_stage = StageManager.MARK.PRESS_MARK_BUTTON)


func _on_interactable_area_button_button_pressed(_button: Variant) -> void:
	if current_stage == StageManager.MARK.PRESS_BUTTON:
		current_stage = StageManager.MARK.GET_BOX


func _on_get_box_area_body_exited(_body: Node3D) -> void:
	if current_stage == StageManager.MARK.GET_BOX:
		current_stage = StageManager.MARK.ATTACH_STICKER


func switched_to_sticker(sticker: Sticker, _by):
	#print(sticker)
	if current_stage == StageManager.MARK.ATTACH_STICKER:
		arrow_connecter.node_a = sticker


func _process(_delta: float) -> void:
	if current_stage == StageManager.MARK.ATTACH_STICKER:
		var distances: Array[float] = []
		
		for i: Marker3D in sticker_place_markers:
			if not i:
				return
			distances.append(i.global_position.distance_squared_to(arrow_connecter.node_a.global_position))
		
		arrow_connecter.node_b = sticker_place_markers[distances.find(distances.min())]
