extends Resource
class_name WorkerData

enum RIGHTS {GUEST, WORKER, ADMIN}

@export var worker_id: String
@export var name: String
@export var rights: RIGHTS
