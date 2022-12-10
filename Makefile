all:
	python3 main_server.py 127.0.0.1 5004
clear:
	rm -rf ./server/db.json
	rm -rf ./server/logfile.txt
	rm -rf ./server/__pycache__
	rm -rf ./server/__pycache__
	rm -rf ./client/__pycache__
	rm -rf ./tests/__pycache__
	rm -rf ./tests/.pytest_cache
