import os
from pyrogram import Client, filters

# এনভায়রনমেন্ট থেকে টোকেন নিচ্ছে
BOT_TOKEN = os.getenv("BOT_TOKEN")

# আপনার নিজস্ব আইডি ও হ্যাশ
API_ID = 32767340
API_HASH = "132de334e7bb2da8b1164b17a21e5f52"

app = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("বট সচল হয়েছে! এখন ভিডিওর লিঙ্ক পাঠান।")

@app.on_message(filters.text & ~filters.command("start"))
async def handle_link(client, message):
    await message.reply_text("আমি লিঙ্কটি পেয়েছি, প্রসেস করছি...")

app.run()
