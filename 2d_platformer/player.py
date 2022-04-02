import pygame


class Player(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		self.image = pygame.Surface((32,64))
		self.image.fill('red')
		self.rect = self.image.get_rect(topleft = pos)
		
		# Player movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 8
		self.gravity = 0.8
		self.jump_speed = -16
		self.available_jumps = 1
		self.delta_jump = 0
		self.has_collided = False

	def get_input(self):
		global delta_jump
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
		else:
			self.direction.x = 0

		if pygame.time.get_ticks()-self.delta_jump >=300 and keys[pygame.K_UP] and self.available_jumps >= 1:
			self.delta_jump = pygame.time.get_ticks()
			self.jump()
			self.available_jumps -= 1

	def apply_gravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y

	def jump(self):
		self.direction.y = self.jump_speed

	def update(self):
		self.get_input()
