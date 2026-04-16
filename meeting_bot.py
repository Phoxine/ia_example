import os
import sys
import whisper
from openai import OpenAI
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


MAX_WORKERS = 3

# Step 1: Load Whisper model
print("Loading Whisper model...")
model = whisper.load_model("base")

# Step 2: API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY not found.")
    sys.exit(1)

client = OpenAI(api_key=api_key)

# Step 3: Audio files
audio_dir = Path("audio_files")
if not audio_dir.exists():
    print(f"Error: {audio_dir} directory does not exist.")
    sys.exit(1)

audio_files = list(audio_dir.glob("*.mp3")) + \
              list(audio_dir.glob("*.wav")) + \
              list(audio_dir.glob("*.m4a"))

if not audio_files:
    print("No audio files found.")
    sys.exit(1)

print(f"Found {len(audio_files)} files.")

# Step 4: Summary dir
summary_dir = Path("summarys")
summary_dir.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d")


def process_file(audio_path: Path):
    audio_name = audio_path.stem
    summary_filename = f"{audio_name}_summary_{timestamp}.md"
    summary_path = summary_dir / summary_filename

    if summary_path.exists():
        return f"⏩ Skipped: {audio_path.name}"

    try:
        print(f"🎧 Processing: {audio_path.name}")

        # Transcribe
        result = model.transcribe(str(audio_path))
        transcript = result["text"]

        # Summarize
        prompt = f"""
You are a meeting assistant. Based on the transcript provided, organize and summarize:

1. Meeting Summary (3-5 key points)
2. Decisions Made
3. Action Items (TODO + Owner)

Transcript:
{transcript}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        summary = response.choices[0].message.content

        # Save
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)

        return f"✅ Done: {audio_path.name}"

    except Exception as e:
        return f"❌ Failed: {audio_path.name} | {e}"


# Concurrent processing
results = []

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = [executor.submit(process_file, f) for f in audio_files]

    for future in as_completed(futures):
        result = future.result()
        print(result)
        results.append(result)

print("\n🎉 All tasks finished!")