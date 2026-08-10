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
        self.port = 8086
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


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
                print("No data received. Closing connection.")
                break
            data = pickle.loads(data)  # Deserialize the received audio data
            print(data)
            q.put(data)  # Deserialize the received audio data and put it in the queue
            
        self.conn.close()