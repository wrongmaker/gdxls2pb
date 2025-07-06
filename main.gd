extends Node2D

var resource_export = "res://resource/excel/export"
var resource_script = "res://resource/excel/script"

var resource_file = {
	"Skill": {
		"pb_gd": "skill.gd",
		"pb_msg": "SkillRows",
		"pb_pbin": "Skill.pbin"
	},
	"Buff": {
		"pb_gd": "skill.gd",
		"pb_msg": "BuffRows",
		"pb_pbin": "Buff.pbin"
	},
	"Effect": {
		"pb_gd": "skill.gd",
		"pb_msg": "EffectRows",
		"pb_pbin": "Effect.pbin"
	}
}

func _on_load_completed(resource_name: String, obj: Object) -> void:
	print(obj)

func _ready() -> void:
	print("加载配置...")
	ResourceMgr.load_completed.connect(_on_load_completed)
	ResourceMgr.load_resources(resource_export, resource_script, resource_file)
