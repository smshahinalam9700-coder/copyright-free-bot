import os
import subprocess
import yt_dlp
from pyrogram import Client, filters

# এনভায়রনমেন্ট থেকে টোকেন নিচ্ছে
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = 32767340
API_HASH = "132de334e7bb2da8b1164b17a21e5f52"

app = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

def edit_video(input_path, output_path):
    # FFmpeg ব্যবহার করে ভিডিও মিরর করা, লোগো ক্রপ করা এবং মেটাডেটা রিমুভ করা
    # এটি মেমোরি সাশ্রয়ী এবং দ্রুত
    cmd = [
        'ffmpeg', '-i', input_path,
        '-vf', 'hflip,crop=iw-50:ih-50:25:25', 
        '-c:a', 'copy',
        '-map_metadata', '-1',
        '-y', output_path
    ]
    subprocess.run(cmd, check=True)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("হ্যালো! আমি তৈরি। ভিডিও লিঙ্ক দিন, আমি এডিট করে দিচ্ছি।")

@app.on_message(filters.text & filters.regex(r"http"))
async def handle_video(client, message):
    # একই ভিডিওর জন্য বটের বারবার প্রসেসিং বন্ধ করার জন্য ফিল্টার
    url = message.text
    msg = await message.reply_text("📥 ডাউনলোড ও এডিটিং শুরু হচ্ছে...")
    
    try:
        # ১. ডাউনলোড
        ydl_opts = {'format': 'best', 'outtmpl': 'input.mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        await msg.edit_text("⚙️ এডিটিং চলছে...")
        
        # ২. এডিটিং
        edit_video("input.mp4", "final.mp4")
        
        # ৩. পাঠানো
        await message.reply_video("final.mp4", caption="✅ আপনার এডিটেড ভিডিও প্রস্তুত!")
        
    except Exception as e:
        await message.reply_text(f"❌ এরর: {e}")
        
    finally:
        # ৪. ফাইল মুছে মেমোরি খালি করা
        for f in ["input.mp4", "final.mp4"]:
            if os.path.exists(f): os.remove(f)

app.run()
