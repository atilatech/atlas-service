import os
import json
import requests
import pytube
from pathlib import Path

def download_mp3(urls):
    yt = pytube.YouTube(url)
    yt.streams.filter(only_audio=True).first()\
    .download(output_path='mp3', filename=f"{yt.video_id}.mp3")

    # Add the video info to the list of downloaded videos
    video_info = {
        'id': yt.video_id,
        'thumbnail': yt.thumbnail_url,
        'title': yt.title,
        'views': yt.views,
        'length': length
    }

    return video_info

# Function to transcribe a file
def transcribe_file(file_path):

    return {'text': '<text_here>'}
