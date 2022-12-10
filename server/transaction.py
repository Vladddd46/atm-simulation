import json

class Transaction:
    def __init__(
        self, ttype=None, amount=None, currency=None, receiver=None, sender=None
    ):
        self.ttype = ttype # transaction type. Transaction types can be viewed in defenitions.py
        self.amount = amount # amount of money to get/send. Used in [get_cash, send_money] transaction types.
        self.currency = currency # not used. will be added support of different currencies in future
        self.receiver = receiver # card number of receiver. Used in [send_money] transaction type.
        self.sender = sender # card number of user, that initiates request. Used in [get_cash, send_money, check_balance] transaction.

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def from_json(self, json_str):
        data = json.loads(json_str)
        self.__dict__ = data
        return self

    def __str__(self):
        return f"Transaction:\n\ttype={self.ttype}\n\tamout={self.amount}\n\tcurrency={self.currency}\n\treceiver={self.receiver}\n\tsender={self.sender}\n\t"
