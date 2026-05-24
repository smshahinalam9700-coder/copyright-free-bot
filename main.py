import os
import subprocess
from pyrogram import Client, filters
import yt_dlp

app = Client("my_bot", 
             bot_token=os.getenv("BOT_TOKEN"), 
             api_id=int(os.getenv("API_ID")), 
             api_hash=os.getenv("API_HASH"))

@app.on_message(filters.text & filters.regex(r"http"))
async def handle_video(client, message):
    try:
        url = message.text
        ydl_opts = {'format': 'best', 'outtmpl': 'input.mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # FFmpeg কমান্ড - সরাসরি পাথ ব্যবহার
        subprocess.run(["/usr/bin/ffmpeg", "-i", "input.mp4", "-vf", "hflip,crop=iw-50:ih-50:25:25", "-c:a", "copy", "-map_metadata", "-1", "-y", "final.mp4"], check=True)
        
        await message.reply_video("final.mp4")
        if os.path.exists("input.mp4"): os.remove("input.mp4")
        if os.path.exists("final.mp4"): os.remove("final.mp4")
    except Exception as e:
        await message.reply_text(f"Error: {e}")

app.run()
