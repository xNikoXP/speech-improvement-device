import torch
import torchaudio.functional as tf


def normalize_audio(audio: torch.Tensor):
    """Normalize audio tensor and return audio"""
    max_val = torch.max(torch.abs(audio))  

    if max_val > 0:  # Normalizes the audio
        audio = audio / max_val
    return audio