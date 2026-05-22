import os
import yt_dlp
from pyrogram import Client, filters
from moviepy.editor import *
import numpy as np

# এনভায়রনমেন্ট থেকে টোকেন নিচ্ছে
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = 32767340
API_HASH = "132de334e7bb2da8b1164b17a21e5f52"

app = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

def apply_copyright_protection(input_path, output_path):
    # ভিডিও লোড করা
    clip = VideoFileClip(input_path)
    
    # ১. লোগো রিমুভ করার জন্য ক্রপ করা (চারপাশ থেকে ৫০ পিক্সেল)
    clip = clip.crop(x1=50, y1=50, x2=clip.w-50, y2=clip.h-50)
    
    # ২. ৫ সেকেন্ড অন্তর কাট এবং ইফেক্ট যোগ
    duration = int(clip.duration)
    clips = []
    for i in range(0, duration, 5):
        subclip = clip.subclip(i, min(i + 5, duration))
        # মিরর এবং জুম ইফেক্ট
        subclip = subclip.fx(vfx.mirror_x).resize(1.02)
        clips.append(subclip)
    
    final = concatenate_videoclips(clips)
    
    # ৩. মেটাডেটা রিমুভ এবং এক্সপোর্ট
    final.write_videofile(output_path, codec="libx264", audio_codec="aac", ffmpeg_params=["-map_metadata", "-1"])
    
    clip.close()
    final.close()

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("হ্যালো! ভিডিও লিঙ্ক পাঠান, আমি সেটি কপিরাইট ফ্রি করে দেব।")

@app.on_message(filters.text & filters.regex(r"http"))
async def process_link(client, message):
    url = message.text
    msg = await message.reply_text("📥 ভিডিও ডাউনলোড হচ্ছে, দয়া করে অপেক্ষা করুন...")
    
    try:
        # ডাউনলোড
        ydl_opts = {'format': 'best', 'outtmpl': 'raw.mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        await msg.edit_text("✂️ ভিডিও এডিটিং চলছে...")
        
        # এডিটিং
        apply_copyright_protection("raw.mp4", "final.mp4")
        
        # পাঠানো
        await message.reply_video("final.mp4", caption="✅ কপিরাইট মুক্ত ভিডিও প্রস্তুত!")
        
    except Exception as e:
        await message.reply_text(f"❌ এরর হয়েছে: {e}")
    finally:
        # ফাইল ডিলিট
        if os.path.exists("raw.mp4"): os.remove("raw.mp4")
        if os.path.exists("final.mp4"): os.remove("final.mp4")

app.run()
