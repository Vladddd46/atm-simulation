class Request:

	def __init__(self, ip_addr, transaction, sock):
		self.sock = sock
		self.ip_addr = ip_addr
		self.transaction = transaction

	def __str__(self):
		return f"Request from {selfsock}: {self.ip_add}\n{self.transaction}\n\n"