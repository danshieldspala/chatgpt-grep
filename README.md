# chatgpt-grep

A utility script to search for specific messages within a ChatGPT data export and retrieve the titles of chats containing those messages.

## Background

When users export their data from ChatGPT, the provided JSON structure can be a bit challenging to navigate due to its nested structure. This tool helps users easily identify the titles of chats based on a keyword or phrase search.

## Usage

1. First, you'll need to download your ChatGPT data export, which will be in a `.zip` format.
2. Then, execute the script with the path to your `.zip` file and the target message you're searching for.

```bash
$ ./gptgrep.py path_to_your_data_export.zip "Your target message here"

