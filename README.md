# YouTube Video Summarization Tool Using LLMs

This tool extracts and summarizes content from YouTube videos using large language models (LLMs). The application downloads the video, converts it to audio, transcribes the content, and then generates a concise summary using GPT-4 or other LLMs like `facebook/bart-large-cnn`.

## Features

- Download and convert YouTube videos to audio.
- Transcribe audio to text using Whisper.
- Summarize the transcribed text using GPT-4 or other LLMs.
- Automatically save the original transcription and the summary for future reference.

## Requirements

- Python 3.8+
- ffmpeg (for audio extraction)
- Whisper (for audio transcription)
- OpenAI API Key (for text summarization)
- YouTube-DL or yt-dlp (for downloading YouTube videos)

## Installation

1. **Install ffmpeg** for video-to-audio conversion:

   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

## Install the required Python libraries:
for example use pyenv, create one env and install requeriments 
```sh
pip install -r requirements.txt
```

## Execute script .py

```py
python summary_video.py --url https://www.youtube.com/watch?v=example
```
This create automatic dir: audio and data