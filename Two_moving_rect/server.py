from os import error
import socket
from _thread import *
import sys
from player import Player
import pickle

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
s.settimeout(10.0)
print("waiting for a connection, Server Started")

# Saving a list of players on serverside, clients can only do commands to update not mess with players
players = [Player(0,0,50,50,(255,0,0)), Player(100,100,50,50,(0,0,255))]

def threaded_client(conn, player):
	conn.send(pickle.dumps(players[player]))

	reply = ""
	while True:
		try:
			data = (pickle.loads(conn.recv(2048)))
			players[player] = data
			# Try to get information from client but if
			# we dont get any we disconnect.
			if not data: 
				print("Disconnected")
				break
			else:
				# Super hard coded when sending info to player 1 about player 2
				if player == 1:
					reply = players[0]
				else:
					reply = players[1]

				print("Received ", data)
				print("Sending ", reply)
			
			# Sends message to all sockets
			conn.sendall(pickle.dumps(reply))
		except:
			break

	print("Lost connection")
	conn.close()

# Amount of connected players
# This is passed in new thread function
currentPlayer = 0
# Continously looks for connections
run = True
while run:
	# Implemented so I can get my KeyboardInterrup Ctrl+c through
	try:
		# conn is an object that represents what is connected
		# addr is an ipv4
		conn, addr = s.accept()
		print("Connected to:", addr)

		start_new_thread(threaded_client, (conn, currentPlayer))
		currentPlayer += 1
	except TimeoutError as e:
		print("No connections were received, error:", e)