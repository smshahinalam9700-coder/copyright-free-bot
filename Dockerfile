FROM python:3.10-slim

# FFmpeg ইনস্টল করা
RUN apt-get update && apt-get install -y ffmpeg

# ওয়ার্কিং ডিরেক্টরি সেট করা
WORKDIR /app
COPY . .

# লাইব্রেরি ইনস্টল করা
RUN pip install --no-cache-dir pyrogram tgcrypto yt-dlp moviepy

# বট স্টার্ট করা
CMD ["python", "main.py"]
