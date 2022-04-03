import pygame
from tiles import Tile
from settings import tile_size, screen_width
from player import Player
from dog import Dog


class Level:
	def __init__(self, level_data, surface):
		# Level setup
		self.display_surface = surface
		self.setup_level(level_data)
		self.world_shift = 0
		self.current_x = 0

	def setup_level(self, layout):
		self.tiles = pygame.sprite.Group()
		self.player = pygame.sprite.GroupSingle()
		self.dog = pygame.sprite.GroupSingle()
		# enumerate method gives the index
		for row_index,row in enumerate(layout):
			for col_index,cell in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				if cell == 'X':
					tile = Tile((x,y),tile_size)
					self.tiles.add(tile)
				if cell == 'P':
					player_sprite = Player((x,y))
					self.player.add(player_sprite)
				if cell == 'D':
					dog_sprite = Dog((x,y))
					self.dog.add(dog_sprite)

	def scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x
		dog = self.dog.sprite
		dog_x = dog.rect.centerx

		if player_x < screen_width / 4 and direction_x < 0:
			self.world_shift = 8
			player.speed = 0
		elif player_x > screen_width - (screen_width/4) and direction_x > 0:
			self.world_shift = -8
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 8
		

	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()
		self.collide_list = []
		for sprite in self.tiles.sprites():
			self.collide_list.append(sprite.rect.colliderect(player.rect))
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0:
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					# Player jump
					player.delta_jump = 0
					player.can_jump = True
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 3
					player.on_ceiling = True
		

		if player.on_ground and (player.direction.y < 0 or player.direction.y > 1):
			player.on_ground = False
			player.can_double_jump = True
			player.can_jump = False
		elif player.on_ceiling and player.direction.y > 0:
			player.on_ceiling = False



	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				# Here is a possibility for improvement
				# Where the collision is done by looking at the movement of the player
				# In case of ex. a fireball hitting this won't be right
				if player.direction.x < 0:
					player.rect.left = sprite.rect.right
					player.on_left = True
					# X position of where collision occured
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right
		
		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False
	def run(self):
		# Level tiles
		self.tiles.update(self.world_shift)
		self.tiles.draw(self.display_surface)
		self.scroll_x()
		# level player
		self.player.update()
		self.horizontal_movement_collision()
		self.vertical_movement_collision()
		self.player.draw(self.display_surface)
		# Level dog
		self.dog.update(self.world_shift)
		self.dog.draw(self.display_surface)
