from os import error
import socket
from _thread import *
import sys

server = "10.33.38.96"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((server, port))
except socket.error as e:
	str(e)

# Backlog parameter (2), specifies how many unaccepted connections are allowed 
s.listen(2)
print("waiting for a connection, Server Started")

""" same 2 functions as game_client """
# Will read a string and convert it into pos x and y
def read_pos(str):
	# Split by comma
	str = str.split(",")
	return int(str[0]), int(str[1])

# create string of the pos x and y
def make_pos(tup):
	return str(tup[0]) + "," + str(tup[1])

# Hold positions of all players
# player 1 will start at (0,0) etc
pos = [(0,0), (100,100)]

def threaded_client(conn, player):
	# First have to make pos[player] into a string and then send it as bytes
	# print(str.encode(make_pos(pos[player])))
	conn.send(str.encode(make_pos(pos[player])))

	reply = ""
	while True:
		try:
			data = read_pos(conn.recv(2048).decode())
			pos[player] = data
			# Try to get information from client but if
			# we dont get any we disconnect.
			if not data: 
				print("Disconnected")
				break
			else:
				# Super hard coded when sending info to player 1 about player 2
				if player == 1:
					reply = pos[0]
				else:
					reply = pos[1]

				print("Received ", data)
				print("Sending ", reply)
			
			# Sends message to all sockets
			conn.sendall(str.encode(make_pos(reply)))
		except:
			break

	print("Lost connection")
	conn.close()

# Amount of connected players
# This is passed in new thread function
currentPlayer = 0
# Continously looks for connections
while True:
	# conn is an object that represents what is connected
	# addr is an ipv4
	conn, addr = s.accept()
	print("Connected to:", addr)

	start_new_thread(threaded_client, (conn, currentPlayer))
	currentPlayer += 1