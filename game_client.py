import pygame
from network import Network
from player import Player

# Creating window
width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

# will be incremented for each client
clientNumber = 0

# redraws the window and fills with white color
def redrawWindow(win, player, player2):
	win.fill((255, 255, 255))
	player.draw(win)
	player2.draw(win)
	pygame.display.update()


def main():
	# creating main game loop
	run = True
	n = Network()
	p = n.getP()
	clock = pygame.time.Clock()

	while run:
		clock.tick(60)	
		p2 = n.send(p)
		# Pygame.event.get will be a certain event defined by pygame
		# In this case it will be QUIT and trigger the quit event.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
		p.move()
		redrawWindow(win, p, p2)

main()