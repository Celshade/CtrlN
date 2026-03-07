from typing import NamedTuple


# ====================== #
# ### Character data ### #
# ====================== #
class Character(NamedTuple):
    """Immutable descriptor for a selectable character."""
    id: str
    name: str
    asset_path: str          # sprite used by the Player class in-game
    preview_path: str = ""   # animated webP shown on screen
    description: str = ""
    locked: bool = False     # if True: greyed out & unselectable


# Shared placeholder assets; swap per-entry once unique assets exist.
_DEFAULT_ASSET   = "assets/player.png"
_DEFAULT_PREVIEW = "assets/key_bounce.webP"


def _char(
    cid: str,
    name: str,
    locked: bool = False,
    asset_path: str = _DEFAULT_ASSET,
    preview_path: str = _DEFAULT_PREVIEW,
) -> Character:
    """Convenience constructor that fills in shared asset defaults."""
    return Character(
        id=cid,
        name=name,
        asset_path=asset_path,
        preview_path=preview_path,
        locked=locked,
    )


# NOTE: Add new entries to CHARACTER_ROSTER and CHARACTER_ORDER; grid
# expands automatically up to 15 slots. locked=True shows padlock & prevents
# selection.
CHARACTER_ROSTER: dict[str, Character] = {
    # fmt: off
    "black": _char(
        cid="black",
        name="Black",
        asset_path="assets/player_black.png",
        preview_path="assets/key_bounce_black.webP",
    ),
    "grey": _char(
        cid="grey",
        name="Grey",
        asset_path="assets/player_grey.png",
        preview_path="assets/key_bounce_grey.webP",
    ),
    "dark_green": _char(
        cid="dark_green",
        name="Dark Green",
        asset_path="assets/player_dgreen.png",
        preview_path="assets/key_bounce_dgreen.webP",
    ),
    "blue": _char(
        cid="blue",
        name="Blue",
        asset_path="assets/player_blue.png",
        preview_path="assets/key_bounce_blue.webP",
    ),
    "red": _char(
        cid="red",
        name="Red",
        asset_path="assets/player_red.png",
        preview_path="assets/key_bounce_red.webP",
    ),
    # --- locked below this line ---
    "yellow": _char(
        cid="yellow",
        name="Yellow",
        locked=True,
        asset_path="assets/player_yellow.png",
        preview_path="assets/key_bounce_yellow.webP",
    ),
    "purple": _char(
        cid="purple",
        name="Purple",
        locked=True,
        asset_path="assets/player_purple.png",
        preview_path="assets/key_bounce_purple.webP",
    ),
    "green": _char(
        cid="green",
        name="Green",
        locked=True,
        asset_path="assets/player_green.png",
        preview_path="assets/key_bounce_green.webP",
    ),
    "orange": _char(
        cid="orange",
        name="Orange",
        locked=True,
        asset_path="assets/player_orange.png",
        preview_path="assets/key_bounce_orange.webP",
    ),
    "white": _char(
        cid="white",
        name="White",
        locked=True,
        asset_path="assets/player_white.png",
        preview_path="assets/key_bounce_white.webP",
    ),
    "aqua": _char(
        cid="aqua",
        name="Aqua",
        locked=True,
        asset_path="assets/player_aqua.png",
        preview_path="assets/key_bounce_aqua.webP",
    ),
    "sunset": _char(
        cid="sunset",
        name="Sunset",
        locked=True,
        asset_path="assets/player_sunset.png",
        preview_path="assets/key_bounce_sunset.webP",
    ),
    "silver": _char(
        cid="silver",
        name="Silver",
        locked=True,
        asset_path="assets/player_silver.png",
        preview_path="assets/key_bounce_silver.webP",
    ),
    "gold": _char(
        cid="gold",
        name="Gold",
        locked=True,
        asset_path="assets/player_gold.png",
        preview_path="assets/key_bounce_gold.webP",
    ),
    # fmt: on
}

# Grid display order: maintains selection & unlocking progression sequence.
CHARACTER_ORDER: list[str] = list(CHARACTER_ROSTER.keys())
