import json
import time

import requests
from tqdm import tqdm

from atlas.embed import upload_transcripts_to_vector_db, query_model, does_video_exist
from atlas.utils import convert_seconds_to_string
from config import HUGGING_FACE_API_KEY, HUGGING_FACE_ENDPOINT_URL


def send_transcription_request(url: str):
    payload = json.dumps({
        "inputs": url
    })
    headers = {
        'Authorization': f'Bearer {HUGGING_FACE_API_KEY}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", HUGGING_FACE_ENDPOINT_URL, headers=headers, data=payload)
    return response.json()


def combine_transcripts(video):
    new_transcript_segments = []
    window = 6  # number of sentences to combine
    stride = 3  # number of sentences to 'stride' over, used to create overlap

    video_info = video['video']
    transcript_segments = video['transcript']['segments']
    for i in tqdm(range(0, len(transcript_segments), stride)):
        i_end = min(len(transcript_segments) - 1, i + window)
        text = ' '.join(transcript['text']
                        for transcript in
                        transcript_segments[i:i_end])
        # TODO: Should int (float to seconds) conversion happen at the API level?
        start = int(transcript_segments[i]['start'])
        end = int(transcript_segments[i]['end'])
        new_transcript_segments.append({
            **video_info,
            **{
                'start': start,
                'end': end,
                'title': video_info['title'],
                'text': text,
                'id': f"{video_info['id']}-t{start}",
                'url': f"https://youtu.be/{video_info['id']}?t={start}",
                'video_id': video_info['id'],
            }
        })
    return new_transcript_segments


def transcribe_and_search_video(url, query, verbose=True):
    t0 = time.time()
    if not does_video_exist(url):
        video_with_transcript = send_transcription_request(url)
        video_with_transcript_combined = combine_transcripts(video_with_transcript)

        upload_transcripts_to_vector_db(video_with_transcript_combined)
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
