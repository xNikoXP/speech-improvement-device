import sounddevice as sd
import torch
from torchaudio.functional import resample
from copyreg import pickle

sd.default.device = 4
sd.default.samplerate = 44100
sd.default.channels = 1
sd.default.blocksize = 16448


def stream(q: torch.multiprocessing.Queue):
    """
    Stream audio from the microphone and put it into a queue.
    """
    def callback(indata, frames, time, status):
        if status:
            print(status)
        data = torch.from_numpy(indata.copy())
        q.put(data)

    with sd.InputStream(callback=callback):
        print("Recording... Press Ctrl+C to stop.")
        sd.sleep(500000)  # Record for 10 seconds
    
