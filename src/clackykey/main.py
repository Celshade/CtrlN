#!/usr/bin/env python3

import os
import sys
from pathlib import Path

# Add src directory to path for direct execution (allows 'python src/clackykey/main.py')
if __name__ == "__main__":
    src_path = str(Path(__file__).parent.parent)
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

import pygame

from clackykey.game import Game


# General NOTE: iirc, pygame counts from the top-down, along the y-axis.
#  i.e. 200 is "lower" than 100


# =================== #
# ### ENTRY POINT ### #
# =================== #
def main() -> None:
    # NOTE: if we keep terminal output, implement Rich to make it look good
    # System data
    print(
        f"\n{'=' * 79}",
        "\nGAME - STARTING",
        f"\n{'=' * 79}",
        f"\nDisplay: {os.environ.get('DISPLAY', 'NOT SET')}",
        f"\nPython: {sys.version.split()[0]}"
    )

    # Initialize Pygame
    pygame.init()
    print(f"Pygame initialized")  # System data
    print(f"Display driver: {pygame.display.get_driver()}")  # System data
    print(f"{'=' * 79}\n")

    # Run the game
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"\n[ERROR] {e}")

        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
