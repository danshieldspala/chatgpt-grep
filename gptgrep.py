#!/usr/bin/python3
import sys
import zipfile
import json
from datetime import datetime

BASE_URL = "https://chat.openai.com/c/"

def find_chat_titles_and_urls_by_message(search_term, data):
    matches = []
    for chat in data:
        title = chat.get('title', '')
        update_time = chat.get('update_time', None)
        formatted_time = datetime.fromtimestamp(update_time).strftime('%B %d, %Y %H:%M:%S') if update_time else "Unknown time"
        for message_id, message_data in chat.get('mapping', {}).items():
            message_details = message_data.get('message', {})
            if not message_details:  # Skip if message details is None or empty
                continue
            message_content = message_details.get('content', {})
            parts = message_content.get('parts', [])
            message_text = " ".join(part for part in parts).lower()
            if search_term.lower() in message_text:
                matches.append((formatted_time, title, BASE_URL + message_id))
                break
    matches.sort(reverse=True, key=lambda x: x[0])  # Sort by timestamp
    return matches

def main(zip_filepath, search_term):
    with zipfile.ZipFile(zip_filepath, 'r') as z:
        with z.open('conversations.json') as f:
            data = json.load(f)
    matches = find_chat_titles_and_urls_by_message(search_term, data)
    for match in matches:
        print(f"{match[0]} - {match[1]} - {match[2]}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script_name.py path_to_export.zip search_term")
    else:
        main(sys.argv[1], sys.argv[2])


