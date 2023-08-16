#!/usr/bin/python3
import json
import zipfile
import os
import sys

def extract_file_from_zip(zip_path, file_name):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        temp_dir = os.path.join(os.path.dirname(zip_path), 'temp_extract')
        os.makedirs(temp_dir, exist_ok=True)
        extracted_file_path = os.path.join(temp_dir, file_name)
        zip_ref.extract(file_name, temp_dir)
    return extracted_file_path

def find_chat_titles_and_urls_by_message(target_message, chats_data):
    target_message_lower = target_message.lower()
    matched_chats = []

    for chat in chats_data:
        for message_id, message_data in chat.get('mapping', {}).items():
            message_content = message_data.get('message', {}).get('content', {}) if message_data.get('message') else {}
            parts = message_content.get('parts', [])
            message_text = " ".join(part for part in parts).lower()
            if target_message_lower in message_text:
                conversation_id = chat.get('id', 'unknown_id')
                title = chat.get('title', 'unknown_title')
                url = f"https://chat.openai.com/c/{conversation_id}"
                matched_chats.append({'title': title, 'url': url})
                break

    return matched_chats

def main(zip_file, message_to_search):
    extracted_file = extract_file_from_zip(zip_file, 'conversations.json')

    with open(extracted_file, 'r') as file:
        data = json.load(file)

    matches = find_chat_titles_and_urls_by_message(message_to_search, data)

    os.remove(extracted_file)
    os.rmdir(os.path.dirname(extracted_file))

    if matches:
        print(f"Chats containing the message '{message_to_search}':")
        for match in matches:
            print(f"Title: {match['title']}\nURL: {match['url']}\n")
    else:
        print("Message not found in any chat.")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
