from transactions_handler import TransActionsHandler
from request_receiver import TransactionsReceiver
from threading import Thread
from global_vars import logger, DEBUG, DB_NAME, TEST_DATA
import json
import sys


def init_db(db_name):
	try:
		with open(db_name, "r") as file:
			data = file.read()
	except:
		data = {}
		if DEBUG:
			with open(TEST_DATA, "r") as file:
				data = json.loads(file.read())
		with open(db_name, "w") as file:
			file.write(json.dumps(data, sort_keys=True, indent=4))


def get_argv():
	if len(sys.argv) != 3:
		logger.log("ERROR", "Wrong number of arguments: python3 main_server.py ip port")
		exit(1)
	ip = sys.argv[1]
	try:
		port = int(sys.argv[2])
	except:
		logger.log("ERROR", "Port must be integer")
		exit(1)
	return ip, port


if __name__ == "__main__":
	sys.path.append('..')
	ip, port = get_argv()
	init_db(DB_NAME)
	trans_receiver = TransactionsReceiver(ip, port)
	trans_handler = TransActionsHandler()
	thread_req_receiver = Thread(target=trans_receiver.receive_requests)
	thread_req_handler = Thread(target=trans_handler.handle_pending_requests)
	thread_req_receiver.start()
	thread_req_handler.start()
	thread_req_handler.join()
