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


def getTranscript(q, bundle):
    "Sends audio data to model and returns written transcript"
    model = Wav2Vec2(bundle)
    while True:
        yield Wav2Vec2.decodeAudio(q)


def main(bundle):
    "Starts the program"
    ctx = mp.get_context("spawn")
    stream_q = ctx.Queue()
    stream_process = ctx.Process(target=getAudio, args=(stream_q,))

    decode_process = ctx.Process(target=getTranscript, args=(stream_q, bundle))


if __name__ == "__main__":
    main(
         bundle=ta.pipelines.WAV2VEC2_ASR_BASE_960H
    )

