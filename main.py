import os
import subprocess
from pyrogram import Client, filters
import yt_dlp

# এনভায়রনমেন্ট ভেরিয়েবল থেকে তথ্যগুলো নিচ্ছে
app = Client("my_bot", 
             bot_token=os.getenv("BOT_TOKEN"), 
             api_id=int(os.getenv("API_ID")), 
             api_hash=os.getenv("API_HASH"))

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("বট সচল আছে! ভিডিও লিঙ্ক পাঠান।")

@app.on_message(filters.text & filters.regex(r"http"))
async def handle_video(client, message):
    url = message.text
    msg = await message.reply_text("📥 ডাউনলোড ও এডিটিং শুরু হচ্ছে...")
    
    try:
        # ভিডিও ডাউনলোড
        ydl_opts = {'format': 'best', 'outtmpl
