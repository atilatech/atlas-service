from flask import Flask, request
from atlas.transcribe import download_mp3, transcribe_file

app = Flask(__name__)

@app.route('/')
def index():
    return "Atlas Service"

@app.route('/search', methods=['GET', 'POST'])
def search():
    url = rrequest.json.get('url')
    query = rrequest.json.get('q')
    video_segments = transcribe_and_search_video(url, query)
    
    return {"results": transcribed_videos}

if __name__ == '__main__':
    app.run(port=5000, debug=True)
