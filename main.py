import os
import subprocess
import sys

# প্রয়োজনীয় লাইব্রেরি চেক ও ইনস্টলেশন
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from pyrogram import Client, filters
    import yt_dlp
except ImportError:
    install("pyrogram")
    install("tgcrypto")
    install("yt-dlp")
    from pyrogram import Client, filters
    import yt_dlp

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = 32767340
API_HASH = "132de334e7bb2da8b1164b17a21e5f52"

app = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("বট সচল আছে! ভিডিও লিঙ্ক পাঠান।")

@app.on_message(filters.text & filters.regex(r"http"))
async def handle_video(client, message):
    url = message.text
    msg = await message.reply_text("📥 ডাউনলোড হচ্ছে...")
    
    try:
        # ডাউনলোড
        ydl_opts = {'format': 'best', 'outtmpl': 'input.mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        await msg.edit_text("✅ ডাউনলোড সম্পন্ন। এখন ভিডিওটি এডিট করার জন্য তৈরি।")
        await message.reply_video("input.mp4", caption="আপনার ভিডিওটি এখানে।")
        
        # ফাইল ডিলিট
        if os.path.exists("input.mp4"): os.remove("input.mp4")
            
    except Exception as e:
        await message.reply_text(f"❌ এরর: {e}")

app.run()
