import pygame

class Settings:
    """A class to store all settings for the game."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg = pygame.image.load('images/background.jpg')

        # Joint settings.
        self.joint_limit = 3

        #Bullet settings.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (220, 53, 69)
        self.bullets_allowed = 3

        # Leaf settings.
        self.fleet_drop_speed = 10

        # Music settings
        self.bullet_sound = pygame.mixer.Sound('music/gun-shot.wav')
        self.ship_crash_sound = pygame.mixer.Sound('music/crash.wav')
        self.game_over_sound = pygame.mixer.Sound('music/sad-game-over.wav')
        self.game_over_sound.set_volume(0.5)

        # How quickly the game speed up.
        self.speedup_scale = 1.2

        # How quickly the alien pointmvalues increse.
        self.score_scale = 1.5

        self.difficulty_level = 'medium'

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize setting that change throughout the game."""
        if self.difficulty_level == 'easy':
            self.joint_limit = 5
            self.bullets_allowed = 10
            self.joint_speed = 0.75
            self.bullet_speed = 1.5
            self.leaf_speed = 1.0
        elif self.difficulty_level == 'medium':
            self.joint_limit = 3
            self.bullets_allowed = 3
            self.joint_speed = 1.5
            self.bullet_speed = 3.0
            self.leaf_speed = 1.5
        elif self.difficulty_level == 'difficult':
            self.joint_limit = 2
            self.bullets_allowed = 3
            self.joint_speed = 3.0
            self.bullet_speed = 6.0
            self.leaf_speed = 2.5

        # fleet_direction of 1 rapresents right; -1 rapresents left.
        self.fleet_direction = 1

        #Scoring.
        self.leaf_points = 20

    def increase_speed(self):
        """Increase speed settings and leaf point value."""
        self.joint_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.leaf_speed *= self.speedup_scale

        self.leaf_points = int(self.leaf_points * self.score_scale)

    def set_difficulty(self, diff_setting):
        if diff_setting == 'easy':
            print('easy')
        elif diff_setting == 'medium':
            pass
        elif diff_setting == 'difficult':
            pass
