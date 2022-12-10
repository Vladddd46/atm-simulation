import socket
from request import Request
from transaction import Transaction
from global_vars import pending_requests, pending_requests_mtx, logger


# Receives requests from client.
# Parse request data into transaction object.
# Creates its own Request object: {"addr": ip_address, "transaction": transaction_object}
# Adds Request into pending_requests list.
class TransactionsReceiver:
    def __init__(self, ip, port):
        self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket.bind((ip, port))
        self.listening_socket.listen()

    def __recv_data_from_sock(self, sock):
        BUFF_SIZE = 4096
        data = b""
        while True:
            part = sock.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data

    def receive_requests(self):
        while True:
            clientsock, addr = self.listening_socket.accept()
            logger.log("Connected by ", addr)
            try:
                received_data = self.__recv_data_from_sock(clientsock).decode("utf-8")
                trans = Transaction().from_json(received_data)
                req = Request(addr, trans, clientsock)
                pending_requests_mtx.acquire()
                pending_requests.append(req) # adding request in pending_request list, which will be handled by another thread
                pending_requests_mtx.release()
            except Exception as e:
                logger.log(f"Request for {addr} creation failed: {e}")
                pending_requests_mtx.acquire()  
                # closes socket, if something went wrong while transmiting data
                for i in range(len(pending_requests)):
                    if pending_requests[i].sock == clientsock:
                        pending_requests[i].sock.close()
                        pending_requests.pop(i)
                        break
                pending_requests_mtx.release()

    def __del__(self):
        self.listening_socket.close()
