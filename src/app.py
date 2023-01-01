try:# see: https://github.com/serverless/serverless-python-requirements#dealing-with-lambdas-size-limitations
  import unzip_requirements
except ImportError:
  pass

from flask import Flask, request
from flask_cors import CORS
from atlas.transcribe import transcribe_and_search_video

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "Atlas Service"


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # Handle POST request
        url = request.json.get('url')
        query = request.json.get('q')
    else:
        # Handle GET request
        url = request.args.get('url')
        query = request.args.get('q')

    transcribed_video = transcribe_and_search_video(url, query)

    return {"results": transcribed_video}


if __name__ == '__main__':
    app.run(port=5000, debug=True)
