import pygame
from support import import_folder, import_spritesheet
from random import randint

class Dog(pygame.sprite.Sprite):
	def __init__(self,pos,surface):
		super().__init__()
		self.import_character_assets()
		self.frame_index = 0
		self.animation_speed = 0.15
		self.image = self.animations['eat'][self.frame_index]

		self.rect = self.image.get_rect(topleft = pos)
		self.rect.y += 20

		# Dog movement
		self.direction = pygame.math.Vector2(1,0)
		self.max_speed = 1
		self.speed = self.max_speed
		self.gravity = 0.8
		self.jump_speed = -13
		self.has_collided = True
		self.can_jump = False
		self.can_double_jump = False
		self.delta_jump = 0
		# Status
		self.status = 'eat'
		self.facing_right = True
		self.on_ground = False
		self.on_ceiling = False
		self.on_right = False
		self.on_left = False
		self.delta_status = 0
		# Surface
		self.display_surface = surface
		self.rect.height = 40



	def import_character_assets(self):
		dog_path = '../graphics/dog/shiba.png'
		# name of key values in dic is same as folders in character
		self.animations = {'eat':[],'walk':[]}
		for animation in self.animations.keys():
			if animation == 'eat':
					self.animations[animation] = import_spritesheet(dog_path, 8, 0, 48, 48)
			elif animation == 'walk':
					self.animations[animation] = import_spritesheet(dog_path, 4, 1, 48, 48)


	def animate(self):
		animation = self.animations[self.status]
		# Loop over frame_index
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		image = animation[int(self.frame_index)]
		# self.image = animation[1]
		image.scroll()
		if not self.facing_right:
			self.image = image
		else:
			flipped_image = pygame.transform.flip(image,True,False)
			self.image = flipped_image

	def get_status(self):
		# Dog is doing randomly
		if pygame.time.get_ticks()-self.delta_status >=5000:
			self.delta_status = pygame.time.get_ticks()
			if randint(0,10) == 1:
				self.status = 'eat'
				print("eating")
			else:
				self.status = 'walk'
				if randint(0,10) == 1:
					self.direction.x = 1
					self.facing_right = True
				else:
					self.direction.x = -1
					self.facing_right = False
				print("walking")

	def apply_gravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y

	def update(self, x_shift):
		self.rect.x += x_shift
		self.get_status()
		self.animate()