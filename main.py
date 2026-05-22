import os
import yt_dlp
from pyrogram import Client, filters
from moviepy.editor import *

# কনফিগারেশন
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = 32767340
API_HASH = "132de334e7bb2da8b1164b17a21e5f52"

app = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

def edit_video(input_path, output_path):
    # ভিডিও লোড করা
    clip = VideoFileClip(input_path)
    
    # লোগো রিমুভ করার জন্য ক্রপ (কোণা থেকে ৫০ পিক্সেল)
    clip = clip.crop(x1=50, y1=50, x2=clip.w-50, y2=clip.h-50)
    
    # মিরর ইফেক্ট ও সামান্য জুম
    clip = clip.fx(vfx.mirror_x).resize(1.02)
    
    # ভিডিও সেভ করা (মেটাডেটা রিমুভ করে)
    clip.write_videofile(output_path, codec="libx264", audio_codec="aac", 
                         ffmpeg_params=["-map_metadata", "-1"])
    clip.close()

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("হ্যালো! যেকোনো ভিডিও লিঙ্ক পাঠান, আমি সেটি এডিট করে দিচ্ছি।")

@app.on_message(filters.text & filters.regex(r"http"))
async def handle_video(client, message):
    url = message.text
    msg = await message.reply_text("📥 ডাউনলোড ও এডিটিং শুরু হচ্ছে...")
    
    try:
        # ডাউনলোড
        ydl_opts = {'format': 'best', 'outtmpl': 'input.mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        await msg.edit_text("⚙️ এডিটিং চলছে...")
        
        # এডিটিং
        edit_video("input.mp4", "final.mp4")
        
        # পাঠানো
        await message.reply_video("final.mp4", caption="✅ কপিরাইট ফ্রি ভিডিও প্রস্তুত।")
        
    except Exception as e:
        await message.reply_text(f"❌ এরর: {e}")
    finally:
        # ফাইল ডিলিট (মেমোরি খালি রাখার জন্য জরুরি)
        for f in ["input.mp4", "final.mp4"]:
            if os.path.exists(f): os.remove(f)

app.run()
