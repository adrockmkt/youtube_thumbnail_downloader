import sys
import os
import requests
from urllib.parse import urlparse, parse_qs

def get_video_id(url: str) -> str:
    """Extract YouTube video ID from URL"""
    parsed_url = urlparse(url)
    if parsed_url.hostname in ("www.youtube.com", "youtube.com"):
        return parse_qs(parsed_url.query)["v"][0]
    elif parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]
    else:
        raise ValueError("Invalid YouTube URL")

def download_thumbnail(video_url: str):
    try:
        video_id = get_video_id(video_url)
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

        response = requests.get(thumbnail_url, stream=True)
        os.makedirs("images", exist_ok=True)
        if response.status_code == 200:
            filename = os.path.join("images", f"thumbnail_{video_id}.jpg")
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"✅ Thumbnail downloaded: {filename}")
        else:
            print("⚠️ Could not fetch max resolution thumbnail. Trying default...")
            fallback_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
            response = requests.get(fallback_url, stream=True)
            filename = os.path.join("images", f"thumbnail_{video_id}_hq.jpg")
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"✅ Thumbnail downloaded: {filename}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python youtube_thumbnail_downloader.py <YouTube_URL>")
    else:
        download_thumbnail(sys.argv[1])