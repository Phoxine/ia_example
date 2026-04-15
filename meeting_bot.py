import os
import sys
import whisper
from openai import OpenAI
from pathlib import Path
from datetime import datetime

# Step 1: Load Whisper model
print("Loading Whisper model...")
model = whisper.load_model("base")

# Step 2: Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    api_key = input("OPENAI_API_KEY not found in environment. Please enter your API key: ").strip()
    if not api_key:
        print("Error: API key is required to proceed.")
        sys.exit(1)

# Step 3: Get audio file from audio_files directory
audio_dir = Path("audio_files")
if not audio_dir.exists():
    print(f"Error: {audio_dir} directory does not exist.")
    sys.exit(1)

audio_files = list(audio_dir.glob("*.mp3")) + list(audio_dir.glob("*.wav")) + list(audio_dir.glob("*.m4a"))
if not audio_files:
    print(f"Error: No audio files found in {audio_dir}")
    sys.exit(1)

print(f"Found {len(audio_files)} audio file(s):")
for i, f in enumerate(audio_files, 1):
    print(f"  {i}. {f.name}")

if len(audio_files) == 1:
    audio_path = audio_files[0]
else:
    choice = input(f"Select audio file (1-{len(audio_files)}): ").strip()
    try:
        audio_path = audio_files[int(choice) - 1]
    except (ValueError, IndexError):
        print("Invalid selection.")
        sys.exit(1)

print(f"Processing: {audio_path.name}")

# Step 4: Transcribe audio to text
result = model.transcribe(str(audio_path))
transcript = result["text"]

print("\n=== Transcript ===")
print(transcript)

# Step 5: Send to LLM for summarization
client = OpenAI(api_key=api_key)

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
    messages=[
        {"role": "user", "content": prompt}
    ]
)

summary = response.choices[0].message.content

# Step 6: Save summary to summarys directory with timestamp
summary_dir = Path("summarys")
summary_dir.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d")
audio_name = audio_path.stem
summary_filename = f"{audio_name}_summary_{timestamp}.md"
summary_path = summary_dir / summary_filename

with open(summary_path, "w", encoding="utf-8") as f:
    f.write(summary)

print(f"\n✅ Complete! Summary saved to {summary_path}")