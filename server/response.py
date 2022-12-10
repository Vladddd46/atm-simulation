import json

class ResponseType:
	OK = 0
	ERROR = 1


class Response:
	def __init__(self, retcode=ResponseType.OK, data={}):
		data["retcode"] = retcode
		self.data = data

	def to_json(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def from_json(self, json_str):
		data = json.loads(json_str)
		self.__dict__ = data
		return self

	def __str__(self):
		return str(self.data)