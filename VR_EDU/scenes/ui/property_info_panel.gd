extends PanelContainer

@onready var header_label: Label = $VBoxContainer/HeaderLabel
@onready var value_label: Label = $VBoxContainer/ValueLabel






var header: String:
	set(value):
		header_label.text = value
		
var value: String:
	set(value):
		value_label.text = value
