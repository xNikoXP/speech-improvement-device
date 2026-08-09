import sounddevice as sd
import torch
from torchaudio.functional import resample

sd.default.device = 0
sd.default.samplerate = 44100
sd.default.channels = 1
sd.default.blocksize = 2048


def stream(q):

    def callback(indata, frames, time, status):
        if status:
            print(status)
        data = torch.from_numpy(indata.copy())
        q.put(data)

    with sd.InputStream(callback=callback):
        print("Recording... Press Ctrl+C to stop.")
        sd.sleep(50000)  # Record for 10 seconds