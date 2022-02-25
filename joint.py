import pygame
from pygame.sprite import Sprite

class Joint(Sprite):
    """ A class to manage the joint. """

    def __init__(self, j_game):
        """ Initialize the joint and set its starting position. """
        super().__init__()
        self.screen = j_game.screen
        self.screen_rect = j_game.screen.get_rect()
        self.settings = j_game.settings

        #Load the joint image and get its rect.
        self.image = pygame.image.load('images/joint_small.bmp')
        self.rect = self.image.get_rect()

        #Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the joint's horizontal position
        self.x = float(self.rect.x)

        #Moving flag.
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the joint position based on the movement flag."""
        # Update the joint's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.joint_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.joint_speed

        #Update the rect object from self x and y.
        self.rect.x = self.x

    def blitme(self):
        """ Draw the joint at its current location. """
        self.screen.blit(self.image, self.rect)

    def center_joint(self):
        """Center the joint on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
