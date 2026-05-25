# পাইথনের একটি হালকা সংস্করণ ব্যবহার করছি
FROM python:3.9-slim

# রেন্ডারে FFmpeg এবং গিট ইন্সটল করার জন্য প্রয়োজনীয় কমান্ড
RUN apt-get update && apt-get install -y ffmpeg

# ওয়ার্কিং ডিরেক্টরি সেট করা
WORKDIR /app

# রিকোয়ারমেন্টস ফাইল কপি ও ইন্সটল করা
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# বাকি কোড কপি করা
COPY . .

# বট চালু করা
CMD ["python", "main.py"]
