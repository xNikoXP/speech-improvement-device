import torchaudio
import torch

class Pipeline:

    def __init__(self, bundle: torchaudio.pipelines.RNNTBundle, beam_width: int = 10):
        self.bundle = bundle
        self.feature_extractor = bundle.get_streaming_feature_extractor()
        self.decoder = bundle.get_decoder()
        self.token_processor = bundle.get_token_processor()

        self.beam_width = beam_width

        self.state = None
        self.hypothesis = None

    def infer(self, segment: torch.Tensor):
        features, length = self.feature_extractor(segment)
        self.hypothesis, self.state = self.decoder.infer(
            features, length, self.beam_width, state=self.state, hypothesis=self.hypothesis
        )
        transcript = self.token_processor(self.hypothesis[0][0], lstrip=False)
        return transcript





class ContextCacher: 

    def __init__(self, segment_length: int, context_length: int):
        self.segment_length = segment_length
        self.context_length = context_length
        self.context = torch.zeros([context_length])

    def __call__(self, chunk: torch.Tensor):
        if chunk.size(0) < self.segment_length:
            chunk = torch.nn.functional.pad(chunk, (0, self.segment_length - chunk.size(0)))
        chunk_with_context = torch.cat((self.context, chunk))        
        self.context = chunk[-self.context_length :]
        return chunk_with_context