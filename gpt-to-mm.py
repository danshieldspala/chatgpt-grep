#!/usr/bin/python3
import sys
import zipfile
import json
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from datetime import datetime

def find_chat_titles_and_dates_by_message(search_term, data):
    matches = []
    for chat in data:
        title = chat.get('title', '')
        update_time = chat.get('update_time', None)
        formatted_time = int(update_time * 1000) if update_time else "Unknown time"
        conversation_elements = []

        for message_id, message_data in chat.get('mapping', {}).items():
            message_details = message_data.get('message', {})
            if not message_details:  # Skip if message details are None or empty
                continue
            message_content = message_details.get('content', {})
            parts = message_content.get('parts', [])
            message_text = ""
            for part in parts:
                if isinstance(part, dict):
                    if part.get('content_type') == 'image_asset_pointer':
                        continue  # Skip image entries
                    message_text += part.get('text', '')
                else:
                    message_text += part
            message_text = message_text.lower()
            if search_term.lower() in message_text:
                conversation_elements.append(message_text)

        if conversation_elements:
            match = {
                'date': formatted_time,
                'title': title,
                'elements': conversation_elements
            }
            matches.append(match)

    matches.sort(reverse=True, key=lambda x: x['date'])  # Sort by timestamp
    return matches

def create_mm_structure(matches):
    root = Element("map", version="1.1.0")
    root.append(Comment("To view this file, download free mind mapping software FreeMind from http://freemind.sourceforge.net"))
    id_counter = 1  # Initialize a counter for generating unique IDs
    for match in matches:
        conversation_node = SubElement(root, "node", CREATED=str(match['date']), MODIFIED=str(match['date']), TEXT=match['title'], ID=f"ID_{id_counter}")
        id_counter += 1  # Increment the counter for each node
        SubElement(conversation_node, "attribute", NAME="role", VALUE="conversation")
        SubElement(conversation_node, "attribute", NAME="content", VALUE=match["title"])
        for element in match["elements"]:
            subnode = SubElement(conversation_node, "node", CREATED=str(match['date']), MODIFIED=str(match['date']), TEXT="", ID=f"ID_{id_counter}")
            id_counter += 1  # Increment the counter for each node
            SubElement(subnode, "attribute", NAME="role", VALUE="message")
            SubElement(subnode, "attribute", NAME="content", VALUE=element)
    return root

def main(zip_filepath, search_term):
    try:
        with zipfile.ZipFile(zip_filepath, 'r') as z:
            with z.open('conversations.json') as f:
                data = json.load(f)
        matches = find_chat_titles_and_dates_by_message(search_term, data)
        mm_structure = create_mm_structure(matches)
        mm_xml = tostring(mm_structure, encoding="utf-8").decode()
        print(mm_xml)
    except FileNotFoundError:
        print(f"Error: The specified file '{zip_filepath}' for the path_to_export.zip argument could not be found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: gptgrep.py path_to_export.zip search_term")
    else:
        main(sys.argv[1], sys.argv[2])
