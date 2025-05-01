extends Node


var data_base: Array[RFIDData]



func get_data_by_id(data_id: String) -> RFIDData:
	
	for data: RFIDData in data_base:
		if data.data_id == data_id:
			return data
			
	return null


func add_data(data: RFIDData) -> Error:
	if not check_valid_data(data):
		return ERR_ALREADY_EXISTS
	
	data_base.append(data)
	return OK


func check_valid_data(data: RFIDData) -> bool:
	for db_data: RFIDData in data_base:
		if db_data.data_id == data.data_id:
			return false
	return true

	
func generate_unique_id() -> String:
	var strings: Array[String]
	for i: RFIDData in data_base:
		strings.append(i.data_id)
	
	if strings.is_empty():
		return 'SN0'
	
	var last = strings[-1]
	var existing := {}  # Using dictionary for fast lookups
	
	# Create a set of existing strings
	for s in strings:
		existing[s] = true
	
	var counter := 1
	while true:
		var candidate = "%s_%d" % [last, counter]
		if not existing.has(candidate):
			return candidate
		counter += 1
	return 'SN0'
