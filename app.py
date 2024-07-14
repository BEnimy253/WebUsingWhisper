from flask import (Flask, render_template, Response, request, redirect, url_for,
                   jsonify)
from MyModel.test import speech2text
from inference.resample import resample
import time
import os
from glob import glob
from tqdm import tqdm
import librosa
import soundfile as sf

# Create instance of Flask object
app = Flask(__name__, template_folder='templates', static_folder='static')
# Load model and processor
model_path = "./MyModel/Whisper_small_model"
processor_path = "./MyModel/Whisper_small_processor"
# Create pipeline
pipe = speech2text(model_dir=model_path, processor_dir=processor_path)
# Create absolute save dir 'inference/audio_files'
SAVE_AUDIOS_FOLDER = os.path.join(os.path.dirname(__file__),
                                  'inference/audio_files')
INFERENCE_AUDIOS = os.path.join(os.path.dirname(__file__),
                                'static/audios')
if not os.path.exists(SAVE_AUDIOS_FOLDER):
    os.makedirs(SAVE_AUDIOS_FOLDER)
if not os.path.exists(INFERENCE_AUDIOS):
    os.makedirs(INFERENCE_AUDIOS)
# Create global upload path
app.config['SAVE_AUDIOS_FOLDER'] = SAVE_AUDIOS_FOLDER
app.config['INFERENCE_AUDIOS'] = INFERENCE_AUDIOS
# Create list to save all uploaded files (just theirs name)
uploaded_files = []
# List to save state
word_List = list()
extract_files = []


def training(uploaded):
    # Convert all audios in uploaded_files list to wav files and pass them
    # into folder inference/wav_files
    # Save_path is a list that all uploaded_files saved into.
    save_path = "inference/audio_files"
    out_folder = "inference/wav_files"
    for item in uploaded:
        texts = []
        # Get audio name that doesn't have extension behind.
        # audio_name include its parent folders.
        audio_name = resample(input_path=save_path + f'/{item}',
                              output_folder=out_folder,
                              new_sr=44100,
                              max_duration=25)
        for i in range(len(glob(audio_name + "*")) - 1):
            text = pipe(f"{audio_name}_{i + 1}.wav")['text']
            words = text.split()
            for word in words:
                texts.append(word)
        yield texts


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/extract')
def extract_text_from_speech():
    global uploaded_files, word_List
    for text in training(uploaded_files):
        word_List.append(text)
    return render_template('extract_text_from_speech.html',
                           uploaded_files=uploaded_files,
                           word_List=word_List)


# @app.route('/stream')
# def stream():
#     def generate():
#         # Convert all audios in uploaded_files list to wav files and pass them
#         # into folder inference/wav_files
#         # Save_path is a list that all uploaded_files saved into.
#         save_path = "inference/audio_files"
#         out_folder = "inference/wav_files"
#         for item in uploaded_files:
#             # Get audio name that doesn't have extension behind.
#             # audio_name include its parent folders.
#             audio_name = resample(input_path=save_path + f'/{item}',
#                                   output_folder=out_folder,
#                                   new_sr=44100,
#                                   max_duration=25)
#             yield f"data: {audio_name}.wav\n\n"
#             for i in range(len(glob(audio_name+"*"))-1):
#                 text = pipe(f"{audio_name}_{i + 1}.wav")['text']
#                 words = text.split()
#                 for word in words:
#                     yield f"data: {word}\n\n"
#                     time.sleep(0.1)
#         # Announce to client that the text ended.
#         yield f"data: END.\n\n"
#         # Announce to system that closes this generate when finishing task.
#         yield "event: close\ndata: Connection closed\n\n"
#     return Response(generate(), mimetype='text/event-stream')


# Reset uploaded files
@app.route('/reset_uploaded_files')
def reset_uploaded_files():
    global uploaded_files
    uploaded_files = []
    return redirect(url_for('index'))


# Access upload.php and save uploaded files
@app.route('/templates/upload.php', methods=['POST'])
def upload_file():
    global uploaded_files
    if request.method == 'POST':
        file = request.files['file']
        if file:
            split_filename = file.filename.split('.')
            print(split_filename)
            if split_filename[-1] not in ['wav', 'm4a', 'mp3']:
                print("Not in")
            else:
                print("OK")
                file_path = os.path.join(app.config['SAVE_AUDIOS_FOLDER'],
                                         file.filename)
                file.save(file_path)
                uploaded_files.append(file.filename)
            return 'File uploaded successfully!'
        else:
            return 'No file received.'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
