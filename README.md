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

2. **Install the required Python libraries**:
   Use `pyenv` to create an environment and install requirements:
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API Key**:
   You need to set your OpenAI API key as an environment variable. You can do this by adding the following line to your shell's configuration file (e.g., `.bashrc`, `.zshrc`):

   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

   Replace `'your-api-key-here'` with your actual OpenAI API key. After adding this line, reload your shell configuration by running:

   ```bash
   source ~/.bashrc  # or source ~/.zshrc
   ```

## Execution Workflow

### Process a Single YouTube Video

To process a single YouTube video, use the `summary_video.py` script:

```sh
python summary_video.py --url https://www.youtube.com/watch?v=example
```

This will download the audio, transcribe it, and generate a summary. It automatically creates directories for audio and data.

### Process All Videos from a YouTube Channel

To process all videos from a YouTube channel, follow these steps:

1. **Download all videos from a YouTube channel**:
   Use the `download_all_videos_channel.py` script to download audio from a YouTube channel.
   ```sh
   python download_all_videos_channel.py --channel_url https://www.youtube.com/@herostartup4493 --output youtube_audio_downloads
   ```

2. **Transcribe the downloaded audio**:
   Use the `process_audio_text.py` script to transcribe the audio files into text.
   ```sh
   python process_audio_text.py --input youtube_audio_downloads
   ```

3. **Correct and curate the transcribed text**:
   Use the `process_text_curate.py` script to correct and improve the transcribed text.
   ```sh
   python process_text_curate.py --input youtube_audio_downloads
   ```

This sequence of scripts allows for the mass downloading, transcription, and text correction of YouTube videos from a channel.
