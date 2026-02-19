import pygame
from PIL import Image


# ==================== #
# ### COUNTER CLASS ### #
# ==================== #
class Counter:
    """Animated counter display using sprite assets."""

    # Class-level cached assets (shared across all instances)
    digit_images = {}  # {"0": Surface, "1": Surface, ...}
    transition_gifs = {}  # {"0-1": [frames], "1-2": [frames], ...}
    new_digit_animation = []  # List of frames for new_digit.gif

    def __init__(self, x_pos=-40, y_pos=-30):
        """Initialize counter at given position."""
        self._load_assets_once()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.score = 0
        self.digit_size = 15  # Size of each digit sprite
        self.digit_spacing = 2  # Space between digits
        # Animation state: determines what's currently being animated
        # 'idle' = showing static digits
        # 'new_digit' = playing new_digit.gif animation
        # 'transition' = playing digit transition animation(s)
        self.animation_state = 'idle'
        self.animation_frame = 0
        self.animating_digit_indices = []  # Which digit column(s) are currently animating
        self.transition_direction = {}  # Track which direction each digit is transitioning

    @classmethod
    def _load_assets_once(cls):
        """Load assets only once at class level."""
        if cls.digit_images:  # Already loaded
            return
        # Load digit images (0-9)
        for i in range(10):
            try:
                img = pygame.image.load(f"assets/counter/{i}.png")
                cls.digit_images[str(i)] = img
            except Exception as e:
                print(f"Warning: Could not load counter digit {i}: {e}")
        # Load transition animations (0-1, 1-2, ..., 9-0)
        transitions = [
            "0-1", "1-2", "2-3", "3-4", "4-5", "5-6", "6-7", "7-8", "8-9", "9-0"
        ]
        for transition in transitions:
            try:
                frames = cls._load_gif(f"assets/counter/{transition}.gif")
                cls.transition_gifs[transition] = frames
            except Exception as e:
                print(f"Warning: Could not load counter transition {transition}: {e}")
        # Load new_digit animation
        try:
            cls.new_digit_animation = cls._load_gif("assets/counter/new_digit.gif")
        except Exception as e:
            print(f"Warning: Could not load new_digit animation: {e}")

    @staticmethod
    def _load_gif(filepath):
        """Load all frames from a GIF file."""
        frames = []
        try:
            pil_image = Image.open(filepath)
            try:
                frame_index = 0
                while True:
                    frame = pil_image.convert("RGBA")
                    pygame_frame = pygame.image.fromstring(
                        frame.tobytes(), frame.size, frame.mode
                    )
                    frames.append(pygame_frame)
                    pil_image.seek(pil_image.tell() + 1)
                    frame_index += 1
            except EOFError:
                pass  # End of frames
        except Exception as e:
            print(f"Warning: Could not load gif {filepath}: {e}")
        return frames

    # TODO check this and clean up if possible
    def update_score(self, new_score):
        """Update score and trigger animations as needed."""
        if new_score == self.score:
            return
        old_score = self.score
        self.score = new_score
        # Check if number of digits increased
        old_digits = len(str(old_score))
        new_digits = len(str(new_score))
        if new_digits > old_digits:
            # New digit column added - start new_digit animation
            self.animation_state = 'new_digit'
            self.animation_frame = 0
            self.animating_digit_indices = [0]  # The new leftmost digit
        else:
            # Determine which digit(s) changed and start transition animations
            self._identify_changed_digits(old_score, new_score)

    # TODO clean this up
    def _identify_changed_digits(self, old_score, new_score):
        """Identify which digits changed and set up transition animations."""
        old_str = str(old_score).zfill(len(str(new_score)))
        new_str = str(new_score).zfill(len(str(old_score)))
        # Pad to same length
        max_len = max(len(old_str), len(new_str))
        old_str = old_str.zfill(max_len)
        new_str = new_str.zfill(max_len)
        self.animating_digit_indices = []
        self.transition_direction = {}
        for i in range(max_len):
            if old_str[i] != new_str[i]:
                self.animating_digit_indices.append(i)
                old_digit = old_str[i]
                new_digit = new_str[i]
                # Store transition key like "0-1"
                self.transition_direction[i] = f"{old_digit}-{new_digit}"
        if self.animating_digit_indices:
            self.animation_state = 'transition'
            self.animation_frame = 0

    def update(self):
        """Update animation frame counters."""
        if self.animation_state == 'idle':
            return
        # Advance animation frame
        self.animation_frame += 1
        # Check animation completion based on state
        if self.animation_state == 'new_digit':
            if self.animation_frame >= len(self.new_digit_animation):
                # New digit animation complete, return to idle
                self.animation_state = 'idle'
                self.animation_frame = 0
        elif self.animation_state == 'transition':
            # All transition animations use the same frame index
            # Check if any transition is still playing
            max_frames = 0
            for idx in self.animating_digit_indices:
                transition_key = self.transition_direction[idx]
                if transition_key in self.transition_gifs:
                    max_frames = max(max_frames, len(self.transition_gifs[transition_key]))

            if self.animation_frame >= max_frames:
                # All transitions complete
                self.animation_state = 'idle'
                self.animation_frame = 0

    def draw(self, screen):
        """Draw the counter on screen."""
        score_str = str(self.score)
        x_offset = 0

        # Draw new digit animation if active
        if self.animation_state == 'new_digit' and self.new_digit_animation:
            frame = self.new_digit_animation[min(self.animation_frame, 
                                                 len(self.new_digit_animation) - 1)]
            screen.blit(frame, (self.x_pos, self.y_pos))
            # After new_digit animation, we'll show the static digit next frame
            return

        # Draw digits (from left to right)
        for digit_index, digit_char in enumerate(score_str):

            if (self.animation_state == 'transition' and
                digit_index in self.animating_digit_indices):
                # Play transition animation for this digit
                transition_key = self.transition_direction[digit_index]
                if transition_key in self.transition_gifs:
                    frames = self.transition_gifs[transition_key]
                    if frames:
                        frame = frames[min(self.animation_frame, len(frames) - 1)]
                        screen.blit(frame, (self.x_pos + x_offset, self.y_pos))
            else:
                # Draw static digit
                if digit_char in self.digit_images:
                    screen.blit(self.digit_images[digit_char], 
                               (self.x_pos + x_offset, self.y_pos))

            x_offset += self.digit_size + self.digit_spacing
