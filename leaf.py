import pygame
from pygame.sprite import Sprite

class Leaf(Sprite):
    """A class to rapresent a single leaf in the fleet."""

    def __init__(self, j_game):
        """Initialize the leaf and set its starting position."""
        super().__init__()
        self.screen = j_game.screen
        self.settings = j_game.settings

        #Load the leaf image and set its rect attribute
        self.image = pygame.image.load('images/leaf.bmp')
        self.rect = self.image.get_rect()

        #Start each leaf at the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the leaf's exact position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if leaf is at the edge of the screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move the leaf to the right or left."""
        self.x += (self.settings.leaf_speed * self.settings.fleet_direction)
        self.rect.x = self.x
