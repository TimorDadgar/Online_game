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
		self.jump_speed = -13
		self.has_collided = True
		self.can_jump = False
		self.can_double_jump = False
		self.delta_jump = 0

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
