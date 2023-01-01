from datetime import timedelta
import urllib


def convert_seconds_to_string(seconds):
    days, seconds = divmod(seconds, 86400)
    return str(timedelta(days=days, seconds=seconds)).split(',')[-1].strip()


def parse_video_id(url):
    # Parse the URL
    parsed_url = urllib.parse.urlparse(url)

    # Check if the URL is a YouTube URL
    if parsed_url and parsed_url.netloc in ['www.youtube.com', 'youtu.be']:
        # Extract the video ID from the path or query parameters
        if parsed_url.netloc == 'www.youtube.com':
            video_id = urllib.parse.parse_qs(parsed_url.query)['v'][0]
        else:
            video_id = parsed_url.path.split('/')[-1]
        return video_id
    else:
        return None
