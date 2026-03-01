from typing import NamedTuple

import pygame
from PIL import Image

from config import WINDOW_WIDTH, WINDOW_HEIGHT, GROUND_Y, BLACK, WHITE, YELLOW


# ------------------------------------------------------------------ #
# Layout constants (tuned for 890×400 px window)                     #
# ------------------------------------------------------------------ #
_FRAME_MS    = 60    # ms per animation frame (~16 fps)
_TITLE_H     = 38    # vertical space reserved for the title bar

# Icon grid — left panel -------------------------------------------
_GRID_COLS   = 5
_GRID_ROWS   = 3     # 5 × 3 = 15 slots
_ICON_SZ     = 50    # rendered icon image size in pixels
_ICON_CELL   = 58    # cell footprint (icon + padding)
_ICON_GAP    = 3     # gap between cells
_ICON_STEP   = _ICON_CELL + _ICON_GAP          # 61 px
_GRID_W      = _GRID_COLS * _ICON_STEP - _ICON_GAP   # 302 px
_GRID_H      = _GRID_ROWS * _ICON_STEP - _ICON_GAP   # 180 px
_GRID_LEFT   = 18
_GRID_PANEL_W = _GRID_LEFT + _GRID_W + _GRID_LEFT    # 338 px

_ICON_BG     = (230, 230, 230)
_ICON_SEL    = YELLOW
_ICON_UNSEL  = (160, 160, 160)
_ICON_BDR    = 3

# Featured card — right panel --------------------------------------
_CARD_W      = 200
_CARD_H      = 270
_PREV_SZ     = 150   # featured preview image size
_CARD_BG     = (240, 240, 240)
_CARD_BDR    = YELLOW
_CARD_BDR_W  = 4

_BTN_W       = 140
_BTN_H       = 40
_BTN_COLOR   = (50, 200, 80)
_BTN_HOVER   = (80, 230, 110)

# Typography -------------------------------------------------------
_FONT_TITLE  = 30
_FONT_NAME   = 24
_FONT_BTN    = 22
_FONT_HINT   = 18


# ====================== #
# ### Character data ### #
# ====================== #
class Character(NamedTuple):
    """Immutable descriptor for a selectable character."""
    id: str
    name: str
    asset_path: str          # sprite used by the Player class in-game
    preview_path: str = ""   # animated webP shown on the select screen
    description: str = ""
    locked: bool = False     # if True: greyed out and unselectable


# NOTE: Add new entries here; the grid expands automatically up to 15 slots.
# Characters with locked=True show a padlock overlay and cannot be selected.
CHARACTER_ROSTER: list[Character] = [
    Character(
        id="black",
        name="Black",
        asset_path="assets/player.png",
        preview_path="assets/key_bounce.webP",
    ),
    Character(
        id="grey",
        name="Grey",
        asset_path="assets/player.png",
        preview_path="assets/key_bounce.webP",
    ),
    Character(
        id="dark_green",
        name="Dark Green",
        asset_path="assets/player.png",
        preview_path="assets/key_bounce.webP",
    ),
    Character(
        id="dark_blue",
        name="Dark Blue",
        asset_path="assets/player.png",
        preview_path="assets/key_bounce.webP",
    ),
    Character(
        id="red",
        name="Red",
        asset_path="assets/player.png",
        preview_path="assets/key_bounce.webP",
    ),
    # --- locked below this line ---
    Character(
        id="yellow",
        name="Yellow",
        asset_path="assets/player.png",
        preview_path="assets/key_bounce.webP",
        locked=True,
    ),
    Character(
        id="purple",
        name="Purple",
        asset_path="assets/player.png",
        preview_path="assets/key_bounce.webP",
        locked=True,
    ),
    Character(
        id="green",
        name="Green",
        asset_path="assets/player.png",
        preview_path="assets/key_bounce.webP",
        locked=True,
    ),
    Character(
        id="orange",
        name="Orange",
        asset_path="assets/player.png",
        preview_path="assets/key_bounce.webP",
        locked=True,
    ),
    Character(
        id="white",
        name="White",
        asset_path="assets/player.png",
        preview_path="assets/key_bounce.webP",
        locked=True,
    ),
    Character(
        id="aqua",
        name="Aqua",
        asset_path="assets/player.png",
        preview_path="assets/key_bounce.webP",
        locked=True,
    ),
    Character(
        id="sunset",
        name="Sunset",
        asset_path="assets/player.png",
        preview_path="assets/key_bounce.webP",
        locked=True,
    ),
    Character(
        id="silver",
        name="Silver",
        asset_path="assets/player.png",
        preview_path="assets/key_bounce.webP",
        locked=True,
    ),
    Character(
        id="gold",
        name="Gold",
        asset_path="assets/player.png",
        preview_path="assets/key_bounce.webP",
        locked=True,
    ),
]


# ============================ #
# ### CharacterSelect UI   ### #
# ============================ #
class CharacterSelect:
    """Renders the character selection screen and tracks current selection.

    Layout:
      Left panel  — 5×3 icon grid (static image when idle, animated when
                    selected).
      Right panel — single full-size featured card for the highlighted
                    character (always animated).
    """

    # Class-level cache: (path, size) -> frames / surface
    _frame_cache: dict[tuple[str, int], list[pygame.Surface]] = {}
    _static_cache: dict[tuple[str, int], pygame.Surface] = {}

    def __init__(self) -> None:
        self._font_title = pygame.font.Font(None, _FONT_TITLE)
        self._font_name  = pygame.font.Font(None, _FONT_NAME)
        self._font_btn   = pygame.font.Font(None, _FONT_BTN)
        self._font_hint  = pygame.font.Font(None, _FONT_HINT)

        self.selected_index: int = 0
        self._play_button_rect: pygame.Rect | None = None
        self._icon_rects: list[pygame.Rect] = []

        preview_path = CHARACTER_ROSTER[0].preview_path
        asset_path   = CHARACTER_ROSTER[0].asset_path

        # Animated frames at icon size (shown only for the selected icon).
        self._icon_frames: list[pygame.Surface] = self._load_frames(
            preview_path, _ICON_SZ
        )
        # Static image at icon size (shown for every unselected icon).
        self._icon_static: pygame.Surface | None = self._load_static(
            asset_path, _ICON_SZ
        )
        # Animated frames at featured size (right-panel card).
        self._feat_frames: list[pygame.Surface] = self._load_frames(
            preview_path, _PREV_SZ
        )

        self._anim_frame: int = 0
        self._last_frame_time: int = 0

        # Lock overlay: semi-transparent dark surface sized to one icon cell.
        self._lock_overlay = pygame.Surface(
            (_ICON_CELL, _ICON_CELL), pygame.SRCALPHA
        )
        self._lock_overlay.fill((0, 0, 0, 160))

        # Lock emoji rendered once; try emoji-capable system fonts first.
        _lock_font = pygame.font.SysFont(
            "notoemoji,noto emoji,noto-color-emoji,symbola,segoeuisymbol",
            22,
        )
        self._lock_surf = _lock_font.render("\U0001f512", True, WHITE)

        # Pre-compute icon rects (layout is fixed).
        self._build_icon_rects()

    # ------------------------------------------------------------------ #
    # Asset loading                                                      #
    # ------------------------------------------------------------------ #

    @classmethod
    def _load_frames(
        cls, path: str, size: int
    ) -> list[pygame.Surface]:
        """Load all frames from an animated webP via PIL; cached by
        (path, size) so decoding only ever happens once."""
        key = (path, size)
        if key in cls._frame_cache:
            return cls._frame_cache[key]
        frames: list[pygame.Surface] = []
        try:
            pil_img = Image.open(path)
            try:
                while True:
                    frame = pil_img.convert("RGBA")
                    frame = frame.resize(
                        (size, size), Image.Resampling.LANCZOS
                    )
                    frames.append(
                        pygame.image.fromstring(
                            frame.tobytes(), frame.size, frame.mode
                        )
                    )
                    pil_img.seek(pil_img.tell() + 1)
            except EOFError:
                pass
        except Exception as exc:
            print(f"Warning: Could not load '{path}': {exc}")
        cls._frame_cache[key] = frames
        return frames

    @classmethod
    def _load_static(
        cls, path: str, size: int
    ) -> pygame.Surface | None:
        """Load and scale a single static image via PIL; cached by
        (path, size)."""
        key = (path, size)
        if key in cls._static_cache:
            return cls._static_cache[key]
        surf: pygame.Surface | None = None
        try:
            pil_img = Image.open(path).convert("RGBA")
            pil_img = pil_img.resize((size, size), Image.Resampling.LANCZOS)
            surf = pygame.image.fromstring(
                pil_img.tobytes(), pil_img.size, pil_img.mode
            )
        except Exception as exc:
            print(f"Warning: Could not load static '{path}': {exc}")
        cls._static_cache[key] = surf
        return surf

    # ------------------------------------------------------------------ #
    # Layout helpers                                                     #
    # ------------------------------------------------------------------ #

    def _build_icon_rects(self) -> None:
        """Pre-compute the pygame.Rect for every icon grid slot."""
        grid_top = (
            _TITLE_H
            + (WINDOW_HEIGHT - _TITLE_H - _GRID_H) // 2
        )
        self._icon_rects = []
        for slot in range(_GRID_COLS * _GRID_ROWS):
            col = slot % _GRID_COLS
            row = slot // _GRID_COLS
            x = _GRID_LEFT + col * _ICON_STEP
            y = grid_top + row * _ICON_STEP
            self._icon_rects.append(
                pygame.Rect(x, y, _ICON_CELL, _ICON_CELL)
            )

    def _featured_rect(self) -> pygame.Rect:
        """Rect for the large featured card, centred in the right panel."""
        right_w = WINDOW_WIDTH - _GRID_PANEL_W
        card_x = _GRID_PANEL_W + (right_w - _CARD_W) // 2
        card_y = _TITLE_H + (WINDOW_HEIGHT - _TITLE_H - _CARD_H) // 2
        return pygame.Rect(card_x, card_y, _CARD_W, _CARD_H)

    # ------------------------------------------------------------------ #
    # Navigation                                                         #
    # ------------------------------------------------------------------ #

    def navigate(self, direction: int) -> None:
        """Move selection by *direction* slots (±1), skipping locked entries."""
        n = len(CHARACTER_ROSTER)
        idx = (self.selected_index + direction) % n
        for _ in range(n):
            if not CHARACTER_ROSTER[idx].locked:
                self.selected_index = idx
                return
            idx = (idx + direction) % n

    def navigate_row(self, direction: int) -> None:
        """Move up (-1) or down (+1) by one grid row, skipping locked entries."""
        n = len(CHARACTER_ROSTER)
        idx = (self.selected_index + direction * _GRID_COLS) % n
        for _ in range(n):
            if not CHARACTER_ROSTER[idx].locked:
                self.selected_index = idx
                return
            idx = (idx + direction * _GRID_COLS) % n

    @property
    def selected(self) -> Character:
        """Return the currently highlighted Character."""
        return CHARACTER_ROSTER[self.selected_index]

    # ------------------------------------------------------------------ #
    # Hit-testing                                                        #
    # ------------------------------------------------------------------ #

    def is_play_clicked(self, pos: tuple[int, int]) -> bool:
        """Return True if *pos* is inside the Play button."""
        if self._play_button_rect is None:
            return False
        return self._play_button_rect.collidepoint(pos)

    def icon_slot_at(self, pos: tuple[int, int]) -> int | None:
        """Return the roster index for the unlocked icon at *pos*, or None."""
        for slot, rect in enumerate(self._icon_rects):
            if slot >= len(CHARACTER_ROSTER):
                break
            if rect.collidepoint(pos):
                return None if CHARACTER_ROSTER[slot].locked else slot
        return None

    # ------------------------------------------------------------------ #
    # Drawing                                                            #
    # ------------------------------------------------------------------ #

    def draw(self, screen: pygame.Surface) -> None:
        """Render the full character selection UI onto *screen*."""
        mouse_pos = pygame.mouse.get_pos()

        # Advance shared animation clock.
        if self._icon_frames:
            now = pygame.time.get_ticks()
            if now - self._last_frame_time >= _FRAME_MS:
                self._last_frame_time = now
                total = len(self._icon_frames)
                self._anim_frame = (self._anim_frame + 1) % total

        # ---- Title ----
        title = self._font_title.render(
            "Select Your Character", True, BLACK
        )
        screen.blit(
            title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 6)
        )

        # ---- Icon grid ----
        self._draw_icon_grid(screen, mouse_pos)

        # ---- Featured card ----
        self._draw_featured_card(screen, mouse_pos)

    def _draw_icon_grid(
        self,
        screen: pygame.Surface,
        mouse_pos: tuple[int, int],
    ) -> None:
        """Draw the 5×3 icon grid in the left panel."""
        for slot, rect in enumerate(self._icon_rects):
            if slot >= len(CHARACTER_ROSTER):
                break
            is_sel = slot == self.selected_index
            is_hov = rect.collidepoint(mouse_pos)

            pygame.draw.rect(screen, _ICON_BG, rect, border_radius=6)

            bdr_col = _ICON_SEL if is_sel else (
                (200, 200, 100) if is_hov else _ICON_UNSEL
            )
            bdr_w = _ICON_BDR + 1 if is_sel else _ICON_BDR
            pygame.draw.rect(
                screen, bdr_col, rect, width=bdr_w, border_radius=6
            )

            img_x = rect.x + (_ICON_CELL - _ICON_SZ) // 2
            img_y = rect.y + (_ICON_CELL - _ICON_SZ) // 2
            is_locked = CHARACTER_ROSTER[slot].locked
            if is_sel and self._icon_frames and not is_locked:
                screen.blit(
                    self._icon_frames[self._anim_frame], (img_x, img_y)
                )
            elif self._icon_static:
                screen.blit(self._icon_static, (img_x, img_y))

            # Lock overlay + emoji for locked slots
            if is_locked:
                screen.blit(self._lock_overlay, rect.topleft)
                lx = (
                    rect.x
                    + (_ICON_CELL - self._lock_surf.get_width()) // 2
                )
                ly = (
                    rect.y
                    + (_ICON_CELL - self._lock_surf.get_height()) // 2
                )
                screen.blit(self._lock_surf, (lx, ly))

        # Navigation hint pinned to the ground bar
        # hint = self._font_hint.render(
        #     "\u25c4 \u25ba \u25b2 \u25bc  navigate   click to select",
        #     True,
        #     (60, 60, 60),
        # )
        # hint_y = GROUND_Y + (WINDOW_HEIGHT - GROUND_Y - hint.get_height()) // 2
        # screen.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, hint_y))

    def _draw_featured_card(
        self,
        screen: pygame.Surface,
        mouse_pos: tuple[int, int],
    ) -> None:
        """Draw the large featured card in the right panel."""
        card_rect = self._featured_rect()

        pygame.draw.rect(screen, _CARD_BG, card_rect, border_radius=10)
        pygame.draw.rect(
            screen, _CARD_BDR, card_rect,
            width=_CARD_BDR_W, border_radius=10,
        )

        # Featured preview image
        img_x = card_rect.x + (_CARD_W - _PREV_SZ) // 2
        img_y = card_rect.y + 10
        if self._feat_frames:
            # feat frames advance at same clock as icon frames
            feat_frame = self._anim_frame % len(self._feat_frames)
            screen.blit(self._feat_frames[feat_frame], (img_x, img_y))

        # Character name
        name = CHARACTER_ROSTER[self.selected_index].name
        name_surf = self._font_name.render(name, True, BLACK)
        name_y = img_y + _PREV_SZ + 6
        screen.blit(
            name_surf,
            (card_rect.x + (_CARD_W - name_surf.get_width()) // 2, name_y),
        )

        # Play button
        btn_x = card_rect.x + (_CARD_W - _BTN_W) // 2
        btn_y = card_rect.bottom - _BTN_H - 10
        self._play_button_rect = pygame.Rect(btn_x, btn_y, _BTN_W, _BTN_H)
        btn_col = (
            _BTN_HOVER
            if self._play_button_rect.collidepoint(mouse_pos)
            else _BTN_COLOR
        )
        pygame.draw.rect(
            screen, btn_col, self._play_button_rect, border_radius=6
        )
        btn_surf = self._font_btn.render("Play", True, WHITE)
        screen.blit(btn_surf, (
            btn_x + (_BTN_W - btn_surf.get_width()) // 2,
            btn_y + (_BTN_H - btn_surf.get_height()) // 2,
        ))
