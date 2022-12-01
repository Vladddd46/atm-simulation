import json


class TransactionType:
    send_money = 1
    get_cash = 2
    check_balance = 4


class Currency:
    USD = 1
    UAH = 2
    EUR = 3


class Transaction:
    def __init__(self, ttype=None, amout=None, currency=None, receiver=None):
        self.ttype = ttype
        self.amout = amout
        self.currency = currency
        self.receiver = receiver

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def from_json(self, json_str):
        data = json.loads(json_str)
        self.__dict__ = data
        return self

    def __str__(self):
        return f"\nTransaction:\n\ttype={self.ttype}\n\tamout={self.amout}\n\tcurrency={self.currency}\n\treceiver={self.receiver}\n\t"
