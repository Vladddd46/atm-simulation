import json

class Transaction:
    def __init__(
        self, ttype=None, amount=None, currency=None, receiver=None, sender=None
    ):
        self.ttype = ttype
        self.amount = amount
        self.currency = currency
        self.receiver = receiver
        self.sender = sender

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def from_json(self, json_str):
        data = json.loads(json_str)
        self.__dict__ = data
        return self

    def __str__(self):
        return f"Transaction:\n\ttype={self.ttype}\n\tamout={self.amount}\n\tcurrency={self.currency}\n\treceiver={self.receiver}\n\tsender={self.sender}\n\t"
