#!/usr/bin/python

import json
import zipfile
import os
import tempfile
import sys

def extract_file_from_zip(zip_path, target_file):
    with zipfile.ZipFile(zip_path, 'r') as z:
        temp_dir = tempfile.mkdtemp()  # creates a temporary directory
        z.extract(target_file, temp_dir)
        return os.path.join(temp_dir, target_file)

def find_chat_titles_by_message(target_message, chats_data):
    target_message_lower = target_message.lower()
    matched_titles = []  # List to store matching chat titles

    for chat in chats_data:
        for message_id, message_data in chat.get('mapping', {}).items():
            if not message_data or not isinstance(message_data, dict):
                continue
            message_details = message_data.get('message', {})
            if not message_details or not isinstance(message_details, dict):
                continue
            content_data = message_details.get('content', {})
            if content_data.get('content_type') == "text":
                message_text = " ".join(content_data.get('parts', [])).lower()  # Convert to lowercase
                if target_message_lower in message_text:
                    matched_titles.append(chat.get('title'))
                    break  # Break after one match in the same chat to avoid duplicate titles

    return matched_titles

def main(zip_file, message_to_search):
    extracted_file = extract_file_from_zip(zip_file, 'conversations.json')

    with open(extracted_file, 'r') as file:
        data = json.load(file)

    titles = find_chat_titles_by_message(message_to_search, data)

    # Clean up: Remove the temporary extracted file and its directory
    os.remove(extracted_file)
    os.rmdir(os.path.dirname(extracted_file))

    if titles:
        print(f"Chats containing the message '{message_to_search}':")
        for title in titles:
            print(title)
    else:
        print("Message not found in any chat.")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <path_to_zip_file> <message_to_search>")
    else:
        main(sys.argv[1], sys.argv[2])

