import pygame

# Creating window
width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

# will be incremented for each client
clientNumber = 0

class Player():
	def __init__(self, x, y, width, height, color):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = color
		self.rect = (x,y,width,height)
		self.vel = 3


	def draw(self, win):
		pygame.draw.rect(win, self.color, self.rect)

	# Check if buttonpresses
	def move(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_LEFT]:
			self.x -= self.vel

		if keys[pygame.K_RIGHT]:
			self.x += self.vel
		# To go down in pygame: y is more
		
		if keys[pygame.K_UP]:
			self.y -= self.vel

		if keys[pygame.K_DOWN]:
			self.y += self.vel

		self.rect = (self.x, self.y, self.width, self.height)

# redraws the window and fills with white color
def redrawWindow(win, player):
	win.fill((255, 255, 255))
	player.draw(win)
	pygame.display.update()


def main():
	# creating main game loop
	run = True
	p = Player(50, 50, 100, 100, (0,255,0))
	clock = pygame.time.Clock()

	while run:

		clock.tick(120)		
		# Pygame.event.get will be a certain event defined by pygame
		# In this case it will be QUIT and trigger the quit event.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
		p.move()
		redrawWindow(win, p)

main()