import pygame
from PIL import Image

from profiles import Profile
from ranks import RANKS
from config import (
    PLAYER_START_X, PLAYER_START_Y, PLAYER_SIZE,
    GRAVITY, KEY_POWER, GROUND_Y, FPS,
    SHIELD_INVULNERABILITY_FRAMES
)


# ==================== #
# ### Player Class ### #
# ==================== #
class Player:
    """In-game player sprite with physics, animation, and XP tracking.

    Manages visual representation, collision detection, shield mechanics,
    and integrates with player progression profile.
    """
    def __init__(self, profile: Profile | None = None,
                 asset_path: str = "assets/player.png") -> None:
        """Initialize player entity.

        Args:
            profile:    Optional Profile for XP/rank persistence.
            asset_path: Path to the sprite image used for this character.
        """
        self.profile = profile
        self.x_pos = PLAYER_START_X
        self.y_pos = PLAYER_START_Y
        self.vel = 0
        self.size = PLAYER_SIZE

        # Initialize progression stats (from profile if provided)
        if profile:
            self.player_id = profile.player_id
            self.player_name = profile.player_name
            self.current_xp = profile.current_xp
            self.total_xp = profile.total_xp
            self.rank = profile.rank
            self.highest_rank = profile.highest_rank
            self.prestige = profile.prestige
            self.seasons_played = profile.seasons_played
            self.achievements = profile.achievements.copy()
        else:
            self.player_id = "guest"
            self.player_name = "Guest"
            self.current_xp = 0
            self.total_xp = 0
            self.rank = 0
            self.highest_rank = 0
            self.prestige = 0
            self.seasons_played = 0
            self.achievements = []

        # Player position and physics
        self.x_pos = PLAYER_START_X
        self.y_pos = PLAYER_START_Y
        self.vel = 0
        self.size = PLAYER_SIZE

        # Load player sprite
        self.image = pygame.image.load(asset_path)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
        self.mask = pygame.mask.from_surface(self.image)

        # Load keypress animation frames once at initialization
        self.keypress_animation_frames = self._load_keypress_animation()
        self.animation_frame = 0
        self.playing_animation = False

        # Load shield sprites
        self.shield_image = pygame.image.load("assets/shield_3.2.png")
        self.shield_image = pygame.transform.scale(self.shield_image,
                                                   (self.size, self.size))

        self.shield_image_tier2 = pygame.image.load("assets/shield_3.4.png")
        self.shield_image_tier2 = pygame.transform.scale(
            self.shield_image_tier2,
            (self.size, self.size)
        )

        # Load shield charge animation frames
        self.shield_charge_animation_frames = (
            self._load_shield_charge_animation(
                "assets/shield_fx3.2.webP"
            )
        )
        self.shield_charge_animation_frames_tier2 = (
            self._load_shield_charge_animation(
                "assets/shield_fx3.4.webP"
            )
        )
        self.shield_animation_frame = 0
        self.playing_shield_animation = False
        self.playing_shield_animation_tier2 = False

        # Shield state
        self.shield_charges = 0  # Current number of shields (0-2 max)
        self.next_shield_threshold = 5  # Score threshold for next shield

        # Invulnerability tracking
        # Frames remaining of invulnerability after shield break
        self.invulnerability_frames = 0  # FIXME edit this

    # ========================== #
    # ### Progression Logic ### #
    # ========================== #

    def get_current_rank(self) -> int:
        """Get player's current rank based on total XP.

        Returns:
            int: Rank ID (0-7), where 1=Diamond (highest),
                0=Unranked.
        """
        if self.total_xp == 0:
            return 0

        for rank_id in range(1, 8):
            if self.total_xp >= RANKS[rank_id]["min_points"]:
                return rank_id

        return 7  # Default to Bamboo

    def get_progress(self) -> dict:
        """Calculate current rank, XP toward next rank, progress %.

        Returns:
            dict: Contains current_rank, current_rank_name,
                xp_in_rank, xp_to_next_rank, progress_percent,
                next_rank.
        """
        current_rank = self.get_current_rank()
        current_rank_name = RANKS[current_rank]["name"]

        # Handle Unranked special case
        if current_rank == 0:
            return {
                "current_rank": 0,
                "current_rank_name": "Unranked",
                "xp_in_rank": 0,
                "xp_to_next_rank": 100,
                "progress_percent": 0.0,
                "next_rank": 7
            }

        # Handle Diamond (highest rank)
        if current_rank == 1:
            current_min = RANKS[1]["min_points"]
            return {
                "current_rank": current_rank,
                "current_rank_name": current_rank_name,
                "xp_in_rank": self.total_xp - current_min,
                "xp_to_next_rank": 0,
                "progress_percent": 100.0,
                "next_rank": None
            }

        # All other ranks
        current_min = RANKS[current_rank]["min_points"]
        next_min = RANKS[current_rank - 1]["min_points"]

        xp_in_rank = self.total_xp - current_min
        xp_to_next = next_min - current_min
        progress_percent = (xp_in_rank / xp_to_next) * 100

        return {
            "current_rank": current_rank,
            "current_rank_name": current_rank_name,
            "xp_in_rank": xp_in_rank,
            "xp_to_next_rank": xp_to_next - xp_in_rank,
            "progress_percent": min(progress_percent, 100.0),
            "next_rank": current_rank - 1
        }

    def add_xp(self, xp_amount: int) -> dict:
        """Award XP and check for rank promotions.

        Args:
            xp_amount: XP to award (non-negative).

        Returns:
            dict: Contains xp_awarded, new_total_xp, old_rank,
                new_rank, rank_up, rank_name.
        """
        old_rank = self.get_current_rank()
        self.total_xp += xp_amount
        self.current_xp += xp_amount
        new_rank = self.get_current_rank()

        rank_up = new_rank != old_rank and new_rank < old_rank

        if new_rank != self.rank:
            self.rank = new_rank
            if new_rank > self.highest_rank:
                self.highest_rank = new_rank

        return {
            "xp_awarded": xp_amount,
            "new_total_xp": self.total_xp,
            "old_rank": old_rank,
            "new_rank": new_rank,
            "rank_up": rank_up,
            "rank_name": RANKS[new_rank]["name"]
        }

    def get_unlocks(self) -> list[str]:
        """Get all unlocks available at current XP level.

        Returns:
            list: All feature/cosmetic unlocks available.
        """
        current_rank = self.get_current_rank()
        unlocks = []

        if current_rank == 0:
            return []

        for rank_id in range(current_rank, 7, 1):
            unlocks.extend(RANKS[rank_id]["unlocks"])

        unlocks.extend(RANKS[7]["unlocks"])

        return list(set(unlocks))

    def get_rank_up_info(
        self,
        old_rank: int,
        new_rank: int
    ) -> dict:
        """Get rank-up notification info.

        Args:
            old_rank: Previous rank ID.
            new_rank: New rank ID.

        Returns:
            dict: Rank-up notification with unlocks.
        """
        from clackykey.ranks import get_rank_unlocks

        unlocked_features = get_rank_unlocks(new_rank)
        rank_name = RANKS[new_rank]["name"]

        notification = (
            f"Rank up! You've been promoted to {rank_name}! "
            f"You unlocked: {', '.join(unlocked_features)}"
        )

        return {
            "promotion": True,
            "rank_name": rank_name,
            "unlocked_features": unlocked_features,
            "notification": notification
        }

    def display_progress(self) -> str:
        """Display player's rank, XP progress, and next rank info.

        Returns:
            str: Formatted progress display.
        """
        progress = self.get_progress()
        current_rank = progress["current_rank"]
        current_name = progress["current_rank_name"]

        output = f"{'PLAYER STATS':^80}\n"
        output += "=" * 80 + "\n"
        output += f"Player ID: {self.player_id}\n"
        output += f"Player: {self.player_name}\n"
        output += f"Rank: {current_name} (Rank {current_rank})\n"
        output += f"Total XP: {self.total_xp:,}\n"

        if progress["next_rank"] is not None:
            next_rank_name = RANKS[progress["next_rank"]]["name"]
            next_min = RANKS[progress["next_rank"]]["min_points"]

            output += f"Next Rank: {next_rank_name} ({next_min:,}+ XP)\n"

            bar_length = 50
            filled_length = int(
                bar_length * progress["progress_percent"] / 100
            )
            bar = ("█" * filled_length +
                   "░" * (bar_length - filled_length))

            output += f"Progress: {bar} "
            output += f"{progress['progress_percent']:.0f}% "
            output += (f"({progress['xp_to_next_rank']:,} "
                       f"XP to next)\n")
        else:
            output += "Next Rank: None (Maximum rank achieved!)\n"
            output += "Progress: ██████████████████ 100%\n"

        return output

    def save(self, filename: str = None) -> bool:
        """Save player progression to profile file.

        Args:
            filename: Path to save to. If None and profile exists,
                uses default player_data/{player_id}.json

        Returns:
            bool: Success status. False if no profile.
        """
        if self.profile is None:
            return False

        # Pass current stats to save_to_file, which handles update_profile
        return self.profile.save_to_file(filename, {
            "current_xp": self.current_xp,
            "total_xp": self.total_xp,
            "rank": self.rank,
            "highest_rank": self.highest_rank,
            "achievements": self.achievements
        })

    def apply_unlocks(self) -> None:
        """Process unlocks and apply them to gameplay.

        This method checks what unlocks the player has and applies
        relevant gameplay effects (e.g., shield tiers, XP multipliers).
        """
        unlocks = self.get_unlocks()

        # TODO apply unlock effects based on unlocks list
        # Apply shield upgrades from unlocks
        if "shield_charge+1" in unlocks:
            # This unlock allows max 3 shields instead of 2
            # (Would need config change to support)
            pass

        if "shield_strength+1" in unlocks:
            # Upgrade shield tier visuals/mechanics
            # Already using tier system based on shield_charges
            pass

        # XP multipliers would be applied at award time
        # (Not implemented in current add_xp, could be added)

    def _load_keypress_animation(self):
        """Load and cache all frames from the keypress animation webp."""
        frames = []
        try:
            pil_image = Image.open("assets/keypress_thruster_fx.webP")

            try:
                while True:
                    frame = pil_image.convert("RGBA")
                    frame = frame.resize((self.size, self.size),
                                         Image.Resampling.LANCZOS)
                    pygame_frame = pygame.image.fromstring(
                        frame.tobytes(), frame.size, frame.mode
                    )
                    frames.append(pygame_frame)
                    pil_image.seek(pil_image.tell() + 1)
            except EOFError:
                pass  # End of frames
        except Exception as e:
            print(f"Warning: Could not load keypress animation: {e}")
        return frames

    def _load_shield_charge_animation(self, filepath=None):
        """Load shield charge animation from given filepath."""
        if filepath is None:
            filepath = "assets/shield_key_fx3.2.webP"
        """Load and cache all frames from the shield charge animation webp."""
        frames = []
        try:
            pil_image = Image.open(filepath)

            try:
                while True:
                    frame = pil_image.convert("RGBA")
                    frame = frame.resize((self.size, self.size),
                                         Image.Resampling.LANCZOS)
                    pygame_frame = pygame.image.fromstring(
                        frame.tobytes(), frame.size, frame.mode
                    )
                    frames.append(pygame_frame)
                    pil_image.seek(pil_image.tell() + 1)
            except EOFError:
                pass  # End of frames
        except Exception as e:
            msg = (
                f"Warning: Could not load shield charge animation "
                f"from {filepath}: {e}"
            )
            print(msg)
        return frames

    def update(self) -> None:
        self.vel += GRAVITY
        self.y_pos += self.vel
        self.rect.topleft = (self.x_pos, self.y_pos)

        # Update animation frame
        if self.playing_animation:
            self.animation_frame += 1
            if self.animation_frame >= len(self.keypress_animation_frames):
                self.playing_animation = False
                self.animation_frame = 0

        # Update shield charge animation frame (tier 1)
        if self.playing_shield_animation:
            self.shield_animation_frame += 1
            if (self.shield_animation_frame >=
                    len(self.shield_charge_animation_frames)):
                self.playing_shield_animation = False
                self.shield_animation_frame = 0

        # Update shield charge animation frame (tier 2)
        if self.playing_shield_animation_tier2:
            self.shield_animation_frame += 1
            if (self.shield_animation_frame >=
                    len(self.shield_charge_animation_frames_tier2)):
                self.playing_shield_animation_tier2 = False
                self.shield_animation_frame = 0

        # Update invulnerability frames
        if self.invulnerability_frames > 0:
            self.invulnerability_frames -= 1

    def keypress(self) -> None:
        self.vel = KEY_POWER
        # Trigger the keypress animation
        if self.keypress_animation_frames:
            self.animation_frame = 0
            self.playing_animation = True

    def has_shield(self) -> bool:
        """Check if shield is currently active (no side effects)."""
        return self.shield_charges > 0

    def is_invulnerable(self) -> bool:
        """Check if player is currently invulnerable after shield break."""
        return self.invulnerability_frames > 0

    def update_shields(self, score) -> bool:
        """Grant new shields based on score threshold.

        Returns:
            bool: True if a new shield charge was granted this call.
        """
        # Grant a new shield when reaching next threshold (capped at 2)
        if score >= self.next_shield_threshold and self.shield_charges < 2:
            self.shield_charges += 1
            self.next_shield_threshold += 5

            # Trigger the appropriate shield charge animation based on tier
            if self.shield_charges == 1:
                # First shield charge
                if self.shield_charge_animation_frames:
                    self.shield_animation_frame = 0
                    self.playing_shield_animation = True
                    self.playing_shield_animation_tier2 = False
            elif self.shield_charges == 2:
                # Second shield charge
                if self.shield_charge_animation_frames_tier2:
                    self.shield_animation_frame = 0
                    self.playing_shield_animation = False
                    self.playing_shield_animation_tier2 = True
            return True
        return False

    def destroy_shield(self) -> None:
        """Destroy the shield when hit."""
        if self.shield_charges > 0:
            self.shield_charges -= 1
            # Reset animation flags when shield is consumed
            self.playing_shield_animation_tier2 = False
            self.playing_shield_animation = False
            # Activate brief invulnerability period after shield break
            self.invulnerability_frames = SHIELD_INVULNERABILITY_FRAMES

    def draw(self, screen, score=0) -> None:
        # Draw player sprite or keypress animation (base layer)
        if (self.playing_animation
            and self.animation_frame < len(self.keypress_animation_frames)
        ):
            current_frame = self.keypress_animation_frames[self.animation_frame]
            anim_rect = current_frame.get_rect(
                center=(self.rect.centerx, self.rect.centery)
            )
            screen.blit(current_frame, anim_rect)
        else:
            screen.blit(self.image, self.rect)

        # Draw shield charge animation if active (on top, highest priority)
        if (self.playing_shield_animation and
                self.shield_animation_frame <
                len(self.shield_charge_animation_frames)):
            current_frame = (
                self.shield_charge_animation_frames
                [self.shield_animation_frame]
            )
            anim_rect = current_frame.get_rect(
                center=(self.rect.centerx, self.rect.centery)
            )
            screen.blit(
                current_frame, anim_rect,
                special_flags=pygame.BLEND_RGBA_MAX
            )
        elif (self.playing_shield_animation_tier2 and
                self.shield_animation_frame <
                len(self.shield_charge_animation_frames_tier2)):
            current_frame = (
                self.shield_charge_animation_frames_tier2
                [self.shield_animation_frame]
            )
            anim_rect = current_frame.get_rect(
                center=(self.rect.centerx, self.rect.centery)
            )
            screen.blit(
                current_frame, anim_rect,
                special_flags=pygame.BLEND_RGBA_MAX
            )

        # Draw shield if it's active - only when no shield charge animation
        if self.shield_charges == 2 and not self.playing_shield_animation_tier2:
            screen.blit(self.shield_image_tier2, self.rect)
        elif self.shield_charges == 1 and not self.playing_shield_animation:
            screen.blit(self.shield_image, self.rect)

    def is_dead(self) -> bool:
        return self.y_pos + self.size >= GROUND_Y or self.y_pos < -14
