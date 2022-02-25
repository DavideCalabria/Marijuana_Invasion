import pygame.font
from pygame.sprite import Group
from joint import Joint

class Scoreboard:
	"""A class to report scoring information."""

	def __init__(self, j_game):
		"""Initialize score-keeping attributes."""
		self.j_game = j_game
		self.screen = j_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = j_game.settings
		self.stats = j_game.stats

		#Font settings for scoring information.
		self.text_color = (220, 53, 69)
		self.font = pygame.font.SysFont(None,48)

		#Prepare the initial score image.
		self.prep_image()

	def prep_image(self):
		"""prepare the initial score image."""
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_joints()

	def prep_score(self):
		"""Turn the score into a rendered image."""
		rounded_score = round(self.stats.score, -1)
		score_str = "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True,
		                                    self.text_color)

		#Display the score at the top right of the screen.
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right -20
		self.score_rect.top = 20

	def show_score(self):
		"""Draw score, level and joints to the screen."""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.joints.draw(self.screen)

	def prep_high_score(self):
		"""Turn the high score into a rendered image."""
		high_score = round(self.stats.high_score, -1)
		high_score_str = "HIGHEST: {:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True,
		                                         self.text_color)

		#Center the high at the top of the screen.
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top

	def check_high_score(self):
		"""Check to see if there is a new high score."""
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = self.stats.score
			self.prep_high_score()

	def prep_level(self):
		"""Turn the level into a render image."""
		level_str = str(self.stats.level)
		self.level_image = self.font.render(level_str, True,
		                                    self.text_color)

		# Position the level below the score.
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom +10

	def prep_joints(self):
		"""Show how many ships are left."""
		self.joints = Group()
		for joint_number in range(self.stats.joints_left):
			joint = Joint(self.j_game)
			joint.rect.x = 10 + joint_number * joint.rect.width
			joint.rect.y = 10
			self.joints.add(joint)
