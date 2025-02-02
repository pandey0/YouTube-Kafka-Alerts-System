import json
import logging
import requests
from config import config
from confluent_kafka import Producer
import os

# Improved logging setup
logging.basicConfig(level=logging.DEBUG)  # Adjust level as needed


# Function to fetch playlist items from the YouTube API
def fetch_playlist_items_page(google_api_key, youtube_playlist_id, page_Token=None):
    response = requests.get("https://www.googleapis.com/youtube/v3/playlistItems", params={
        "key": google_api_key,
        "playlistId": youtube_playlist_id,
        "part": "contentDetails",
        "pageToken": page_Token
    })

    if response.status_code != 200:
        logging.error(f"Failed to fetch playlist items, status code: {response.status_code}")
        return {}

    payload = json.loads(response.text)
    logging.debug("Got the response %s", payload)
    return payload


# Function to fetch all items in the playlist
def fetch_playlist_all_item_details(google_api_key, youtube_playlist_id, next_Page_token=None):
    payload = fetch_playlist_items_page(google_api_key, youtube_playlist_id, next_Page_token)
    yield from payload.get("items", [])
    next_Page_token = payload.get("nextPageToken")
    if next_Page_token:
        yield from fetch_playlist_all_item_details(google_api_key, youtube_playlist_id, next_Page_token)


# Function to fetch video content details from the YouTube API
def fetch_video_content_page(google_api_key, videoid, page_token=None):
    response = requests.get("https://www.googleapis.com/youtube/v3/videos", params={
        "key": google_api_key,
        "id": videoid,
        "part": "snippet,statistics",
        "pageToken": page_token
    })

    if response.status_code != 200:
        logging.error(f"Failed to fetch video content, status code: {response.status_code}")
        return {}

    payload = json.loads(response.text)
    logging.debug("Got the response %s", payload)
    return payload


# Function to fetch all video content
def fetch_all_video_content(google_api_key, videoid, next_page_token=None):
    payload = fetch_video_content_page(google_api_key, videoid, next_page_token)
    yield from payload.get("items", [])
    next_page_token = payload.get("nextPageToken")
    if next_page_token:
        yield from fetch_all_video_content(google_api_key, videoid, next_page_token)


# Function to summarize video details
def summarize(video):
    return {
        "video_id": video["id"],
        "title": video["snippet"]["title"],
        "view": video["statistics"].get("viewCount", 0),
        "likecount": video["statistics"].get("likeCount", 0),
        "commentcount": video["statistics"].get("commentCount", 0),
    }


# Main function to process the playlist and send data to Kafka
def main():
    logging.info("Starting script")
    google_api_key = config["google_api_key"]  # Load API key from environment variable
    youtube_playlist_id = config["playlist_id"]
    print(f"Processing playlist ID: {youtube_playlist_id}")

    # Kafka producer configuration
    kafka_config = config["kafka_config"]
    producer = Producer(kafka_config)

    # Process all video items in the playlist
    for video_items in fetch_playlist_all_item_details(google_api_key, youtube_playlist_id):
        videoid = video_items["contentDetails"]["videoId"]
        print(f"Processing video ID: {videoid}")

        # Fetch and process video content
        for video_content in fetch_all_video_content(google_api_key, videoid):
            video_summary = summarize(video_content)
            logging.info("Got video details: %s", video_summary)

            # Serialize the video summary to JSON before sending to Kafka
            producer.produce(
                topic="youtube_Video",
                key=videoid,
                value=json.dumps(video_summary)  # Serialize to JSON string
            )

            # Ensure message is sent
            producer.flush()


if __name__ == '__main__':
    main()
