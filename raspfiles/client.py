import pickle
import socket
import struct

class Client:

    def __init__(self, host="localhost", port=8086):
        self.host = socket.gethostbyname(host)
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    

    def connect(self):
        """Connect to the server at the specified host and port."""
        self.sock.connect((self.host, self.port))

    def send(self, data):
        """Serielize data and send it to server"""
        serialized_data = pickle.dumps(data)    #Serializes the data

        length = struct.pack('>I', len(serialized_data))   # Length of the serialised data

        self.sock.sendall(length + serialized_data) # sends the serialized data and its length to the server
        print("Sent data to server.")

    def receive(self):
        """Recieve and deserialize data from server and return data"""
        data = self.sock.recv(4096)
        if data:
            return pickle.loads(struct.pack('>I',len(data)) + data)
        return None

    def close(self):
        """Close connection with server"""
        self.sock.close()