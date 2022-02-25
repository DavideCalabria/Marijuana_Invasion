import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the joint. """

    def __init__(self, j_game):
        """Create a bullet object at the joint's current position."""
        super().__init__()
        self.screen = j_game.screen
        self.settings = j_game.settings
        self.color = self.settings.bullet_color

        #Create a bullet rect at (0, 0) position and then set correct position. """
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = j_game.joint.rect.midtop

        #Store the bullet's position at a decimal value.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up to the scree."""
        #Update the decimal position of the bullet.
        self.y -= self.settings.bullet_speed
        #Update the rect postion.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
