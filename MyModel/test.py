import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
# from datasets import load_dataset
import warnings
import os
from pathlib import Path
import time
from glob import glob
import sys

warnings.filterwarnings("ignore")
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"


def speech2text(model_dir, processor_dir):
    device, torch_dtype = "cpu", torch.float32
    print("GPU found!" if torch.cuda.is_available() else "Using CPU!")
    if torch.cuda.is_available():
        device = "cuda:0"
        torch_dtype = torch.float16
    print("Loading model...")
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_dir,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=True,
        use_safetensors=True,
        # attn_implementation="flash_attention_2"
    )
    model.to(device=device, dtype=torch_dtype)
    print("Loading processor...")
    processor = AutoProcessor.from_pretrained(processor_dir)
    # Check device and dtype of model
    print(f"Model device: {next(model.parameters()).device}")
    print(f"Model dtype: {next(model.parameters()).dtype}")
    # Create pipeline
    pipe = pipeline(
        task="automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,
        # return_timestamps=True,
        torch_dtype=torch_dtype,
        device=device,
    )
    # Using toy audio of Dataset library
    # print("Loading dataset...")
    # dataset = load_dataset("distil-whisper/librispeech_long",
    #                        "clean",
    #                        split="validation")
    # sample = dataset[0]["audio"]
    # file audio must have sample rate less than 44100
    return pipe


if __name__ == '__main__':
    start = time.time()

    # 486.5806782245636
    # model_path = "./Whisper_large_v3_model"
    # processor_path = "./Whisper_large_v3_processor"

    # 111.90643119812012
    model_path = "./Whisper_small_model"
    processor_path = "./Whisper_small_processor"

    # 36.89752769470215
    # model_path = "./Whisper_base_model"
    # processor_path = "./Whisper_base_processor"

    pipe = speech2text(model_dir=model_path, processor_dir=processor_path)
    print("GENERATED TEXT:")
    audio_dir = Path(__file__).parent.parent / "inference" / "wav_files"
    audio_name = "buon_hay_vui_1"
    audio_paths = audio_dir.glob(f"{audio_name}*")
    for i in range(len(list(audio_paths))):
        words = pipe(str(audio_dir) + f"\\{audio_name}_{i+1}.wav")
        words = words['text'].split()
        for word in words:
            print(word, end=' ', flush=True)
            time.sleep(0.1)

    end = time.time()
    print(f"\nGENERATED TEXT TIME: {end - start}")
