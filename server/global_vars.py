from threading import Lock
from logger import Logger

pending_requests = []
pending_requests_mtx = Lock()

logger = Logger("logfile.txt")

DEBUG = True

DB_NAME = "db.json"

TEST_DATA = "test_data.json"

SENDBACK_PORT = 5005