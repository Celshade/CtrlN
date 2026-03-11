extends Node2D
## Player entity — physics, shields, drawing.
## Assets used here:
##   - Character sprite (Sprite2D):      passed in via setup() asset_path
##   - Jump animation (AnimatedSprite2D): keypress_{char_id}/keypress_thruster_fx{i}.png
##                                        plays during in-game keypresses; replaces sprite briefly
##   - Shield sprite/anim:               shield_3.2.png, shield_3.4.png, shield gain anim frames

@onready var sprite: Sprite2D = $Sprite
@onready var shield_sprite: Sprite2D = $ShieldSprite
@onready var shield_anim: AnimatedSprite2D = $ShieldAnim
@onready var jump_anim: AnimatedSprite2D = $JumpAnim

var velocity := 0.0
var character_id := "black"

# Shield state
var shield_charges := 0
var next_shield_threshold := 5
var invulnerability_frames := 0

# Shield textures
var shield_tex_t1: Texture2D
var shield_tex_t2: Texture2D

# In-game jump animation frames cache: character_id -> SpriteFrames
# Loaded from: assets/keypress_{char_id}/keypress_thruster_fx{i}.png
static var _jump_frames_cache: Dictionary = {}


func setup(char_id: String, asset_path: String) -> void:
	character_id = char_id
	position = Vector2(GameConfig.PLAYER_START_X, GameConfig.PLAYER_START_Y)
	velocity = 0.0
	shield_charges = 0
	next_shield_threshold = 5
	invulnerability_frames = 0

	# Load character sprite
	var tex := load(asset_path) as Texture2D
	if tex:
		sprite.texture = tex
		sprite.centered = false
		var sx := float(GameConfig.PLAYER_SIZE) / tex.get_width()
		var sy := float(GameConfig.PLAYER_SIZE) / tex.get_height()
		sprite.scale = Vector2(sx, sy)

	# Load shield textures
	shield_tex_t1 = load("res://assets/shields/tier1/shield_3.2.png") as Texture2D
	shield_tex_t2 = load("res://assets/shields/tier2/shield_3.4.png") as Texture2D
	shield_sprite.centered = false
	if shield_tex_t1:
		var ssx := float(GameConfig.PLAYER_SIZE) / shield_tex_t1.get_width()
		var ssy := float(GameConfig.PLAYER_SIZE) / shield_tex_t1.get_height()
		shield_sprite.scale = Vector2(ssx, ssy)
	# Shield charge animation
	shield_anim.centered = false
	shield_anim.scale = Vector2(
		float(GameConfig.PLAYER_SIZE) / 150.0,
		float(GameConfig.PLAYER_SIZE) / 150.0
	)
	shield_anim.animation_finished.connect(_on_shield_anim_finished)
	# In-game jump animation: keypress thruster FX from keypress_{char_id}/
	if not _jump_frames_cache.has(char_id):
		_jump_frames_cache[char_id] = _build_jump_frames(char_id)
	var jframes: SpriteFrames = _jump_frames_cache[char_id]
	if jframes:
		jump_anim.sprite_frames = jframes
		jump_anim.centered = false
		jump_anim.scale = sprite.scale
		if jump_anim.animation_finished.is_connected(_on_jump_anim_finished):
			jump_anim.animation_finished.disconnect(_on_jump_anim_finished)
		jump_anim.animation_finished.connect(_on_jump_anim_finished)



static func _build_jump_frames(char_id: String) -> SpriteFrames:
	# Loads in-game keypress thruster frames from assets/keypress_{char_id}/
	var frames := SpriteFrames.new()
	frames.add_animation("jump")
	frames.set_animation_speed("jump", 20)
	frames.set_animation_loop("jump", false)
	var i := 1
	while true:
		var path := "res://assets/characters/%s/keypress/keypress_%d.png" % [char_id, i]
		if ResourceLoader.exists(path):
			frames.add_frame("jump", load(path))
			i += 1
		else:
			break
	return frames if i > 1 else null

func _on_jump_anim_finished() -> void:
	jump_anim.visible = false
	sprite.visible = true


func do_jump() -> void:
	velocity = GameConfig.KEY_POWER
	if jump_anim.sprite_frames:
		sprite.visible = false
		jump_anim.visible = true
		jump_anim.stop()
		jump_anim.play("jump")


func do_update() -> void:
	velocity += GameConfig.GRAVITY
	position.y += velocity

	# Update animation frame visibility in sync with invulnerability flash
	if invulnerability_frames > 0:
		invulnerability_frames -= 1
		var show := invulnerability_frames % 4 < 2
		sprite.modulate.a = 0.5 if show else 1.0
		if jump_anim.visible:
			jump_anim.modulate.a = sprite.modulate.a
	else:
		sprite.modulate.a = 1.0
		jump_anim.modulate.a = 1.0

	_update_shield_visual()


func has_shield() -> bool:
	return shield_charges > 0


func is_invulnerable() -> bool:
	return invulnerability_frames > 0


func update_shields(current_score: int) -> bool:
	if current_score >= next_shield_threshold and shield_charges < 2:
		shield_charges += 1
		next_shield_threshold += 5
		_play_shield_gain_anim(shield_charges)
		return true
	return false


func _play_shield_gain_anim(new_level: int) -> void:
	var frames := _build_shield_anim_frames(new_level)
	if frames == null:
		_update_shield_visual()
		return
	var anim_name := "shield_t%d" % new_level
	shield_anim.sprite_frames = frames
	shield_anim.visible = true
	shield_sprite.visible = false  # hidden while gain-anim plays
	shield_anim.stop()
	shield_anim.play(anim_name)


static var _shield_frames_cache: Dictionary = {}

static func _build_shield_anim_frames(level: int) -> SpriteFrames:
	var cache_key := "t%d" % level
	if _shield_frames_cache.has(cache_key):
		return _shield_frames_cache[cache_key]
	var color_dir := "tier%d" % level
	var frames := SpriteFrames.new()
	var anim_name := "shield_t%d" % level
	frames.add_animation(anim_name)
	frames.set_animation_speed(anim_name, 30.0)  # 30 fps = one frame per physics tick
	frames.set_animation_loop(anim_name, false)
	var i := 1
	while true:
		var path := "res://assets/shields/%s/charge/charge%d.png" % [color_dir, i]
		if ResourceLoader.exists(path):
			frames.add_frame(anim_name, load(path))
			i += 1
		else:
			break
	if frames.get_frame_count(anim_name) == 0:
		return null
	_shield_frames_cache[cache_key] = frames
	return frames


func _on_shield_anim_finished() -> void:
	shield_anim.visible = false
	_update_shield_visual()


func destroy_shield() -> void:
	if shield_charges > 0:
		shield_charges -= 1
		invulnerability_frames = GameConfig.SHIELD_INVULNERABILITY_FRAMES
		_update_shield_visual()


func _update_shield_visual() -> void:
	if shield_anim.visible:
		return  # gain-animation is in progress; it will call us when done
	if shield_charges == 2 and shield_tex_t2:
		shield_sprite.texture = shield_tex_t2
		shield_sprite.visible = true
	elif shield_charges == 1 and shield_tex_t1:
		shield_sprite.texture = shield_tex_t1
		shield_sprite.visible = true
	else:
		shield_sprite.visible = false


func is_dead() -> bool:
	return position.y + GameConfig.PLAYER_SIZE >= GameConfig.GROUND_Y or position.y < -14
