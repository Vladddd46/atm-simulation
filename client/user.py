import json


class AuthorizedUser:
    def __init__(self, communicator, card_num, cvv, date):
        self.card_num = card_num
        self.cvv = cvv
        self.date = date
        self.communicator = communicator

    def get_balance(self):
        """
        # makes request to server, that gets balance of <self.card_num>
        # return {"data": {"retcode": 0, "balance": float}}
        # return {"data": {"retcode": 1, "msg": str}} - in case of error
        """
        req = json.dumps({"ttype": 3, "sender": self.card_num})
        response = self.communicator.make_request(req)
        return response

    def get_cash(self, amount):
        """
        # makes request to server, that gets cash from <self.card_num>
        # return {"data": {"retcode": 0, "balance": float}} - balance after getting cash
        # return {"data": {"retcode": 1, "msg": str}} - in case of error
        """
        req = json.dumps({"ttype": 2, "sender": self.card_num, "amount": amount})
        response = self.communicator.make_request(req)
        return response

    def send_money(self, receiver, amount):
        """
        # makes request to server to send <amount> money from sender(self.card_num) to receiver.
        # return {"data": {"retcode": 0, "balance": float}} - balance after sending money
        # return {"data": {"retcode": 1, "msg": str}} - in case of error
        """
        req = json.dumps(
            {
                "ttype": 1,
                "sender": self.card_num,
                "receiver": receiver,
                "amount": amount,
            }
        )
        response = self.communicator.make_request(req)
        return response

    def __str__(self):
        return f"card_num:{self.card_num}\ncvv:{self.cvv}\ndate:{self.date}\n"
