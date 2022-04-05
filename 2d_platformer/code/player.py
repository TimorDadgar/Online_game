import pygame
from support import import_folder, import_spritesheet

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,surface):
		super().__init__()
		self.import_character_assets()
		self.frame_index = 0
		self.animation_speed = 0.15
		self.image = self.animations['idle'][self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)
		
		# Player movement
		self.direction = pygame.math.Vector2(0,0)
		self.max_speed = 20
		self.speed = self.max_speed
		self.gravity = 0.8
		self.jump_speed = -13
		self.has_collided = True
		self.can_jump = False
		self.can_double_jump = False
		self.delta_jump = 0

		# Player status
		self.status = 'idle'
		self.facing_right = True
		self.on_ground = False
		self.on_ceiling = False
		self.on_right = False
		self.on_left = False

		# Player dust particles
		self.import_dust_run_particles()
		self.dust_frame_index = 0
		self.dust_animation_speed = 0.4
		self.display_surface = surface


	def import_character_assets(self):
		character_path = '../graphics/character/'
		# name of key values in dic is same as folders in character
		self.animations = {'jump':[],'idle':[],'run':[],'fall':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def import_dust_run_particles(self):
		# boom_path = '../graphics/character/boom.png'
		# self.dust_run_particles = import_spritesheet(boom_path,3,0,512,512)
		boom_path = '../graphics/character/new_boom.png'
		self.dust_run_particles = import_spritesheet(boom_path,3,0,256/3,256/3)


	def animate(self):
		animation = self.animations[self.status]
		# Loop over frame_index
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		image = animation[int(self.frame_index)]
		if self.facing_right:
			self.image = image
		else:
			flipped_image = pygame.transform.flip(image,True,False)
			self.image = flipped_image

		# Set the rect, fix levitating player
		# Ground
		if self.on_ground and self.on_right:
			self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
		elif self.on_ground and self.on_left:
			self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
		elif self.on_ground:
			self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
		# Ceiling
		elif self.on_ceiling and self.on_right:
			self.rect = self.image.get_rect(topright = self.rect.topright)
		elif self.on_ceiling and self.on_left:
			self.rect = self.image.get_rect(topleft = self.rect.topleft)
		elif self.on_ceiling:
			self.rect = self.image.get_rect(midtop = self.rect.midtop)

	def run_dust_animation(self):
		if self.status == 'run' and self.on_ground:
			self.dust_frame_index += self.dust_animation_speed
			if self.dust_frame_index >= len(self.dust_run_particles):
				self.dust_frame_index = 0

			dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

			if self.facing_right:
				pos = self.rect.bottomleft - pygame.math.Vector2(50, 60)
				self.display_surface.blit(dust_particle, pos)
			if not self.facing_right:
				pos = self.rect.bottomright - pygame.math.Vector2(40, 60)
				flipped_dust_particle = pygame.transform.flip(dust_particle, True, False)
				self.display_surface.blit(flipped_dust_particle, pos)

	def get_input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
			self.facing_right = True
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
			self.facing_right = False

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
		self.run_dust_animation()
