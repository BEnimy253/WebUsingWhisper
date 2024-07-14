import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor


def download_model(model_name, model_dir, processor_dir):
    torch_dtype = torch.float32  # Load model by CPU
    # Load model
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_name,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=True,
        use_safetensors=True
    )
    # Load processor
    processor = AutoProcessor.from_pretrained(model_name)
    # Save model and processor
    model.save_pretrained(model_dir)
    processor.save_pretrained(processor_dir)


if __name__ == "__main__":
    # model_to_download = "openai/whisper-large-v3"
    # dir_to_save_model = "./Whisper_large_v3_model/"
    # dir_to_save_processor = "./Whisper_large_v3_processor/"

    # model_to_download = 'openai/whisper-small'
    # dir_to_save_model = "./Whisper_small_model/"
    # dir_to_save_processor = "./Whisper_small_processor/"

    model_to_download = 'openai/whisper-base'
    dir_to_save_model = "./Whisper_base_model/"
    dir_to_save_processor = "./Whisper_base_processor/"

    download_model(model_name=model_to_download,
                   model_dir=dir_to_save_model,
                   processor_dir=dir_to_save_processor)
