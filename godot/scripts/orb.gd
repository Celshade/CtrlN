extends Node2D
## Flying bird obstacle (orb).

@onready var anim_sprite: AnimatedSprite2D = $AnimatedSprite

# Static frames loaded from BirdFlying.gif — shared via class
static var _frames_loaded := false
static var _sprite_frames: SpriteFrames = null


func _ready() -> void:
	if not _frames_loaded:
		_load_frames()
		_frames_loaded = true

	if _sprite_frames:
		anim_sprite.sprite_frames = _sprite_frames
		# Scale to ORB_SIZE (frames are 28x26 px original)
		anim_sprite.scale = Vector2(
			float(GameConfig.ORB_SIZE) / 28.0,
			float(GameConfig.ORB_SIZE) / 26.0
		)
		anim_sprite.play("fly")
	anim_sprite.centered = false
	set_meta("scored", false)


static func _load_frames() -> void:
	_sprite_frames = SpriteFrames.new()
	_sprite_frames.add_animation("fly")
	# GIF has 100ms per frame = 10 fps
	_sprite_frames.set_animation_speed("fly", 10)
	_sprite_frames.set_animation_loop("fly", true)

	for i in range(3):  # BirdFlying.gif has exactly 3 frames
		var tex := load("res://assets/bird_fly_%d.png" % i) as Texture2D
		if tex:
			_sprite_frames.add_frame("fly", tex)

	if _sprite_frames.get_frame_count("fly") == 0:
		_sprite_frames = null
