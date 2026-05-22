import os
from pyrogram import Client, filters

# এনভায়রনমেন্ট থেকে টোকেন নিচ্ছে (নিরাপদ পদ্ধতি)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# আপনার সংগৃহীত API ID এবং API HASH নিচে বসান
API_ID = 28659551
API_HASH = "80f121d51a65526e0b7849e830e9d40b"

# বট ক্লায়েন্ট তৈরি
app = Client(
    "my_bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

# /start কমান্ডের জন্য রেসপন্স
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("হ্যালো! বটটি সফলভাবে সচল হয়েছে।")

# বট রান করা
print("বট সচল হচ্ছে...")
app.run()
