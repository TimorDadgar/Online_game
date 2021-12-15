import socket
from _thread import *
import pickle
from game import Game

server = "192.168.43.172"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((server, port))
except socket.error as e:
	str(e)

# Backlog parameter (2), specifies how many unaccepted connections are allowed 
s.listen(2)
# Implemented so I can get my KeyboardInterrup Ctrl+c through
print("waiting for a connection, Server Started")

# Store addresses of connected clients
connected = set()
# Dict. stores games, gameId as key and game object as value
games = {}
# Keep track of current Id, no overwritting games etc.
idCount = 0


def threaded_client(conn, p, gameId):
	global idCount
	conn.send(str.encode(str(p)))

	reply = ""
	while True:
		try:
			data = conn.recv(4096).decode()
			# Checks if game is still in dict. of games
			if gameId in games:
				game = games[gameId]
			
				if not data:
					break
				else:
					if data == "reset":
						game.resetWent()
					elif data != "get":
						game.play(p, data)

					conn.sendall(pickle.dumps(game))
			else:
				break
		except:
			break

	print("Lost connection")
	try:
		del games[gameId]
		print("Closing Game", gameId)
	except:
		pass
	idCount -= 1
	conn.close


# Continously looks for connections
while True:
	# Implemented so I can get my KeyboardInterrup Ctrl+c through
	# conn is an object that represents what is connected
	# addr is an ipv4
	conn, addr = s.accept()
	print("Connected to:", addr)
	# Keep track of how many people are connected at once
	idCount += 1
	p = 0
	# // is integer division
	# How many games do we have, if 7 people we need 4 games
	gameId = (idCount - 1)//2
	# Dont have enough players for game
	if idCount % 2 == 1:
		# Filling dict. with games
		games[gameId] = Game(gameId)
		print("Creating a new game...")
	# Don't need to create a new game
	else:
		games[gameId].ready = True
		p = 1

	start_new_thread(threaded_client, (conn, p, gameId))