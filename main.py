import os
import yt_dlp
import subprocess
from pyrogram import Client, filters

# এনভায়রনমেন্ট থেকে টোকেন ও আইডি নিচ্ছে
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID", "32767340"))
API_HASH = os.getenv("API_HASH", "132de334e7bb2da8b1164b17a21e5f52")

app = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("স্বাগতম! ভিডিও লিঙ্ক পাঠান, আমি সেটি কপিরাইট ফ্রি করে দেব।")

@app.on_message(filters.text & filters.regex(r"http"))
async def handle_video(client, message):
    url = message.text
    msg = await message.reply_text("📥 ভিডিও ডাউনলোড হচ্ছে...")
    
    try:
        # ১. ডাউনলোড
        ydl_opts = {'format': 'best', 'outtmpl': 'input.mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        await msg.edit_text("⚙️ এডিটিং চলছে...")
        
        # ২. এডিটিং (সরাসরি সিস্টেমের FFmpeg ব্যবহার করে)
        # হরাইজন্টাল ফ্লিপ, ক্রপ এবং মেটাডেটা রিমুভ
        subprocess.run([
            "ffmpeg", "-i", "input.mp4", 
            "-vf", "hflip,crop=iw-50:ih-50:25:25", 
            "-c:a", "copy", 
            "-map_metadata", "-1", 
            "-y", "final.mp4"
        ], check=True)
        
        # ৩. পাঠানো
        await message.reply_video("final.mp4", caption="✅ কপিরাইট ফ্রি ভিডিও প্রস্তুত!")
        
    except Exception as e:
        await message.reply_text(f"❌ এরর: {e}")
        
    finally:
        # ৪. ফাইল মুছে মেমোরি খালি করা
        for f in ["input.mp4", "final.mp4"]:
            if os.path.exists(f): 
                os.remove(f)

app.run()
