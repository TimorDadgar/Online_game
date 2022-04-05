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
					player_sprite = Player((x,y), self.display_surface)
					self.player.add(player_sprite)
				if cell == 'D':
					dog_sprite = Dog((x,y), self.display_surface)
					self.dog.add(dog_sprite)

	def scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 4 and direction_x < 0:
			self.world_shift = player.max_speed
			player.speed = 0
		elif player_x > screen_width - (screen_width/4) and direction_x > 0:
			self.world_shift = -player.max_speed
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = player.max_speed
		

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

		
	
	def vertical_dog_collision(self):
		doggo = self.dog.sprite
		doggo.apply_gravity()
		self.collide_list = []
		for sprite in self.tiles.sprites():
			self.collide_list.append(sprite.rect.colliderect(doggo.rect))
			if sprite.rect.colliderect(doggo.rect):
				if doggo.direction.y > 0:
					doggo.rect.bottom = sprite.rect.top
					doggo.direction.y = 0
					# doggo jump
					doggo.delta_jump = 0
					doggo.can_jump = True
					doggo.on_ground = True
				elif doggo.direction.y < 0:
					doggo.rect.top = sprite.rect.bottom
					doggo.direction.y = 3
					doggo.on_ceiling = True
		

		if doggo.on_ground and (doggo.direction.y < 0 or doggo.direction.y > 1):
			doggo.on_ground = False
			doggo.can_double_jump = True
			doggo.can_jump = False
		elif doggo.on_ceiling and doggo.direction.y > 0:
			doggo.on_ceiling = False



	def horizontal_dog_collision(self):
		doggo = self.dog.sprite
		if doggo.status == 'walk':
			doggo.rect.x += doggo.direction.x * doggo.speed

			for sprite in self.tiles.sprites():
				if sprite.rect.colliderect(doggo.rect):
					# Here is a possibility for improvement
					# Where the collision is done by looking at the movement of the player
					# In case of ex. a fireball hitting this won't be right
					if doggo.direction.x < 0:
						doggo.rect.left = sprite.rect.right
						doggo.on_left = True
						# X position of where collision occured
						self.current_x = doggo.rect.left
					elif doggo.direction.x > 0:
						doggo.rect.right = sprite.rect.left
						doggo.on_right = True
						self.current_x = doggo.rect.right
			
			if doggo.on_left and (doggo.rect.left < self.current_x or doggo.direction.x >= 0):
				doggo.on_left = False
			if doggo.on_right and (doggo.rect.right > self.current_x or doggo.direction.x <= 0):
				doggo.on_right = False

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
		self.horizontal_dog_collision()
		self.vertical_dog_collision()
		self.dog.draw(self.display_surface)
