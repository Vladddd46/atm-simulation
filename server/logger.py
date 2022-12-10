import time

class Logger:

	def __init__(self, logfile):
		self.logfile = logfile
		with open(self.logfile, "w") as file:
			file.write(f"{time.time()}: Start")


	def log(self, prefix=None, msg=None):
		with open(self.logfile, "a") as file:
			file.write(f"{time.time()}| {prefix} | {msg}\n")