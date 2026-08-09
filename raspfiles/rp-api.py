def electric_shock():
    print("Electric shock! ⚡")

from copyreg import pickle
import socket

host = socket.gethostbyname("localhost")
port = 25000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))

    import torch.multiprocessing as mp
    import datacollector as dc

    #Creates and executes a process to collect audio stream
    ctx = mp.get_context("spawn")
    q = ctx.Queue()
    p = ctx.Process(target=dc.stream, args=(q,))
    p.start()

    print("Starting audio stream...")

    #outdata = pickle.dumps(q) #Serialize the audio data from the queue
    p.join() #Wait for the process to finish

    #s.sendall(outdata)
    s.close()
