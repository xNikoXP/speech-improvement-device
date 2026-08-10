from client import Client
import audio
import torch.multiprocessing as mp
import threading


#Send Audio through Client
def send_audio(data_q, client):
    while True:
        if not data_q.empty():
            audio_data = data_q.get()
            client.send(audio_data)



#Listen to Client for Response (Cannot Block)
def listen_for_response(client):
    while True:
        response = client.receive()
        if response:
            print("Received from server:", response)



def main():
    client = Client()
    client.connect()

    ctx = mp.get_context('spawn')
    q = ctx.Queue()
    stream_process = ctx.Process(target=audio.stream, args=(q,))
    stream_process.start()

    output_process = ctx.Process(target=send_audio, args=(q, client))
    output_process.start()

    #t = threading.Thread(target=listen_for_response, args=(client,))
    #t.start()

    stream_process.join()
    output_process.join()
    #t.join()

if __name__ == "__main__":
    main()