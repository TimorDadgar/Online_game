from os import walk
import pygame

# Important: make sure to only have png in folders

def import_folder(path):
	surface_list = []
	# os.walk returns 3 things: dirpath, dirnames, filenames
	for _,__,img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			# img = pygame.image.load(full_path).convert()
			# image_surf = img.subsurface(48*48)
			surface_list.append(image_surf)
		
	return surface_list
# import_folder('../graphics/character/run')

def import_spritesheet(path, count, row, width, height):
	surface_list = []
	sprite_sheet = pygame.image.load(path).convert_alpha()
	
	# sprite = pygame.Surface((width, height)).convert()
	# x = 1
	y = 0
	for x in range(count):
		rect = pygame.Rect(width*x, row*height+y, width, height)
		# sprite.blit(sprite_sheet, (0,0), (i*width+x,y,width,height))
		print("x :", width*x,"y :", y)
		surface_list.append(sprite_sheet.subsurface(rect))

	return surface_list