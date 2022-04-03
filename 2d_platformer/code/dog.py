import pygame
from support import import_folder, import_spritesheet
from random import randint

class Dog(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		self.import_character_assets()
		self.frame_index = 0
		self.animation_speed = 0.05
		self.image = self.animations['eat'][self.frame_index]

		self.rect = self.image.get_rect(topleft = pos)
		self.rect.y += 20
		# Dog movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 8
		# Status
		self.status = 'eat'
		self.delta_status = 0


	def import_character_assets(self):
		dog_path = '../graphics/dog/shiba.png'
		# name of key values in dic is same as folders in character
		self.animations = {'eat':[],'walk':[]}
		for animation in self.animations.keys():
			if animation == 'eat':
					self.animations[animation] = import_spritesheet(dog_path, 8, 0, 48, 48)
			elif animation == 'walk':
					self.animations[animation] = import_spritesheet(dog_path, 8, 1, 48, 48)


	def animate(self):
		animation = self.animations[self.status]
		# Loop over frame_index
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]
		# self.image = animation[1]


	def get_status(self):
		# Dog is doing randomly
		if pygame.time.get_ticks()-self.delta_status >=5000:
			self.delta_status = pygame.time.get_ticks()
			if randint(0,1) == 1:
				self.status = 'eat'
				print("eating")
			else:
				self.status = 'walk'
				print("walking")

	def apply_gravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y

	def update(self, x_shift):
		self.rect.x += x_shift
		self.get_status()
		self.animate()