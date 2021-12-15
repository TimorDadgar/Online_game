# Responsibility is to connect to a server

import socket
# will allow for serialized objects, objects made into bytes
import pickle

class Network:
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = "192.168.43.172"
		self.port = 5555
		self.addr = (self.server, self.port)
		# This is implemented so that each player (client) will have their own id
		self.p = self.connect()

	def getP(self):
		return self.p

	def connect(self):
		try:
			self.client.connect(self.addr)
			# pickle that loads decomposes object data (decoding data)
			return pickle.loads(self.client.recv(2048))
		except socket.error as e:
			print(e)
			pass

	def send(self, data):
		# If server cant receive message
		try:
			# pickle.dumps is the same as encoding the data
			self.client.send(pickle.dumps(data))
			# This implementation of a recv at each send
			# works in cases where you dont do pings
			# where all send messages want a block reply
			return pickle.loads(self.client.recv(2048))
		except socket.error as e:
			print(e)

	# Recv function isn't really neded now since send function is doing recv.
	def recv(self):
		try:
			reply = pickle.loads(self.client.recv(2048))
			print(reply)
		except socket.error as e:
			print(e)