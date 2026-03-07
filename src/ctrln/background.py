import pygame

from config import WINDOW_WIDTH, WINDOW_HEIGHT, OBJECT_SPEED


class Background:
    """Manages parallax background layers for the game.

    Handles loading, updating (parallax scrolling), resetting, and
    drawing all background layers in back-to-front order.
    """

    # Layer definitions: name, asset path, parallax speed
    # speed=0.0 means static (no scrolling)
    _LAYER_DEFS: list[tuple[str, str, float]] = [
        ("sky_and_grass",       "assets/sky_and_grass.png",       0.0),
        ("big_clouds",          "assets/big_clouds.png",          0.025),
        ("mountains",           "assets/mountains.png",           0.0),
        ("little_clouds",       "assets/little_clouds.png",       0.05),
        ("background",          "assets/background.png",          0.04),
        ("middleground_back",   "assets/middleground_back.png",   0.0625),
        ("middleground_middle", "assets/middleground_middle.png", 0.08),
        ("middleground_front",  "assets/middleground_front.png",  0.2),
        ("ground",              "assets/ground.png",              1.0),
    ]

    def __init__(self) -> None:
        """Load all background layers and initialize scroll offsets."""
        self.layers: list[dict] = []
        for name, path, speed in self._LAYER_DEFS:
            image = pygame.transform.scale(
                pygame.image.load(path),
                (WINDOW_WIDTH, WINDOW_HEIGHT)
            )
            self.layers.append({
                "name": name,
                "image": image,
                "speed": speed,
                "offset": 0,
            })

    def reset(self) -> None:
        """Reset all parallax offsets (call on game restart)."""
        for layer in self.layers:
            layer["offset"] = 0

    def update(self) -> None:
        """Advance parallax offsets for all scrolling layers."""
        for layer in self.layers:
            if layer["speed"] > 0.0:
                layer["offset"] += OBJECT_SPEED * layer["speed"]
                # Wrap for seamless scrolling
                if layer["offset"] < -WINDOW_WIDTH:
                    layer["offset"] += WINDOW_WIDTH

    def draw(self, screen: pygame.Surface) -> None:
        """Draw all layers back-to-front onto screen.

        Args:
            screen: The pygame surface to draw onto.
        """
        for layer in self.layers:
            if layer["speed"] == 0.0:
                # Static layer — single blit
                screen.blit(layer["image"], (0, 0))
            else:
                # Scrolling layer — draw twice for seamless wrap
                offset = int(layer["offset"])
                screen.blit(layer["image"], (offset, 0))
                screen.blit(layer["image"], (offset + WINDOW_WIDTH, 0))
