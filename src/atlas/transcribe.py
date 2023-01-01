import json
import time

import requests

from atlas.embed import upload_transcripts_to_vector_db, query_model, does_video_exist
from atlas.utils import convert_seconds_to_string
from config import HUGGING_FACE_API_KEY, HUGGING_FACE_ENDPOINT_URL


def send_transcription_request(url: str):
    payload = json.dumps({
        "inputs": "",  # inputs key is not used but our endpoint expects it
        "video_url": url,
    })
    headers = {
        'Authorization': f'Bearer {HUGGING_FACE_API_KEY}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", HUGGING_FACE_ENDPOINT_URL, headers=headers, data=payload)
    return response.json()


def transcribe_and_search_video(url, query, verbose=True):
    t0 = time.time()
    if not does_video_exist(url):
        video_with_transcript = send_transcription_request(url)
        upload_transcripts_to_vector_db(video_with_transcript['encoded_segments'])
    else:
        print(f'Skipping transcribing and embedding.'
              ' Video already exists:{url}')
    results = query_model(query)
    t1 = time.time()
    total = t1 - t0
    if verbose:
        video_length = f"{convert_seconds_to_string(results['matches'][0]['metadata']['length'])} " \
                       "long video" \
            if len(results['matches']) > 0 else 'no video found'
        print(f'Transcribed and searched {video_length} in {total} seconds')
    return results
