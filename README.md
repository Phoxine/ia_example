# IA Example Meeting Bot

This repository contains a simple meeting audio transcription and summarization utility.

The script `meeting_bot.py` uses OpenAI Whisper for transcription and the OpenAI API for generating a structured meeting summary.

## Features

- Transcribes audio files from `audio_files/`
- Summarizes meetings into:
  - Meeting summary
  - Decisions made
  - Action items
- Saves summaries as Markdown files in `summarys/`
- Supports concurrent processing

## Requirements

- Python 3.12+
- `OPENAI_API_KEY` environment variable
- `ffmpeg`
- Packages from `requirements.txt`

## Setup (Docker preferred)

### Docker Compose

This project is designed to run via Docker Compose.

Update `compose.yaml` to set your OpenAI API key:

```yaml
environment:
  - OPENAI_API_KEY=your_api_key_here
```

Build and run:

```bash
docker compose up --build
```

## Usage

1. Place meeting audio files in `audio_files/`.
2. Run the command:

```bash
docker compose up
```

3. Check `summarys/` for generated markdown summaries.

## output

```bash
$ docker compose up
Attaching to meeting-bot
meeting-bot  | Loading Whisper model...
meeting-bot  | Found 1 files.
meeting-bot  | 🎧 Processing: harvard.wav
meeting-bot  | ✅ Done: harvard.wav
meeting-bot  | 
meeting-bot  | 🎉 All tasks finished!
```

## Notes

- Supported audio formats: `.mp3`, `.wav`, `.m4a`
- The script will skip files that already have a summary file in `summarys/`
- The output filename is generated from the audio filename plus a timestamp

## Project Structure

- `meeting_bot.py` - main transcription and summarization script
- `requirements.txt` - Python dependencies
- `dockerfile` - Docker image build file
- `compose.yaml` - Docker Compose service definition
- `audio_files/` - input directory for audio files
- `summarys/` - output directory for markdown summaries
