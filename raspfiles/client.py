import pickle
import socket

class Client:

    def __init__(self, host="localhost", port=8086):
        self.host = socket.gethostbyname(host)
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """
        Connect to the server at the specified host and port.
        """
        self.sock.connect((self.host, self.port))

    def send(self, data):
        """
        Serializes and sends data through server
        """
        serialized_data = pickle.dumps(data)
        self.sock.sendall(serialized_data)
        print("Sent data to server.")

    def receive(self):
        """
        Receives data from the server and deserializes it.
        """
        data = self.sock.recv(4096)
        if data:
            return pickle.loads(data)
        return None

    def close(self):
        self.sock.close()