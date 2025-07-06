extends Node

#@export var resource_path : String = "res://resource/excel/export"
var _resource_dics : Dictionary = {}

@export var can_async : bool = true
var thread := Thread.new()

signal load_completed(resource_name: String, obj: Object)

func _exit_tree() -> void:
	thread.wait_to_finish()

func load_resources(resource_export, resource_script: String, resource_list: Dictionary) -> void:
	if can_async:
		thread.start(_load_resources.bind(resource_export, resource_script, resource_list))
		thread.wait_to_finish()
	else:
		_load_resources(resource_export, resource_script, resource_list)

func _load_resources(resource_export, resource_script: String, resource_list: Dictionary) -> Dictionary:
	var ret_dic : Dictionary
	for resource_name in resource_list:
		var resource_load_cfg = resource_list[resource_name]
		ret_dic[resource_name] = _load_resource_one(resource_export, resource_script, resource_name, resource_load_cfg)
	return ret_dic

func _get_resouce_obj(gd_class: GDScript, msg: String) -> Object:
	var constants = gd_class.get_script_constant_map()
	assert(constants.has(msg), msg + " 不存在")
	var clazz = constants[msg]
	assert(typeof(clazz) == TYPE_OBJECT && clazz.has_method("new"), msg + " 创建失败")
	return clazz.new()

func _load_resource_pbin(resource_pb_pbin: String, resource_gd_obj: Object):
	var ref_rv = null
	var ref_file = FileAccess.open(resource_pb_pbin, FileAccess.READ)
	assert(ref_file, resource_pb_pbin + " 不存在")
	ref_rv = ref_file.get_buffer(ref_file.get_length())
	var error_erl = resource_gd_obj.from_bytes(ref_rv)
	assert(error_erl == 0, resource_pb_pbin + " 加载失败")

func _load_resource_one(resource_export, resource_script, resource_name: String, resource_load_cfg: Dictionary) -> Object:
	# 先进行基础数据检查与获取
	assert(resource_load_cfg.has("pb_gd"), resource_name + "." + "pb_gd")
	assert(resource_load_cfg.has("pb_msg"), resource_name + "." + "pb_msg")
	assert(resource_load_cfg.has("pb_pbin"), resource_name + "." + "pb_pbin")
	var resource_pb_gd = resource_load_cfg.get("pb_gd") # proto生成的gd
	var resource_pb_msg = resource_load_cfg.get("pb_msg") # proto这个配置的message名
	var resource_pb_pbin = resource_load_cfg.get("pb_pbin") # proto这个配置的pbin文件
	# 检查对应pb和pbin是否存在
	var resource_gd = resource_script + "/" + resource_pb_gd
	assert(FileAccess.file_exists(resource_gd), resource_gd + " 不存在")
	var resource_pbin = resource_export + "/" + resource_pb_pbin
	assert(FileAccess.file_exists(resource_pbin), resource_pbin + " 不存在")
	# 开始加载gd
	var resource_gd_class = load(resource_gd)
	assert(resource_gd_class,  resource_gd + " 加载失败")
	var resource_gd_obj = _get_resouce_obj(resource_gd_class, resource_pb_msg)
	# 加载pbin
	_load_resource_pbin(resource_pbin, resource_gd_obj)
	# 报告加载结果
	add_resource(resource_name, resource_gd_obj)
	load_completed.emit(resource_name, resource_gd_obj)
	return resource_gd_obj

func add_resource(resource_name: String, obj: Object) -> void:
	_resource_dics[resource_name] = obj

func get_resource(resource_name: StringName) -> Object:
	if not _resource_dics.has(resource_name):
		printerr("配置不存在: ", resource_name)
		return null
	return _resource_dics[resource_name]
