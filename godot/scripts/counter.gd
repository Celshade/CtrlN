extends Control
## Animated score counter using sprite digit assets.
## Uses TextureRect children so it works reliably inside a CanvasLayer.

const DIGIT_SIZE := 17    # 1× the 16px source content pixel width
const DIGIT_SPACING := 1
# All digit/transition PNGs are 120×120 with content at (59,50)-(75,67).
const _DIGIT_REGION := Rect2(59, 50, 16, 17)
const FRAMES_PER_ANIM := 3
const TICKS_PER_FRAME := 3

var _digit_tex: Array[Texture2D] = []
var _trans_tex: Dictionary = {}
var _new_digit_tex: Array[Texture2D] = []

var _score := -1
var _digit_rects: Array = []

var _anim_state := "idle"
var _anim_tick := 0
var _anim_frame := 0
var _trans_by_index: Dictionary = {}
var _animating_indices: Array = []


func _ready() -> void:
	_load_assets()
	set_score(0)


## Wraps a raw texture in an AtlasTexture cropped to the digit content region.
func _make_atlas(tex: Texture2D) -> AtlasTexture:
	var a := AtlasTexture.new()
	a.atlas = tex
	a.region = _DIGIT_REGION
	return a


func _load_assets() -> void:
	_digit_tex.clear()
	for i in range(10):
		var tex := load("res://assets/counter/%d.png" % i) as Texture2D
		if tex:
			_digit_tex.append(_make_atlas(tex))
		else:
			_digit_tex.append(null)

	_trans_tex.clear()
	for from_d in range(10):
		var to_d := (from_d + 1) % 10
		var key := "%d-%d" % [from_d, to_d]
		var arr: Array[Texture2D] = []
		for f in range(FRAMES_PER_ANIM):
			var tex := load("res://assets/counter/trans_%d_%d_%d.png" % [from_d, to_d, f]) as Texture2D
			if tex:
				arr.append(_make_atlas(tex))
		_trans_tex[key] = arr

	_new_digit_tex.clear()
	for f in range(FRAMES_PER_ANIM):
		var tex := load("res://assets/counter/new_digit_%d.png" % f) as Texture2D
		if tex:
			_new_digit_tex.append(_make_atlas(tex))


func set_score(new_score: int) -> void:
	if new_score == _score:
		return
	var old_score := _score if _score >= 0 else 0
	_score = new_score

	var old_str := str(old_score)
	var new_str := str(new_score)

	if new_str.length() > old_str.length():
		_rebuild_rects(new_score)
		_anim_state = "new_digit"
		_anim_tick = 0
		_anim_frame = 0
		_animating_indices = [0]
		_trans_by_index = {}
	else:
		_rebuild_rects(new_score)
		var padded_old := old_str.lpad(new_str.length(), "0")
		_trans_by_index = {}
		_animating_indices = []
		for i in range(new_str.length()):
			if padded_old[i] != new_str[i]:
				_trans_by_index[i] = "%s-%s" % [padded_old[i], new_str[i]]
				_animating_indices.append(i)
		if not _animating_indices.is_empty():
			_anim_state = "transition"
			_anim_tick = 0
			_anim_frame = 0


func _rebuild_rects(score_val: int) -> void:
	for r in _digit_rects:
		r.queue_free()
	_digit_rects.clear()

	var s_str := str(score_val)
	var start_x := 0.0

	for i in range(s_str.length()):
		var tr := TextureRect.new()
		tr.stretch_mode = TextureRect.STRETCH_SCALE
		tr.custom_minimum_size = Vector2(DIGIT_SIZE, DIGIT_SIZE)
		tr.size = Vector2(DIGIT_SIZE, DIGIT_SIZE)
		tr.position = Vector2(start_x + i * (DIGIT_SIZE + DIGIT_SPACING), 0.0)
		var d := int(s_str[i])
		if d < _digit_tex.size() and _digit_tex[d]:
			tr.texture = _digit_tex[d]
		add_child(tr)
		_digit_rects.append(tr)


func _physics_process(_delta: float) -> void:
	if _anim_state == "idle":
		return

	_anim_tick += 1
	var new_frame := _anim_tick / TICKS_PER_FRAME
	if new_frame == _anim_frame:
		return
	_anim_frame = new_frame

	var score_str := str(_score)

	match _anim_state:
		"new_digit":
			if _new_digit_tex.is_empty():
				_anim_state = "idle"
				return
			if _anim_frame >= _new_digit_tex.size():
				if not _digit_rects.is_empty():
					var d := int(score_str[0])
					if d < _digit_tex.size() and _digit_tex[d]:
						(_digit_rects[0] as TextureRect).texture = _digit_tex[d]
				_anim_state = "idle"
			else:
				if not _digit_rects.is_empty():
					(_digit_rects[0] as TextureRect).texture = _new_digit_tex[_anim_frame]

		"transition":
			var max_frames := 0
			for idx in _animating_indices:
				var key: String = _trans_by_index[idx]
				if _trans_tex.has(key):
					max_frames = maxi(max_frames, (_trans_tex[key] as Array).size())

			if _anim_frame >= max_frames:
				for idx in _animating_indices:
					if idx < _digit_rects.size():
						var d := int(score_str[idx])
						if d < _digit_tex.size() and _digit_tex[d]:
							(_digit_rects[idx] as TextureRect).texture = _digit_tex[d]
				_anim_state = "idle"
			else:
				for idx in _animating_indices:
					if idx >= _digit_rects.size():
						continue
					var key: String = _trans_by_index[idx]
					if _trans_tex.has(key):
						var frames: Array = _trans_tex[key]
						if not frames.is_empty():
							var fi := mini(_anim_frame, frames.size() - 1)
							(_digit_rects[idx] as TextureRect).texture = frames[fi]
