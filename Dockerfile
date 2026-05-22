FROM python:3.10-slim
RUN apt-get update && apt-get install -y ffmpeg
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir pyrogram tgcrypto yt-dlp
CMD ["python", "main.py"]
