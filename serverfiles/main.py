from datareciever import DataReceiver as dr
import torch.multiprocessing as mp
import functionalaudio as fn
import torch
import torchaudio as ta
import inferencepipeline as ip
import time

NUM_ITER = 100

def run_stream(data_q: torch.multiprocessing.Queue):
        """
            Initializes DataReciever class and starts streaming audio data from Raspberry Pi.
        """
        stream = dr()
        stream.stream(data_q)

def main(bundle):

    print(f"torch.__version__: {torch.__version__}")
    print(f"torchaudio.__version__: {ta.__version__}")


    print("Building the Pipeline...")
    pipeline = ip.Pipeline(bundle)

    sample_rate = bundle.sample_rate
    segment_length = bundle.segment_length * bundle.hop_length
    context_length = bundle.right_context_length * bundle.hop_length

    cacher = ip.ContextCacher(segment_length, context_length)

    @torch.inference_mode()
    def infer():
        for _ in range(NUM_ITER):
            chunk = segment_q.get()
            segment = cacher(chunk[:, 0])
            transcript = pipeline.infer(segment)
            print(transcript)

    
    #Creates Process to receive audio data from Raspberry Pi and put it in a multiprocessing queue
    ctx = mp.get_context("spawn")
    data_q = ctx.Queue()
    stream_process = ctx.Process(target=run_stream, args=(data_q,))
    stream_process.start()

    while data_q.empty():   # Waits until client is connected to segment audio data
         time.sleep(0.05)

    #Creates process to segement the audio data from the queue and put it in another queue for inference
    segment_q = ctx.Queue()
    segment_separator_process = ctx.Process(target=fn.seperate_segments, args=(data_q, segment_length, segment_q))
    segment_separator_process.start()

    infer()
    stream_process.join()
    segment_separator_process.join()



if __name__ == "__main__":
    bundle = ta.pipelines.EMFORMER_RNNT_BASE_LIBRISPEECH
    main(bundle)
            
    

