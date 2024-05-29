#!/bin/env python
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

wled_ip = os.getenv('WLED_IP')
youtube_channel_id = os.getenv('YOUTUBE_CHANNEL_ID')
youtube_api_key = os.getenv('YOUTUBE_API_KEY')

def get_youtube_subscriber_count(api_key, channel_id):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if 'items' in data and len(data['items']) > 0:
        subscriber_count = data['items'][0]['statistics']['subscriberCount']
        return int(subscriber_count)
    else:
        raise Exception('Channel not found or invalid channel ID.')

def set_scrolling_text(wled_ip, text):
    url = f"http://{wled_ip}/json/state"
    payload = {
        "seg": [
            {
                "id": 0,
                "txt": text
            }
        ]
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        print("Text set successfully.")
    else:
        print(f"Failed to set text. Status code: {response.status_code}")

# Fetch YouTube subscriber count
try:
    subscriber_count = get_youtube_subscriber_count(youtube_api_key, youtube_channel_id)
    text = f"Subscribers: {subscriber_count}"
    print(text)
#    set_scrolling_text(wled_ip, text)
except Exception as e:
    print(f"Error: {e}")

