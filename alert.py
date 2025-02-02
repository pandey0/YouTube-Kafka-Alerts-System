import json
import requests


# Function to send a message to the Telegram chat
def send_telegram_alert(message, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID):
    url = "https://api.telegram.org/bot8196346478:AAH67GQ66XQiY0lQR-ve4wBz6FohIiK98rs/sendMessage"
    print(url)
    try:
        # Direct request post with payload in the same line
        print("Stared to send req")
        response = requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID, 'text': message})
        print("req sent")
        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Telegram: {e}")


def raiseAlert(data, client, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID):
    if client:
        db = client["youtubealert"]
        collection = db["countdata"]

        print(type(data))
        data_decode = data.decode()
        json_data = json.loads(data_decode)

        # Extract the unique identifier (video_id) and the count values
        video_id = json_data['video_id']
        new_view_count = json_data['view']
        new_like_count = json_data['likecount']
        new_comment_count = json_data['commentcount']
        title = json_data['title']

        # Step 4: Check if the video already exists in the collection
        existing_video = collection.find_one({'video_id': video_id})

        if existing_video:
            # Step 5: Compare the counts
            existing_view_count = existing_video['view']
            existing_like_count = existing_video['likecount']
            existing_comment_count = existing_video['commentcount']

            # Step 6: Trigger alert if counts have changed
            alert_message = []
            if new_view_count != existing_view_count:
                alert_message.append(f"View count has changed from {existing_view_count} to {new_view_count}.")
            if new_like_count != existing_like_count:
                alert_message.append(f"Like count has changed from {existing_like_count} to {new_like_count}.")
            if new_comment_count != existing_comment_count:
                alert_message.append(f"Comment count has changed from {existing_comment_count} to {new_comment_count}.")

            # Print the alert message if any changes were detected
            if alert_message:
                full_alert_message = f"ALERT: Changes detected for video {title}:\n" + "\n".join(alert_message)
                print(full_alert_message)
                send_telegram_alert(full_alert_message, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)

                # Step 7: Update the video data in the database with the new values
                collection.update_one(
                    {'video_id': video_id},  # Filter to match the video
                    {
                        '$set': {  # Update the fields with new values
                            'view': new_view_count,
                            'likecount': new_like_count,
                            'commentcount': new_comment_count
                        }
                    }
                )
                print(f"Database updated for video {video_id}.")
            else:
                print(f"No changes detected for video {video_id}.")
        else:
            # If no existing data, this is a new video, so we can insert it into the database
            collection.insert_one(json_data)
            print(f"New video data inserted for {video_id}.")
    else:
        print("Failed to connect to MongoDB.")
