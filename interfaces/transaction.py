import json

class TransactionTypes:
	login = 1
	logout = 2
	send_money = 3
	get_cash = 4
	change_password = 5
	check_balance = 6

class Transaction:


	def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,  sort_keys=True, indent=4)