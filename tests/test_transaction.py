import sys
sys.path.append('..')
from interfaces.transaction import Transaction
from interfaces.definitions import TransactionType, Currency
import pytest
import json

@pytest.mark.parametrize("transaction_data", [{"ttype": TransactionType.send_money, "amout": 100, "currency": Currency.UAH, "receiver": 000000000}]) 
def test_transaction(transaction_data):
	json_data = json.dumps(transaction_data, sort_keys=True)
	trans = Transaction().from_json(json_data)
	assert(trans.ttype==transaction_data["ttype"])
	assert(trans.amount==transaction_data["amount"])
	assert(trans.currency==transaction_data["currency"])
	assert(trans.receiver==transaction_data["receiver"])
	trans_in_json = trans.to_json()
	assert(type(trans_in_json)==str)