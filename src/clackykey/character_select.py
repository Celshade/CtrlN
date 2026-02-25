from typing import NamedTuple

import pygame

from config import WINDOW_WIDTH, WINDOW_HEIGHT, SCALE, BLACK, WHITE, YELLOW


# ----------------------------------------- #
# Layout constants (tuned for 890×400 px)   #
# ----------------------------------------- #
_CARD_W       = 200
_CARD_H       = 270
_PREVIEW_SIZE = 150   # square preview image
_GAP          = 24    # horizontal gap between cards

_BTN_W        = 140
_BTN_H        = 40
_BTN_COLOR    = (50, 200, 80)
_BTN_HOVER    = (80, 230, 110)

_CARD_BG      = (240, 240, 240)
_SEL_BORDER   = YELLOW
_UNSEL_BORDER = (180, 180, 180)
_BORDER_W     = 4

# Fonts are fixed-pixel, not SCALE-based, because the character select
# screen is designed to sit within the fixed 890×400 game window.
_FONT_TITLE   = 30
_FONT_NAME    = 24
_FONT_BTN     = 22
_FONT_HINT    = 18


# ====================== #
# ### Character data ### #
# ====================== #
class CharacterDef(NamedTuple):
    """Immutable descriptor for a selectable character."""
    id: str
    name: str
    asset_path: str
    description: str = ""


# NOTE Add new entries here to extend the roster - they'll appear automatically.
CHARACTER_ROSTER: list[CharacterDef] = [
    CharacterDef(
        id="default",
        name="Clacky",
        asset_path="assets/player.png",
        description="The original Clacky Key",
    ),
]


# ============================ #
# ### CharacterSelect UI   ### #
# ============================ #
class CharacterSelect:
    """Renders the character selection screen and tracks current selection."""

    def __init__(self) -> None:
        self._font_title = pygame.font.Font(None, _FONT_TITLE)
        self._font_name  = pygame.font.Font(None, _FONT_NAME)
        self._font_btn   = pygame.font.Font(None, _FONT_BTN)
        self._font_hint  = pygame.font.Font(None, _FONT_HINT)

        self.selected_index: int = 0
        self._previews: list[pygame.Surface] = []
        self._play_button_rect: pygame.Rect | None = None

        # Pre-load and scale all preview images once.
        for char in CHARACTER_ROSTER:
            img = pygame.image.load(char.asset_path).convert_alpha()
            img = pygame.transform.scale(img, (_PREVIEW_SIZE, _PREVIEW_SIZE))
            self._previews.append(img)

    # ------------------------------------------------------------------ #
    # Navigation                                                           #
    # ------------------------------------------------------------------ #

    def navigate(self, direction: int) -> None:
        """Cycle selection left (-1) or right (+1), wrapping around roster."""
        self.selected_index = (
            (self.selected_index + direction) % len(CHARACTER_ROSTER)
        )

    @property
    def selected(self) -> CharacterDef:
        """Return the currently highlighted CharacterDef."""
        return CHARACTER_ROSTER[self.selected_index]

    # ------------------------------------------------------------------ #
    # Hit-testing                                                          #
    # ------------------------------------------------------------------ #

    def is_play_clicked(self, pos: tuple[int, int]) -> bool:
        """Return True if *pos* is inside the Play button (left mouse click)."""
        if self._play_button_rect is None:
            return False
        return self._play_button_rect.collidepoint(pos)

    # ------------------------------------------------------------------ #
    # Drawing                                                              #
    # ------------------------------------------------------------------ #

    def draw(self, screen: pygame.Surface) -> None:
        """Render the full character selection UI onto *screen*."""
        n = len(CHARACTER_ROSTER)
        total_w = n * _CARD_W + (n - 1) * _GAP
        start_x = (WINDOW_WIDTH - total_w) // 2

        # Vertically centre cards, leaving room for title above.
        start_y = (WINDOW_HEIGHT - _CARD_H) // 2 + 15

        # ---- Title ----
        title = self._font_title.render("Select Your Character", True, BLACK)
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 8))

        mouse_pos = pygame.mouse.get_pos()

        for i, char in enumerate(CHARACTER_ROSTER):
            card_x = start_x + i * (_CARD_W + _GAP)
            card_rect = pygame.Rect(card_x, start_y, _CARD_W, _CARD_H)

            # Card background
            pygame.draw.rect(screen, _CARD_BG, card_rect, border_radius=10)

            # Border — gold for selected, grey otherwise
            border_color = _SEL_BORDER if i == self.selected_index else _UNSEL_BORDER
            border_w     = _BORDER_W   if i == self.selected_index else 2
            pygame.draw.rect(screen, border_color, card_rect,
                             width=border_w, border_radius=10)

            # Preview image (centred horizontally, 10 px padding from card top)
            img_x = card_x + (_CARD_W - _PREVIEW_SIZE) // 2
            img_y = start_y + 10
            screen.blit(self._previews[i], (img_x, img_y))

            # Character name
            name_surf = self._font_name.render(char.name, True, BLACK)
            name_y = img_y + _PREVIEW_SIZE + 6
            screen.blit(
                name_surf,
                (card_x + (_CARD_W - name_surf.get_width()) // 2, name_y),
            )

            # Play button — only rendered on the selected card
            if i == self.selected_index:
                btn_x = card_x + (_CARD_W - _BTN_W) // 2
                btn_y = start_y + _CARD_H - _BTN_H - 10
                self._play_button_rect = pygame.Rect(btn_x, btn_y,
                                                     _BTN_W, _BTN_H)

                # Hover tint
                btn_color = (
                    _BTN_HOVER
                    if self._play_button_rect.collidepoint(mouse_pos)
                    else _BTN_COLOR
                )
                pygame.draw.rect(screen, btn_color, self._play_button_rect,
                                 border_radius=6)
                btn_surf = self._font_btn.render("Play", True, WHITE)
                screen.blit(btn_surf, (
                    btn_x + (_BTN_W - btn_surf.get_width()) // 2,
                    btn_y + (_BTN_H - btn_surf.get_height()) // 2,
                ))

        # Navigation hint — only visible when roster has more than one entry
        if n > 1:
            hint = self._font_hint.render(
                "\u25c4  \u25ba  to navigate", True, (100, 100, 100)
            )
            screen.blit(
                hint,
                (WINDOW_WIDTH // 2 - hint.get_width() // 2,
                 start_y + _CARD_H + 8),
            )
