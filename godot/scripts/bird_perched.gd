extends Node2D
## Bird perched on a tree — may fly upward.

@onready var sprite: Sprite2D = $Sprite
@onready var fly_anim: AnimatedSprite2D = $FlyAnim

static var _fly_frames: SpriteFrames = null

var is_flying := false
var is_red := false
var tree_ref: Node2D = null
var transition_frame := 0
var y_distance_per_frame := 20.0


func setup(tree: Node2D) -> void:
	tree_ref = tree
	is_flying = randf() < 0.33
	is_red = (not is_flying) and randf() < 0.5
	set_meta("scored", false)
	set_meta("is_red", is_red)

	if is_flying:
		position.x = tree.position.x + (GameConfig.TREE_SIZE - GameConfig.ORB_SIZE) / 2.0
		position.y = tree.position.y - GameConfig.PERCHED_BIRD_SIZE / 1.9
	else:
		_update_perch_position()

	# Load appropriate sprite
	call_deferred("_load_sprite")


func _load_sprite() -> void:
	if is_flying:
		sprite.visible = false
		if _fly_frames == null:
			_fly_frames = _build_fly_frames()
		if _fly_frames:
			fly_anim.sprite_frames = _fly_frames
			fly_anim.centered = false
			var sx := float(GameConfig.ORB_SIZE) / 28.0
			var sy := float(GameConfig.ORB_SIZE) / 26.0
			fly_anim.scale = Vector2(sx, sy)
			fly_anim.visible = true
			fly_anim.play("fly")
	else:
		fly_anim.visible = false
		var filename := "res://assets/bird_red/BirdPerchedRed.png" if is_red else "res://assets/bird_yellow/BirdPerched.png"
		var tex := load(filename) as Texture2D
		if tex:
			sprite.texture = tex
			sprite.centered = false
			var sx := float(GameConfig.PERCHED_BIRD_SIZE) / tex.get_width()
			var sy := float(GameConfig.PERCHED_BIRD_SIZE) / tex.get_height()
			sprite.scale = Vector2(sx, sy)
			sprite.visible = true


static func _build_fly_frames() -> SpriteFrames:
	var frames := SpriteFrames.new()
	frames.add_animation("fly")
	frames.set_animation_speed("fly", 10)
	frames.set_animation_loop("fly", true)
	for i in range(3):  # BirdFlying.gif has exactly 3 frames
		var tex := load("res://assets/bird_yellow/bird_fly_%d.png" % i) as Texture2D
		if tex:
			frames.add_frame("fly", tex)
	return frames if frames.get_frame_count("fly") > 0 else null


func _update_perch_position() -> void:
	if tree_ref:
		position.x = tree_ref.position.x + (GameConfig.TREE_SIZE - GameConfig.PERCHED_BIRD_SIZE) / 2.0 - 46
		position.y = tree_ref.position.y - GameConfig.PERCHED_BIRD_SIZE / 1.9


## Returns the world-space Rect2 of the actual visible sprite pixels.
## Used by game.gd for pixel-accurate (mask-equivalent) collision instead of AABB.
func get_hitbox_rect() -> Rect2:
	if is_flying:
		# fly_anim uses bird_fly frames at ORB_SIZE (38×38), opaque region ~(4,3) size (29,31).
		return Rect2(position + GameConfig.ORB_HITBOX_OFFSET, GameConfig.ORB_HITBOX_SIZE)
	else:
		# Sprite uses BirdPerched.png scaled to 300×300; actual bird occupies a tiny region.
		return Rect2(position + GameConfig.PERCHED_BIRD_HITBOX_OFFSET, GameConfig.PERCHED_BIRD_HITBOX_SIZE)


func _physics_process(_delta: float) -> void:
	if is_flying:
		if transition_frame < 7:
			position.y -= y_distance_per_frame
			transition_frame += 1
	else:
		if tree_ref and is_instance_valid(tree_ref):
			_update_perch_position()
