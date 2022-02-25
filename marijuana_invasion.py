import sys
from time import sleep
import json

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from joint import Joint
from bullet import Bullet
from leaf import Leaf

class JointGame:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Marijuana Invasion")

        #Create an instance to store game statistics,
        # and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.joint = Joint(self)
        self.bullets = pygame.sprite.Group()
        self.leafs = pygame.sprite.Group()

        self._create_fleet()

        # Make Play button.
        self.play_button = Button(self, "Play")

        # Make difficulty level buttons.
        self._make_difficulty_buttons()

    def _make_difficulty_buttons(self):
        """Make buttons that allow to select difficulty level."""
        self.easy_button = Button(self, "Easy")
        self.medium_button = Button(self, "Medium")
        self.difficulty_button = Button(self, "Difficult")

        # Position buttons so they don't all overlap.
        self.easy_button.rect.top = (
                self.play_button.rect.top + 1.5 * self.play_button.rect.height)
        self.easy_button._update_msg_position()

        self.medium_button.rect.top = (
                self.easy_button.rect.top + 1.5 * self.easy_button.rect.height)
        self.medium_button._update_msg_position()

        self.difficulty_button.rect.top = (
                self.medium_button.rect.top + 1.5 * self.medium_button.rect.height)
        self.difficulty_button._update_msg_position()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self.check_events()

            if self.stats.game_active:
                self.joint.update()
                self._update_bullets()
                self._update_leafs()

            self._update_screen()

    def check_events(self):
        # Respond to keypress and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._close_game()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_difficulty_buttons(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            self._start_game()

    def _check_difficulty_buttons(self, mouse_pos):
        """Set the appropriate difficulty level."""
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        medium_button_clicked = self.medium_button.rect.collidepoint(
            mouse_pos)
        diff_button_clicked = self.difficulty_button.rect.collidepoint(
            mouse_pos)
        if easy_button_clicked and not self.stats.game_active:
            self.settings.difficulty_level = 'easy'
            self.settings.initialize_dynamic_settings()
            self._start_game()
        elif medium_button_clicked and not self.stats.game_active:
            self.settings.difficulty_level = 'medium'
            self.settings.initialize_dynamic_settings()
            self._start_game()
        elif diff_button_clicked and not self.stats.game_active:
            self.settings.difficulty_level = 'difficult'
            self.settings.initialize_dynamic_settings()
            self._start_game()

    def _start_game(self):
        """Start a new game."""

        self.play_music()

        # Reset the game settings.
        self.settings.initialize_dynamic_settings()

        #Reset game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_image()

        #Get rid of any remainging leafs and bullets.
        self.leafs.empty()
        self.bullets.empty()

        #Create a new ship and center the leaf.
        self._create_fleet()
        self.joint.center_joint()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    def check_keydown_events(self, event):
        """Responding to key pressing."""
        if event.key == pygame.K_RIGHT:
            self.joint.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.joint.moving_left = True
        elif event.key == pygame.K_q:
            self._close_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            self.settings.bullet_sound.play()
        elif event.key == pygame.K_RETURN and not self.stats.game_active:
            self._start_game()

    def check_keyup_events(self, event):
        """Responding to key pressing."""
        if event.key == pygame.K_RIGHT:
            self.joint.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.joint.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        #Update bullet position.
        self.bullets.update()

        #Get rid of bullets that have disapeared."""
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_leaf_collisions()

    def _check_bullet_leaf_collisions(self):
        """Respond to leaf-bullets collisions."""
        #Remove any bullets and leafs that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.leafs, True, True)

        if collisions:
            for leafs in collisions.values():
                self.stats.score += self.settings.leaf_points * len(leafs)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.leafs:
            self.start_new_level()

    def _update_leafs(self):
        """Check if the fleet is at an edge, then update the positions ao all the leafs in the fleet."""
        self._check_fleet_edges()
        self.leafs.update()

        #Look for leaf-joint collision.
        if pygame.sprite.spritecollideany(self.joint, self.leafs):
            self._joint_hit()

        # Look for leafshitting the bottom of the screen.
        self._check_leafs_bottom()

    def start_new_level(self):
        """Start a new levle when leaf's fleet is destroyed."""
        #Destroy existing bullets and create new fleet_direction.
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()

        #Increase level.
        self.stats.level += 1
        self.sb.prep_level()

    def _check_leafs_bottom(self):
        """Check if any leafs has reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for leaf in self.leafs.sprites():
            if leaf.rect.bottom >= screen_rect.bottom:
                #Treat this the same as the joint got hit.
                self._joint_hit()
                break

    def _joint_hit(self):
        """Respond to the joint hit by the leaf."""
        if self.stats.joints_left > 0:
            # play crash sound effect
            self.settings.ship_crash_sound.play()
            # Decrement joints_left and update scoreboard.
            self.stats.joints_left -= 1
            self.sb.prep_joints()

            # Get rid of remaining leafs and bullets.
            self.leafs.empty()
            self.bullets.empty()

            # Create a new fleet at the center the joint.
            self._create_fleet()
            self.joint.center_joint()

            #Pause.
            sleep(0.5)
        else:
            self.pause_music()
            self.settings.game_over_sound.play()
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Create a fleet of leafs."""
        #Make a leaf and find the number of leaf in a row.
        #Spacing between each width is equal to one leaf width
        leaf = Leaf(self)
        leaf_width, leaf_height = leaf.rect.size
        available_space_x = self.settings.screen_width - (2 * leaf_width)
        number_leaf_x = available_space_x // (2 * leaf_width)

        #Determinate the number of row of leaf that feet in the screen.
        joint_height = self.joint.rect.height
        available_space_y = (self.settings.screen_height - (3 * leaf_height) - joint_height)
        number_row = available_space_y // (2 * leaf_height)

        #Create a full fleet of leaf.
        for row_number in range (number_row):
            for leaf_number in range(number_leaf_x):
                self._create_leaf(leaf_number, row_number)

    def _create_leaf(self, leaf_number, row_number):
        """Create a leaf and place it in a row."""
        leaf = Leaf(self)
        leaf_width, leaf_height = leaf.rect.size
        leaf.x = leaf_width + 2 * leaf_width * leaf_number
        leaf.rect.x = leaf.x
        leaf.rect.y = leaf_height + 2 * leaf.rect.height * row_number
        self.leafs.add(leaf)

    def _check_fleet_edges(self):
        """Respond appropriately if any leafs reach an edge."""
        for leaf in self.leafs.sprites():
            if leaf.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's directions."""
        for leaf in self.leafs.sprites():
            leaf.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update image to the screen, and flit to the new screen."""
        img = pygame.transform.scale(self.settings.bg, (1200, 800))
        self.screen.blit(img, (0, 0))

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.joint.blitme()
        self.leafs.draw(self.screen)

        #Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.difficulty_button.draw_button()

        pygame.display.flip()

    def play_music(self):
        """play background music"""
        pygame.mixer.music.load('music/dont_worry_be_happy.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def pause_music(self):
        """pause background music"""
        pygame.mixer.music.fadeout(500)

    def _close_game(self):
        """Save high score and exit."""
        saved_high_score = self.stats.get_saved_high_score()
        if self.stats.high_score > saved_high_score:
            with open('high_score.json', 'w') as f:
                json.dump(self.stats.high_score, f)

        sys.exit()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    j = JointGame()
    j.run_game()
