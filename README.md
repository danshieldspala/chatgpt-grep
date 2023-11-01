# chatgpt-grep

A utility script to search for specific messages within a ChatGPT data export and retrieve the titles of chats, and date of conversations containing those messages.

## Background

When users export their data from ChatGPT, the provided JSON structure can be a bit challenging to navigate due to its nested structure. This tool helps users easily identify the titles of chats based on a keyword or phrase search.

## Usage

1. First, you'll need to download your ChatGPT data export, which will be in a `.zip` format.
2. Then, execute the script with the path to your `.zip` file and the target message you're searching for.

```bash
$ ./gptgrep.py path_to_your_data_export.zip "Your target message here"
```

## Features

- Case-insensitive search within messages.
- Outputs the titles and URL links back to all chats that contain the target message.
- Easy extraction from the exported `.zip` without needing manual unzipping.
  
## Dependencies

- Python 3

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Ensure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
