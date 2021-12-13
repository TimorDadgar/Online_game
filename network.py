# Responsibility is to connect to a server

import socket

class Network:
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = "10.33.38.96"
		self.port = 5555
		self.addr = (self.server, self.port)
		# This is implemented so that each player (client) will have their own id
		self.pos = self.connect()

	def getPos(self):
		return self.pos

	def connect(self):
		try:
			self.client.connect(self.addr)
			return self.client.recv(2048).decode()
		except:
			pass

	def send(self, data):
		# If server cant receive message
		try:
			self.client.send(str.encode(data))
			# This implementation of a recv at each send
			# works in cases where you dont do pings
			# where all send messages want a block reply
			return self.client.recv(2048).decode()
		except socket.error as e:
			print(e)

	# Recv function isn't really neded now since send function is doing recv.
	def recv(self):
		try:
			reply = self.client.recv(2048).decode()
			print(reply)
		except socket.error as e:
			print(e)