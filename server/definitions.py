class TransactionType:
    send_money = 1
    get_cash = 2
    check_balance = 3


class Currency:
    USD = 1
    UAH = 2
    EUR = 3


class Error:
    def __init__(self, msg):
        self.msg = msg
