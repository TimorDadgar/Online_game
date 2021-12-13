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

def threaded_client(conn):
	conn.send(str.encode("Connected"))
	reply = ""
	while True:
		try:
			data = conn.recv(2048)
			reply = data.decode("utf-8")

			# Try to get information from client but if
			# we dont get any we disconnect.
			if not data: 
				print("Disconnected")
				break
			else:
				print("Received ", reply)
				print("Sending ", reply)
			
			# Sends message to all sockets
			conn.sendall(str.encode(reply))
		except:
			break

	print("Lost connection")
	conn.close()

# Continously looks for connections
while True:
	# conn is an object that represents what is connected
	# addr is an ipv4
	conn, addr = s.accept()
	print("Connected to:", addr)

	start_new_thread(threaded_client, (conn,))