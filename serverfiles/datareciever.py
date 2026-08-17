import socket
import pickle
import struct

import torch


class DataReceiver:
    """Methods for communicating with the taser modules 
    
    Establishes a server, listens to connections, maintains connections with clients, \
    and facilitates two way communication.

    Attributes:
        host: The name of local machine
        port: The port the server should listen to
        socket: The socket that facilitates the connectio9ns
        conn: The socket's connection to the client
        addr: The client's address
    """

    def __init__(self):
        "Establish connection with client"
        self.host = socket.gethostbyname("localhost")
        self.port = 8086
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        print(f"Listening on {self.host}:{self.port}...")
        self.conn, self.addr = self.sock.accept()
        print(f"Connection from {self.addr} established.")

    def __recv_full(self, size):
        """Recieves data from client and returns the full intact data
        
        Args:
            size: size of data to recieve from client

        Returns:
            queue: the data recieved from client
        """
        data = b''
        while len(data) < size: #Checks if data is full and requests missing data if it is not
            packet = self.conn.recv(size - len(data))    
            if not packet:
                return None
            data += packet;
        return data

    def stream(self, q: torch.multiprocessing.Queue):
        """Recieves data from client and puts data into a queue
        
        Args:
            q: The queue to store incoming data from client
        """
        print("Streaming...")
        while True:
            header = self.__recv_full(4) # Recieves the first 4 bytes which has the message length
            if not header:
                print("No header")
                break
            length = struct.unpack('>I', header)[0]

            data = self.__recv_full(length)  # Gets the full complete data
            if not data:
                print("No data")
                break
            data = pickle.loads(data)  # Deserializes data
            q.put(data)
            