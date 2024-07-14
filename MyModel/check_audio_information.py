import librosa
from pathlib import Path


def get_sample_rate(audio_file):
    # Read audio file by librosa
    y, sr = librosa.load(audio_file, sr=None)
    # Get sample rate and number of amplitude of this audio
    return len(y), sr


if __name__ == '__main__':
    # audio file path
    audio_file1 = Path(__file__).parent.parent / 'inference' / 'doraemon_music.m4a'
    audio_file2 = Path(__file__).parent.parent / 'inference' / 'buon_hay_vui.m4a'
    audio_file3 = Path(__file__).parent.parent / 'inference' / 'record_1.m4a'

    len_audio1, sample_rate1 = get_sample_rate(audio_file1)
    len_audio2, sample_rate2 = get_sample_rate(audio_file2)
    len_audio3, sample_rate3 = get_sample_rate(audio_file3)

    print(f"Number of amplitude: {len_audio1}")
    print(f"Sample rate: {sample_rate1} Hz")

    print(f"Number of amplitude: {len_audio2}")
    print(f"Sample rate: {sample_rate2} Hz")

    print(f"Number of amplitude: {len_audio3}")
    print(f"Sample rate: {sample_rate3} Hz")
