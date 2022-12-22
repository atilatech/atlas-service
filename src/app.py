from flask import Flask, request
from atlas.transcribe import download_mp3, transcribe_file

app = Flask(__name__)

@app.route('/')
def index():
    return "Atlas Service"

@app.route('/transcribe', methods=['GET', 'POST'])
def transcribe():
    url = request.values.get('q') or request.json.get('urls')
    audio_metadata = download_mp3(url)
    transcribed_audio = transcribe_file(f"./mp3/${audio_metadata['id']}.mp3")

    audio_metadata['transcript'] = transcribed_audio['text']
    
    return {"transcript": transcribed_videos}

if __name__ == '__main__':
    app.run(port=5000, debug=True)
