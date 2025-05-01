extends Node



var workers: Array[WorkerData] = []




func _ready() -> void:
	var divan: WorkerData = WorkerData.new()
	
	divan.name = 'Диван'
	divan.worker_id = '123123'
	divan.rights = divan.RIGHTS.WORKER
	workers.append(divan)
	
	var vasya: WorkerData = WorkerData.new()
	
	vasya.name = 'Вася'
	vasya.worker_id = '222444'
	vasya.rights = divan.RIGHTS.WORKER
	workers.append(vasya)


func worker_exists(id: String) -> bool:
	for i: WorkerData in workers:
		if i.worker_id == id:
			return true
	return false
