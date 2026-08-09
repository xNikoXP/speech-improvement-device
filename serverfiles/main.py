from datareciever import DataReceiver as dr
import torch.multiprocessing as mp
import functionalaudio as fn
import torch
import torchaudio as ta
import inferencepipeline as ip

NUM_ITER = 100

def main(bundle):

    print(f"torch.__version__: {torch.__version__}")
    print(f"torchaudio.__version__: {ta.__version__}")

    # Create a DataReceiver Instance
    stream = dr()

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
            segment = cacher(chunk)
            transcript = pipeline.infer(segment)
            print(transcript)

    
    #Creates Process to receive audio data from Raspberry Pi and put it in a multiprocessing queue
    ctx = mp.get_context("spawn")
    data_q = ctx.Queue()
    stream_process = ctx.Process(target=stream.stream, args=(data_q,))
    stream_process.start()

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
            
    

