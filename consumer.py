from confluent_kafka import Consumer, KafkaException, KafkaError
import json
import logging
from alert import raiseAlert
from mongoconnect import connectdb
from config import config
TELEGRAM_BOT_TOKEN = config["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = config["TELEGRAM_CHAT_ID"]
# Logging setup
logging.basicConfig(level=logging.INFO)

# Consumer configuration
consumer_config = config["consumer_config"]

# Initialize the Kafka Consumer
consumer = Consumer(consumer_config)

# Subscribe to the Kafka topic
consumer.subscribe(['youtube_Video'])

client = connectdb()


# Function to consume and process messages from Kafka
def consume_messages():
    try:
        # Infinite loop to consume messages
        while True:
            msg = consumer.poll(timeout=1.0)  # Poll for new messages with a 1-second timeout

            if msg is None:
                # No message available within the timeout
                continue
            elif msg.error():
                # Error handling for Kafka messages
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logging.info(f"End of partition reached: {msg.partition()} at offset {msg.offset()}")
                else:
                    raise KafkaException(msg.error())
            else:
                # Successfully received a message, process it
                logging.info(f"Received message: {msg.value()}")
                # alert
                raiseAlert(msg.value(), client,TELEGRAM_BOT_TOKEN,TELEGRAM_CHAT_ID)

    except KeyboardInterrupt:
        logging.info("Consumer interrupted, shutting down...")
    finally:
        # Close the consumer gracefully when finished
        consumer.close()
        logging.info("Kafka Consumer closed gracefully.")


# Main entry point of the script
if __name__ == '__main__':
    consume_messages()
