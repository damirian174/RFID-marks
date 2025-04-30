extends Node3D
class_name LevelController


enum MODE {TUTORIAL, EXAM, SANDBOX}


@export var active: bool = true
@export var arrow_connecter: PathConnector
@export var arrow_pointer: MeshInstance3D
@export var mode: MODE
