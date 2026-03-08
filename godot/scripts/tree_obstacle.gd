extends Node2D
## Tree ground obstacle.

@onready var sprite: Sprite2D = $Sprite


func _ready() -> void:
	var tex := load("res://assets/tree_obj.png") as Texture2D
	if tex:
		sprite.texture = tex
		sprite.centered = false
		var sx := float(GameConfig.TREE_SIZE) / tex.get_width()
		var sy := float(GameConfig.TREE_SIZE) / tex.get_height()
		sprite.scale = Vector2(sx, sy)
	set_meta("scored", false)
