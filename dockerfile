FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

ENV OPENAI_API_KEY=""

CMD ["python", "meeting_bot.py"]
