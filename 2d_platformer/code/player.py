import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		self.import_character_assets()
		self.frame_index = 0
		self.animation_speed = 0.15
		self.image = self.animations['idle'][self.frame_index]

		self.rect = self.image.get_rect(topleft = pos)
		
		# Player movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 8
		self.gravity = 0.8
		self.jump_speed = -13
		self.has_collided = True
		self.can_jump = False
		self.can_double_jump = False
		self.delta_jump = 0

		# Player status
		self.status = 'idle'

	def import_character_assets(self):
		character_path = '../graphics/character/'
		# name of key values in dic is same as folders in character
		self.animations = {'jump':[],'idle':[],'run':[],'fall':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def animate(self):
		animation = self.animations[self.status]
		# Loop over frame_index
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]

	def get_input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
		else:
			self.direction.x = 0

		if pygame.time.get_ticks()-self.delta_jump >=300 and keys[pygame.K_UP]:
			self.delta_jump = pygame.time.get_ticks()
			self.jump()


	def get_status(self):
		# figure out what player is doing
		if self.direction.y < 0:
			self.status = 'jump'
		elif self.direction.y > 1:
			self.status = 'fall'
		else:
			if self.direction.x != 0:
				self.status = 'run'
			else:
				self.status = 'idle'


	def apply_gravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y

	def jump(self):
		if self.can_jump:
			self.direction.y = self.jump_speed
			self.can_jump = False
			self.can_double_jump = True
		elif self.can_double_jump:
			self.direction.y = self.jump_speed
			self.can_double_jump = False

	def update(self):
		self.get_input()
		self.get_status()
		self.animate()
