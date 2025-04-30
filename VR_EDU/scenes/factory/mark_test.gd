extends LevelController



@export_group("Object markers")
@export var stickers: Array[Sticker]
@export var sensor_parts:Array[XRToolsPickable]
@export var container: XRToolsPickable
@export var scanner: MeshInstance3D
@export var computer: Node3D


## Указать на кнопку
@onready var button_hint_marker: Marker3D = $Button/ButtonHintMarker

## Указать на коробку(Положить на стол)
@onready var hand: XRToolsHand = $Player/RaightHand/RightHand


## Указать на коробку(Стикеры)
@onready var sticker_place_marker1: Marker3D = $Container/StickerAreas/StickerArea/StickerPlaceMarker
@onready var sticker_place_marker2: Marker3D = $Container/StickerAreas/StickerArea2/StickerPlaceMarker
@onready var sticker_place_marker3: Marker3D = $Container/StickerAreas/StickerArea3/StickerPlaceMarker
@onready var sticker_place_marker4: Marker3D = $Container/StickerAreas/StickerArea4/StickerPlaceMarker

var sticker_in_hand: Sticker


## Указать на маркировку
@onready var mark_marker: Marker3D = $Computer/MarkMarker

## Указать на клавиатуру
@onready var keyboard_marker: Marker3D = $Computer/KeyboardMarker


## Указать на сканнер
@onready var connector_marker: Marker3D = $Scanner/ScanArea/ConnectorMarker


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



func _ready() -> void:
	current_stage = StageManager.MARK.PRESS_BUTTON


func _on_interactable_area_button_button_pressed(button: Variant) -> void:
	if StageManager.MARK.PRESS_BUTTON:
		current_stage = StageManager.MARK.GET_BOX


func _on_get_box_area_body_entered(body: Node3D) -> void:
	pass # Replace with function body.
