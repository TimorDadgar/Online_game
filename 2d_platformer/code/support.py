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
			surface_list.append(image_surf)
		
	return surface_list
# import_folder('../graphics/character/run')