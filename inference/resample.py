import librosa
import soundfile as sf
from pathlib import Path
import warnings
from tqdm import tqdm
warnings.filterwarnings('ignore')


def __create_input_path_object(input_path):
    """
    Checks if the input path and output path are valid.
    Parameters:
        input_path (str): The input path, make sure it exists.
    Return:
        None if the input path is not valid.
        Path object of input path if the input path is valid.
    """
    # Create Path object and check its existence
    input_path = Path(input_path)
    if not input_path.exists():
        print("Audio path does not exist!")
        return None
    # Return
    return input_path


def __display_process(desc=None):
    process = tqdm(range(1), desc=desc)
    process.update(1)
    process.close()


def __auto_create_output_path(input_path, output_folder):
    """
    Automatically create the output path.
    Parameters:
        input_path (str): The input path.
    Returns:
        The output path.
    """
    input_path = str(input_path)
    # split input_path into elements that separated by '\'
    split_input_path = input_path.split('/')  # a list
    # Create first audio name
    audio_name = split_input_path[-1].split('.')[0]
    # Maybe this audio name existed, add number behind audio_name to make it
    # different from existed one.
    count = 1
    while (Path(output_folder + "/" + audio_name + f"_{str(count)}_1.wav")
            .exists()):
        count += 1
    return output_folder + "/" + audio_name + "_" + str(count)


def resample(input_path, output_folder, new_sr, max_duration=None):
    """
    Resample the audio file to a new sr using librosa.resample, split audio into
    smaller audios that have equal duration and save file with .wav extension.
    Parameters:
        input_path (str): The input path
        output_folder (str): The output path
        new_sr (int): The new sr
        max_duration (float): The max duration of the audio file (in seconds)
    Return:
        The resampled audio file and the new sample rate.
    """
    output_path = __auto_create_output_path(input_path, output_folder)
    input_path = __create_input_path_object(input_path)
    if input_path is None:
        return None, new_sr
    print(f"\nInput path: {input_path}")
    print(f"Output path: {Path(output_path+'.wav')}")
    # Load audio
    audio, orig_sr = librosa.load(input_path, sr=None)
    # Change sample rate
    resampled_audio = librosa.resample(audio,
                                       orig_sr=orig_sr,
                                       target_sr=new_sr)
    __display_process("Resampling ")
    # Save new audio
    sf.write(Path(output_path + ".wav"), resampled_audio, new_sr)
    __display_process("Saving ")
    # Split audio into smaller audios that have equal duration if max_duration
    # is not None
    if max_duration is not None:
        process = tqdm(range(len(audio)),
                       desc="Splitting audio into smaller audios ")
        count = 1
        for t in range(0, len(audio), int(max_duration*orig_sr)):
            # Trimming
            t_audio = audio[t: t + int(max_duration*orig_sr)]
            # Resampling
            resampled_audio = librosa.resample(t_audio,
                                               orig_sr=orig_sr,
                                               target_sr=new_sr)
            # Saving
            sf.write(Path(output_path + f"_{count}.wav"),
                     resampled_audio,
                     orig_sr)
            count += 1
            process.update(int(max_duration*orig_sr))
        process.close()
    return str(output_path)


if __name__ == '__main__':
    # Convert all audios in folder audio_files to wav files and pass them into
    # folder wav_files
    audio_paths = Path("audio_files")
    out_folder = "wav_files"
    for item in audio_paths.iterdir():
        item_split = str(item).split('\\')
        audio_path = item_split[0]
        for idx in range(1, len(item_split)):
            audio_path += '/' + item_split[idx]
            out = resample(input_path=audio_path,
                           output_folder=out_folder,
                           new_sr=44100,
                           max_duration=25)
            print(out)
