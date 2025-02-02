# YouTube-Kafka-Alerts-System

## Overview
The YouTube Kafka Alerts System is a real-time data monitoring solution that tracks YouTube video statistics (views, likes, comments) for a specified playlist. It uses Apache Kafka for message streaming between producer and consumer components, MongoDB for storing historical video statistics, and Telegram for sending real-time notifications when significant changes are detected in a video’s statistics.

## Features
- **Real-Time Monitoring**: Automatically fetches and processes video statistics from a YouTube playlist.
- **Change Detection**: Monitors views, likes, and comments for each video and detects changes.
- **Alert System**: Sends Telegram notifications when changes in video statistics are detected.
- **Scalable Architecture**: Built using Kafka for decoupling the producer and consumer services.
- **Database Integration**: Uses MongoDB to store video stats for comparison and historical tracking.

## Technologies
- **YouTube API**: Fetches video and playlist data.
- **Kafka**: Message streaming platform for handling video data between producer and consumer.
- **MongoDB**: NoSQL database for storing video statistics.
- **Telegram Bot API**: Sends alerts via Telegram when video stats change.
- **Python**: Main programming language used to implement the system.

## Setup Instructions

### Prerequisites
Before you begin, ensure that you have the following installed:
- Python 3.x
- Docker and Docker Compose (for Kafka and Zookeeper setup)
- MongoDB (either locally or cloud service)
- Telegram Bot: Create a bot via BotFather on Telegram and get the Bot Token and Chat ID.

### 1. Clone the repository
Clone the project to your local machine:
git clone https://github.com/your-username/youtube-kafka-alerts.git
cd youtube-kafka-alerts
### 2. Install dependencies
Use pip to install the required Python packages:
pip install -r requirements.txt
This will install all necessary dependencies listed in requirements.txt
### 3. Set up Kafka Cluster with Docker
You can easily set up Kafka and Zookeeper using Docker Compose. Kafka requires Zookeeper, which is why both are included in this setup.
Create a docker-compose.yml file in your project directory. Then start the Kafka and Zookeeper services:
docker-compose up -d
This will spin up Kafka and Zookeeper in the background. Kafka will be available at localhost:9092.
### 4. Configure credentials
Before running the system, you'll need to replace the placeholders in the config.py file with your own credentials.

Open the config.py file and set:

Google API Key: Get an API key from the Google Developers Console. Enable the YouTube Data API v3 and create an API key.
YouTube Playlist ID: This is the ID of the playlist you want to monitor. You can find it in the URL when you open the playlist on YouTube.
Kafka Broker: By default, it should be localhost:9092 if running locally.
MongoDB URI: This is the connection string for MongoDB (e.g., mongodb://localhost:27017).
Telegram Bot Token and Chat ID: Get these from your Telegram bot.
### 5. Running the System
Run the Producer:
The producer fetches video statistics from the YouTube API and sends them to Kafka. Run the producer script with:
python src/producer/producer.py
Run the Consumer:
The consumer listens for messages from Kafka, processes the video statistics, and sends alerts via Telegram if there are any changes. Run the consumer script with:
python src/consumer/consumer.py
### 6. MongoDB Setup
Ensure MongoDB is set up and accessible by the script. The script will store video statistics in the youtubealert database, specifically in the countdata collection.

### Contributing
Feel free to fork the repository and submit issues or pull requests. Contributions are welcome!
