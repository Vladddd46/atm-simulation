import socket


class Communicator:
    """
    # Responsible for making requests to server and getting response
    """

    def __init__(self, ip="127.0.0.1", port=5000):
        self.ip = ip
        self.port = int(port)

    def __recv_data_from_sock(self, sock):
        """
        # receives all data from socket <sock>
        """
        BUFF_SIZE = 4096
        data = b""
        while True:
            part = sock.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data

    def make_request(self, request):
        """
        # sends request -> gets response from server.
        """
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.ip, self.port))
        client_socket.sendall(bytes(request, "utf-8"))
        data = self.__recv_data_from_sock(client_socket)
        data = data.decode("utf-8")
        client_socket.close()
        return data
