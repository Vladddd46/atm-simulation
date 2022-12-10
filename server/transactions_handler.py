from global_vars import pending_requests, pending_requests_mtx, SENDBACK_PORT, DB_NAME, logger
from definitions import TransactionType, Error
from response import Response, ResponseType
import json
import socket


# Retrieves transactions from pending_requests.
# Handles tranaction depending on it`s type.
class TransActionsHandler:
	def get_data_from_db(self, db_name):
		with open(db_name, "r") as file:
			data = json.loads(file.read())
		return data

	def check_balance(self, card_num):
		data = self.get_data_from_db(DB_NAME)
		for card in data.values():
			if card["card_num"] == card_num:
				logger.log("INFO", f"Ceck balance {card_num}")
				return card["balance"]
		return Error("No such card!")

	def get_cash(self, card_num, amount):
		data = self.get_data_from_db(DB_NAME)
		for card in data.values():
			if card["card_num"] == card_num:
				if card["balance"] < amount:
					return Error("Not enough money on balance")
				else:
					card["balance"] = card["balance"] - amount
					with open(DB_NAME, "w") as file:
						file.write(json.dumps(data, sort_keys=True))
					logger.log("INFO", f"Get cash {card_num} amount={amount}")
					return card["balance"]
		return Error("Card is not supported!")

	def send_money(self, sender_card_num, receiver_card_num, amount):
		data = self.get_data_from_db(DB_NAME)
		receiver_exists = False
		for card in data.values():
			if card["card_num"] == receiver_card_num:
				receiver_exists = True
				break
		if not receiver_exists:
			return Error("No such card!")
		for card in data.values():
			if card["card_num"] == sender_card_num:
				if card["balance"] < amount:
					return Error("Not enough money to send on balance")
				else:
					card["balance"] = card["balance"] - amount
		for card in data.values():
			if card["card_num"] == receiver_card_num:
				card["balance"] = card["balance"] + amount
				with open(DB_NAME, "w") as file:
					file.write(json.dumps(data, sort_keys=True))
				logger.log("INFO", f"Sending money {sender_card_num} to {receiver_card_num} | amount={amount}")
				return card["balance"]
		return Error("Card is not supported!")

	def handle_pending_requests(self):
		while True:
			if not pending_requests:
				continue
			pending_requests_mtx.acquire()
			req_to_handle = pending_requests.pop(0)
			pending_requests_mtx.release()
			trans = req_to_handle.transaction
			if trans.ttype == TransactionType.send_money:
				if trans.amount < 0:
					amount *= -1
				balance = self.send_money(trans.sender, trans.receiver, trans.amount)
			elif trans.ttype == TransactionType.get_cash:
				if trans.amount < 0:
					amount *= -1
				balance = self.get_cash(trans.sender, trans.amount)
			elif trans.ttype == TransactionType.check_balance:
				balance = self.check_balance(trans.sender)

			if type(balance) == Error:
				response = Response(retcode=ResponseType.ERROR, data={"msg": balance.msg})
			else:
				response = Response(retcode=ResponseType.OK, data={"balance": balance})

			sendback_data = response.to_json()
			req_to_handle.sock.sendall(bytes(sendback_data, "utf-8"))
			req_to_handle.sock.close();







