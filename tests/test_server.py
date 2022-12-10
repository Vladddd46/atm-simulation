
import pytest
import json
import socket
import time
import os

# to run this test, server on this ip and port must be started
ip = "127.0.0.1"
port = 5002

def send_transaction(trans):
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect((ip, port))
	send_data = json.dumps(trans, sort_keys=True, indent=4)
	client_socket.sendall(bytes(send_data, "utf-8"))
	client_socket.close()

def get_data(path):
	with open(path, "r") as f:
		data = json.loads(f.read())
	return data

def test_get_cache():
	os.chdir("..")
	os.system("make clear")
	os.chdir("server")
	os.system("python3 main_server.py 127.0.0.1 5002")
	t1 = {"ttype": 2, "sender": "111.111.111.111", "amount": 10}
	send_transaction(t1)
	time.sleep(1)
	data = get_data("../server/db.json")
	assert(data["0"]["balance"] == 990)

	t2 = {"ttype": 2, "sender": "111.111.111.111", "amount": 990}
	send_transaction(t2)
	time.sleep(1)
	data = get_data("../server/db.json")	
	assert(data["0"]["balance"] == 0)

	send_transaction(t2)
	time.sleep(1)
	data = get_data("../server/db.json")	
	assert(data["0"]["balance"] == 0)


def test_send_money():
	os.chdir("..")
	os.system("make clear")
	os.chdir("server")
	os.system("python3 main_server.py 127.0.0.1 5002")
	t1 = {"ttype": 1, "sender": "111.111.111.111", "receiver": "222.222.222.222","amount": 500}
	send_transaction(t1)
	time.sleep(1)
	data = get_data("../server/db.json")
	assert(data["1"]["balance"] == 1000)
	assert(data["0"]["balance"] == 500)

	t2 = {"ttype": 1, "sender": "111.111.111.111", "receiver": "222.222.222.222","amount": 499.5}
	send_transaction(t2)
	time.sleep(1)
	data = get_data("../server/db.json")	
	assert(data["1"]["balance"] == 1499.5)
	assert(data["0"]["balance"] == 0.5)

	t3 = {"ttype": 1, "sender": "111.111.111.111", "receiver": "222.222.222.222","amount": 0.5}
	send_transaction(t3)
	time.sleep(1)
	data = get_data("../server/db.json")	
	assert(data["1"]["balance"] == 1500)
	assert(data["0"]["balance"] == 0)

	t4 = {"ttype": 1, "sender": "111.111.111.111", "receiver": "222.222.222.222","amount": 5000}
	send_transaction(t4)
	time.sleep(1)
	data = get_data("../server/db.json")	
	assert(data["1"]["balance"] == 1500)
	assert(data["0"]["balance"] == 0)


