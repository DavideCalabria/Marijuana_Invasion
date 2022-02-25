import json

class GameStats:
    """Track statistics for Marijuana Invasion."""

    def __init__(self, j_game):
        """Initialized statistics."""
        self.settings = j_game.settings
        self.reset_stats()

        # Start Marijuana Invasion in an active state.
        self.game_active = False

        # High score should never be reset.
        self.high_score = self.get_saved_high_score()

    def get_saved_high_score(self):
        """Gets high score from file, if it exists."""
        try:
            with open('high_score.json') as f:
                return json.load(f)
        except FileNotFoundError:
            return 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.joints_left = self.settings.joint_limit
        self.score = 0
        self.level = 1
