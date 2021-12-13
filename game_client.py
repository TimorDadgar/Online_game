import pygame
from network import Network

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

		self.update()

	def update(self):
		self.rect = (self.x, self.y, self.width, self.height)

# Will read a string and convert it into pos x and y
def read_pos(str):
	str = str.split(",")
	return int(str[0]), int(str[1])

# create string of the pos x and y
def make_pos(tup):
	return str(tup[0]) + "," + str(tup[1])

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
	startPos = read_pos(n.getPos())
	p = Player(startPos[0], startPos[1], 100, 100, (0,255,0))
	# we have to draw player 2 also from info given from server
	p2 = Player(0, 0, 100, 100, (255,0,0))
	clock = pygame.time.Clock()

	while run:
		clock.tick(60)	
		# Get player 2:s position and update it for us and draw it in redrawWindow 
		p2Pos = read_pos(n.send(make_pos((p.x, p.y))))
		p2.x = p2Pos[0]
		p2.y = p2Pos[1]
		p2.update()
		# Pygame.event.get will be a certain event defined by pygame
		# In this case it will be QUIT and trigger the quit event.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
		p.move()
		redrawWindow(win, p, p2)

main()