from client import Client
import audio
import torch.multiprocessing as mp
import threading



#Send Audio through Client
def send_audio(data_q):

    client = Client()
    client.connect()

    while True:
        if not data_q.empty():
            audio_data = data_q.get()
            client.send(audio_data)



def main():
    
    ctx = mp.get_context('spawn')
    q = ctx.Queue()
    stream_process = ctx.Process(target=audio.stream, args=(q,))
    stream_process.start()

    output_process = ctx.Process(target=send_audio, args=(q,))
    output_process.start()

    stream_process.join()
    output_process.join()



if __name__ == "__main__":
    main()