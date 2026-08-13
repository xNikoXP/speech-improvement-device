import torch



def normalize_audio(audio: torch.Tensor):
    """
    Normalize the audio tensor to the range [-1, 1].
    """

    max_val = torch.max(torch.abs(audio)) #Get the maximum absolute value in the audio tensor

    if max_val > 0: # Normalizes the audio
        audio = audio / max_val
    return audio



def seperate_segments(data_q: torch.multiprocessing.Queue, segment_length: int, segment_q: torch.multiprocessing.Queue):
    """
    Combines audio tensor in data queue into segments of specified length and puts them in a new queue for inference.
    """
    while not data_q.empty():
        audio = data_q.get() # Get the audio tensor from the data queue
        audio = normalize_audio(audio) # Normalize the audio tensor
        for i in range(0, audio.size(0), segment_length):
            segment = audio[i:i + segment_length]
            segment_q.put(segment)
        print(data_q.empty())