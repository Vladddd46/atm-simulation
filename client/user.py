import socket
import json
import random
import sys

class Communicator:

	def __init__(self, ip="127.0.0.1", port=5000):
		self.ip=ip
		self.port=int(port)
	
	def __recv_data_from_sock(self, sock):
		BUFF_SIZE = 4096
		data = b""
		while True:
			part = sock.recv(BUFF_SIZE)
			data += part
			if len(part) < BUFF_SIZE:
				break
		return data

	def make_request(self, request):
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.connect((self.ip, self.port))
		client_socket.sendall(bytes(request, "utf-8"))
		data = self.__recv_data_from_sock(client_socket)
		data = data.decode("utf-8")
		client_socket.close()
		return data


class AuthorizedUser:

	def __init__(self, communicator, card_num, cvv, date):
		self.card_num = card_num
		self.cvv = cvv
		self.date = date
		self.communicator = communicator

	def get_balance(self):
		req = json.dumps({"ttype": 3, "sender": self.card_num})
		response = self.communicator.make_request(req)
		return response

	def get_cash(self, amount):
		req = json.dumps({"ttype": 2, "sender": self.card_num, "amount": amount})
		response = self.communicator.make_request(req)
		return response

	def send_money(self, receiver, amount):
		req =  json.dumps({"ttype": 1, "sender": self.card_num, "receiver": receiver,"amount": amount})
		response = self.communicator.make_request(req)
		return response
		
	def __str__(self):
		return f"card_num:{self.card_num}\ncvv:{self.cvv}\ndate:{self.date}\n"
