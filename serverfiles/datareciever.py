import socket
import torch
import functionalaudio as fn
import pickle

class DataReceiver:

    def __init__(self):
        """
            Initializes DataReciever class and establishes socket connection for Raspberry Pi
        """
        self.host = socket.gethostbyname("localhost")
        self.port = 25000
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        with self.sock:
            self.sock.bind((self.host, self.port))
            self.sock.listen(1)
            print(f"Listening on {self.host}:{self.port}...")
            self.conn, self.addr = self.sock.accept()
            print(f"Connection from {self.addr} established.")
  
        
    def stream(self, q: torch.multiprocessing.Queue):
        """
            Receives audio data from Raspberry Pi and puts it in a multiprocessing queue.
        """
        while True:
            data = self.conn.recv(4096)
            if not data:
                break
            q.put(pickle.loads(data))  # Deserialize the received audio data and put it in the queue
            
        self.conn.close()