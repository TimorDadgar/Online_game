import pygame
from tiles import Tile
from settings import tile_size, screen_width

class Level:
	def __init__(self, level_data, surface):
		# Level setup
		self.display_surface = surface
		self.setup_level(level_data)
		self.world_shift = 0

	def setup_level(self, layout):
		self.tiles = pygame.sprite.Group()
		# enumerate method gives the index
		for row_index,row in enumerate(layout):
			for col_index,cell in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size

				if cell == 'X':
					tile = Tile((x,y),tile_size)
					self.tiles.add(tile)

	def run(self):
		self.tiles.update(self.world_shift)
		self.tiles.draw(self.display_surface)