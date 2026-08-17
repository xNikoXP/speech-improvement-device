import torch
import torchaudio as ta


class Wav2Vec2:
    """Methods required for Wav2Vec2 ASR

    Takes audio tensors and processes them into a transcript

    Attributes:
        device: The decoding hardware
        model: Wav2Vec2 model
        decoder: Method used to turn audio tensors into a readable transcript
    """

    def __init__(self, bundle):
        """Initiliazes Wav2Vec2 ASR model"""
        print("Torch Version: ", torch.__version__)
        print("TorchAudio Version: ", ta.__version__)
        torch.manual_seed(0)
        self.device = torch.device("cpu")
        print("Device: ", self.device)
        print("Sample Rate: ", bundle.sample_rate)
        print("Labels: ", bundle.get_labels())

        self.model = bundle.get_model().to(self.device)
        self.decoder = Wav2Vec2.GreedyCTCDecoder(labels=bundle.get_labels())

    def decodeAudio(self, data: torch.Tensor):
        """Decodes audio and returns transcript
        
        Args:
            data: audio tensor
        
        Returns:
            An iterable string of the models guess on the words spoken in
            the audio tensor.
        """
        data = ta.functional.resample(data, 44100, 16000)
        with torch.inference_mode():
             emission, _ = self.model(data)
        transcript = self.decoder(emission[0])
        return transcript


    class GreedyCTCDecoder(torch.nn.Module):

            def __init__(self, labels, blank=0):
                """Initializes GreedyCTC Decoder"""
                super().__init__()
                self.labels = labels
                self.blank = blank
    
            def forward(self, emission: torch.Tensor) -> str:

                indices = torch.argmax(emission, dim=-1)
                indices = torch.unique_consecutive(indices,dim=-1)
                indices = [i for i in indices if i != self.blank]
                return "".join([self.labels[i] for i in indices])
    



        
