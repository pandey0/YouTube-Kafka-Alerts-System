config = {
    "google_api_key": "YOUR_GOOGLE_API_KEY",
    "playlist_id": "YOUR_YOUTUBE_PLAYLIST_ID",
    "kafka_config": {
        "bootstrap.servers": "YOUR_KAFKA_BROKER",
        "group.id": "youtube-group",
        "auto.offset.reset": "earliest"
    },
    "consumer_config": {
        "bootstrap.servers": "YOUR_KAFKA_BROKER",
        "group.id": "youtube-consumer-group",
        "auto.offset.reset": "earliest"
    },
    "uri": "mongodb://your_mongo_uri",
    "TELEGRAM_BOT_TOKEN": "your_bot_token",
    "TELEGRAM_CHAT_ID": "your_chat_id"
}
