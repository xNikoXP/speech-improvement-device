from time import sleep

import torch
import torch.multiprocessing as mp
import torchaudio as ta

from datareciever import DataReceiver as dr
from asr import Wav2Vec2
import audiofunctions as fn


NUM_ITER = 500


def getAudio(q: torch.multiprocessing.Queue):
    "Recieves audio from server puts it into q"
    reciever = dr()  
    reciever.stream(q)


def getTranscript(input: torch.multiprocessing.Queue, bundle):
    "Sends audio data to model and returns written transcript"
    model = Wav2Vec2(bundle)
    while True:
        word = torch.from_numpy(input.get()).t()
        print(word.shape)
        print(model.decodeAudio(word))


def main(bundle):
    "Starts the program"
    print("Starting...")
    ctx = mp.get_context("spawn")
    stream_q = ctx.Queue()

    stream_process = ctx.Process(target=getAudio, args=(stream_q,))
    stream_process.start()
    transcript_process = ctx.Process(target=getTranscript, args=(stream_q, bundle))
    
    while stream_q.empty():
        sleep(0.05)

    transcript_process.start()
    stream_process.join()
    transcript_process.join()



if __name__ == "__main__":
    main(
         bundle=ta.pipelines.WAV2VEC2_ASR_BASE_960H
    )

