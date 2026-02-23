"""ClackyKey - A rhythmic tapping game."""

__version__ = "0.1.0"
__author__ = "Celshade"

from .models.profiles import Profile
from .models.ranks import RANKS

__all__ = ["Profile", "RANKS", "__version__", "__author__"]
