from time import sleep

import torch
import torch.multiprocessing as mp
import torchaudio as ta
import numpy as np

from datareciever import DataReceiver as dr
from asr import Wav2Vec2


NUM_ITER = 500


def getAudio(q: torch.multiprocessing.Queue):
    "Recieves audio from server puts it into q"
    reciever = dr()  
    reciever.stream(q)


def getTranscript(input: torch.multiprocessing.Queue, time, sample_rate, bundle):
    """Prints the transcript

    Takes the given audio and splits it into segments of specified length.
    The audio segments gets fed into the Wav2Vec2 model and prints out
    the written transcript of the audio

    Args:
        input: A queue of audio tensors
        time: Length of audio to feed to the model
        sample_rate: sample_rate of the audio tensors
        bundle: the Wav2Vec2 pipeline
    """
    model = Wav2Vec2(bundle)
    segment_length = sample_rate * time;
    while True:
        buffer = np.empty((1, 1))
        while np.size(buffer) < segment_length:
            buffer = np.concat((buffer, input.get()),dtype='float32')
        buffer = torch.from_numpy(buffer).t()
        print(buffer)
        print(model.decodeAudio(buffer))


def main(bundle):
    "Starts the program"
    print("Starting...")
    ctx = mp.get_context("spawn")
    stream_q = ctx.Queue()

    stream_process = ctx.Process(target=getAudio, args=(stream_q,))
    stream_process.start()
    transcript_process = ctx.Process(target=getTranscript, args=(stream_q, 5, 44100, bundle))
    
    while stream_q.empty():
        sleep(0.05)

    transcript_process.start()
    stream_process.join()
    transcript_process.join()



if __name__ == "__main__":
    main(
         bundle=ta.pipelines.WAV2VEC2_ASR_BASE_960H
    )

