import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

API_KEY_FILE = 'ExampleFile.json' #Your Private Api Key json File Location
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

def get_channel_info(channel_id):
    credentials = service_account.Credentials.from_service_account_file(API_KEY_FILE, scopes=SCOPES)
    youtube = build(API_NAME, API_VERSION, credentials=credentials)

    try:
        channel_response = youtube.channels().list(
            part='snippet,statistics,brandingSettings',
            id=channel_id
        ).execute()

        channel = channel_response['items'][0]

        channel_info = {
            'title': channel['snippet']['title'],
            'description': channel['snippet']['description'],
            'subscriber_count': channel['statistics']['subscriberCount'],
            'video_count': channel['statistics']['videoCount'],
            'view_count': channel['statistics']['viewCount'],
            'country': channel['brandingSettings']['channel']['country'],
            'published_at': channel['snippet']['publishedAt'],
        }

        return channel_info

    except Exception as e:
        return None

def get_most_popular_video(channel_id):
    credentials = service_account.Credentials.from_service_account_file(API_KEY_FILE, scopes=SCOPES)
    youtube = build(API_NAME, API_VERSION, credentials=credentials)

    try:
        videos_response = youtube.search().list(
            part='id',
            channelId=channel_id,
            maxResults=1,
            order='viewCount',
        ).execute()

        most_popular_video_id = videos_response['items'][0]['id']['videoId']

        video_response = youtube.videos().list(
            part='snippet,statistics',
            id=most_popular_video_id
        ).execute()

        most_popular_video = video_response['items'][0]

        popular_video_info = {
            'title': most_popular_video['snippet']['title'],
            'published_at': most_popular_video['snippet']['publishedAt'],
            'view_count': most_popular_video['statistics']['viewCount'],
        }

        return popular_video_info

    except Exception as e:
        return None

def get_latest_video(channel_id):
    credentials = service_account.Credentials.from_service_account_file(API_KEY_FILE, scopes=SCOPES)
    youtube = build(API_NAME, API_VERSION, credentials=credentials)

    try:
        recent_videos_response = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            maxResults=1,
            order='date',
        ).execute()

        latest_video_info = []
        for video in recent_videos_response['items']:
            video_info = {
                'title': video['snippet']['title'],
                'published_at': video['snippet']['publishedAt'],
            }
            latest_video_info.append(video_info)

        return latest_video_info

    except Exception as e:
        return []

# Usage example
if __name__ == '__main__':
    channel_id = 'UCMiJRAwDNSNzuYeN2uWa0pA'
    channel_info = get_channel_info(channel_id)
    popular_video_info = get_most_popular_video(channel_id)
    latest_video_info = get_latest_video(channel_id)

    print('Channel Info:', channel_info)
    print('Most Popular Video:', popular_video_info)
    print('Latest Videos:', latest_video_info)
