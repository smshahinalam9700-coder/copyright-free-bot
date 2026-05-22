import os
from pyrogram import Client, filters
import yt_dlp
from moviepy.editor import VideoFileClip

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = 32767340
API_HASH = "132de334e7bb2da8b1164b17a21e5f52"

app = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("হ্যালো! ভিডিওর লিঙ্ক দিন, আমি প্রসেস করছি।")

@app.on_message(filters.text & ~filters.command("start"))
async def handle_link(client, message):
    url = message.text
    if "facebook.com" in url or "fb.watch" in url:
        msg = await message.reply_text("ডাউনলোড শুরু হচ্ছে...")
        
        # ভিডিও ডাউনলোডের অংশ
        ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        await msg.edit_text("ডাউনলোড শেষ! এডিট করছি...")
        
        # ভিডিও এডিটিংয়ের অংশ (যেমন: মেটাডেটা রিমুভ বা ফ্লিপ করা)
        clip = VideoFileClip("video.mp4")
        clip = clip.fx(lambda c: c.rotate(0)) # এখানে আপনার কাস্টম এডিটিং লজিক যোগ করুন
        clip.write_videofile("final.mp4")
        
        await message.reply_video("final.mp4", caption="✅ কপিরাইট ফ্রি ভিডিও প্রস্তুত।")
        
        # ফাইল ডিলিট করে দেওয়া
        os.remove("video.mp4")
        os.remove("final.mp4")
    else:
        await message.reply_text("দয়া করে একটি সঠিক ফেসবুক ভিডিও লিঙ্ক দিন।")

app.run()
