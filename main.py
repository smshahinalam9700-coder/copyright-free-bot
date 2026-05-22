import os
from pyrogram import Client, filters

# এনভায়রনমেন্ট থেকে টোকেন নিচ্ছে (নিরাপদ পদ্ধতি)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# যদি টোকেন সেট করা না থাকে, তবে বট চালু হবে না
if not BOT_TOKEN:
    raise ValueError("Error: BOT_TOKEN এনভায়রনমেন্ট ভেরিয়েবলে পাওয়া যায়নি!")

# বট ক্লায়েন্ট (এখানে API_ID এবং API_HASH প্রয়োজন)
# এগুলো my.telegram.org থেকে পাবেন
app = Client(
    "my_bot",
    bot_token=BOT_TOKEN,
    api_id=1234567,            # আপনার নিজস্ব API ID দিন
    api_hash="your_api_hash"   # আপনার নিজস্ব API Hash দিন
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("হ্যালো! বটটি সফলভাবে সচল হয়েছে।")

print("বট সচল হচ্ছে...")
app.run()
